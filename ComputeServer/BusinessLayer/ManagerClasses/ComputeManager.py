#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : ComputeManager.py
# DESCRIPTION : See class description.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================

# Configuration of the Compute server path
import sys
sys.path.insert(0, '/var/www/ConfBuster/ComputeServer')

# Other core dependancies
import time
import os
import subprocess

# Server modules
from BusinessLayer.ManagerClasses.FileSystemManager import FileSystemManager
from BusinessLayer.ManagerClasses.MailManager import MailQuickMessages

from BusinessLayer.TransportObjects.ComputeJobTO import ComputeJobTO

from DatabaseLayer.DatabaseManager import DatabaseQuickQueries


# ============================================================
#  CLASS       : ComputeManager
#  DESCRIPTION : Manager class for handling compute jobs.
# ============================================================
class ComputeManager:
    
    # --------------------------------------------------------
    #                Private Static attributes
    # --------------------------------------------------------
    __Path_of_job_compute_area = "/var/www/ConfBuster/ComputeServer/ActiveJobs"


    # --------------------------------------------------------
    # public static void StartNewJob(ComputeJobTO computeJobTO)
    # --------------------------------------------------------
    # Handle a compute job process.
    # 
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #          Structure
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # (1) Check if a job object was provided.
    # (2) Create a compute directory in the compute area
    # (3) Create the data input file
    # (4) Email the user to aknowledge the job initilization.
    # (5) Launch the ConfBuster compute commands
    # (6) Create the results archive file
    # (7) Email ConfBuster results/error to the user
    # (8) Delete the compute directory
    # (9) Decrement the active job value in the database
    #
    #
    # Parameters :
    #   ComputeJobTO computeJobTO : The object which contains all the informations of the compute job
    # 
    # Returns : 
    #   void 
    # --------------------------------------------------------
    @staticmethod
    def StartNewJob(computeJobTO = None):

        # ~~~~~~~~~~
        #    (1)
        # ~~~~~~~~~~  
        # Drop the job if no transport object was provided
        if computeJobTO is None:
            print "Error (ComputeManager.py,StartNewJob()) : The compute job should not be None. | " + time.strftime("%Y-%b-%d_%Hh%Mm%Ss", time.localtime()) + "\n\n"
            return

        computeErrorOccured = False

        # ~~~~~~~~~~
        #    (2)
        # ~~~~~~~~~~
        computeDirectoryName   = str(computeJobTO.id)
        computeDirectoryName  += "_" 
        computeDirectoryName  += time.strftime("%Y-%b-%d_%Hh%Mm%Ss", time.localtime())
        computeDirectoryName  += "_" 
        computeDirectoryName  += str(int(round(time.time() * 1000)))
        
        computeDirectoryPath = ComputeManager.__Path_of_job_compute_area + "/" + computeDirectoryName

        FileSystemManager.CreateDirectory(computeDirectoryPath)

        # ~~~~~~~~~~
        #    (3)
        # ~~~~~~~~~~ 
        fileNameWithoutExtension = ('.').join(computeJobTO.fileName.split('.')[:-1])
        fileName = computeJobTO.fileName
        filePath = computeDirectoryPath + "/" + fileName

        FileSystemManager.WriteFile(filePath, computeJobTO.fileContent)   

        # ~~~~~~~~~~
        #    (4)
        # ~~~~~~~~~~ 
        messageSent = MailQuickMessages.JobInitialization(computeJobTO)
        if messageSent == False:
            computeErrorOccured = True

        # ~~~~~~~~~~
        #    (5)
        # ~~~~~~~~~~ 
        try:
            # The job won't be compute if we can't reach the user by email
            if computeErrorOccured == False:
                computeErrorOccured = ComputeManager.__ExecuteConfbuster(computeDirectoryPath, fileName, fileNameWithoutExtension)

        except Exception, e:
            print e
            computeErrorOccured = True

        # ~~~~~~~~~~
        #    (6)
        # ~~~~~~~~~~
        zipFolderPath = computeDirectoryPath + "/" + "ConfBuster_Results"
        zipFilePath = zipFolderPath + ".zip"

        FileSystemManager.CreateDirectory(zipFolderPath)
        FileSystemManager.MoveAllItems(computeDirectoryPath, zipFolderPath)
        os.system("cd " + computeDirectoryPath + " && zip -q9r ConfBuster_Results.zip ConfBuster_Results")

        # ~~~~~~~~~~
        #    (7)
        # ~~~~~~~~~~
        if computeErrorOccured:
            MailQuickMessages.ComputeError(computeJobTO)
        else:
            MailQuickMessages.ComputeResults(computeJobTO, zipFilePath)

        # ~~~~~~~~~~
        #    (8)
        # ~~~~~~~~~~
        FileSystemManager.DeleteDirectory(computeDirectoryPath)

        # ~~~~~~~~~~
        #    (9)
        # ~~~~~~~~~~
        DatabaseQuickQueries.DecrementNumberOfJobInProcess()


    # --------------------------------------------------------
    # private static boolean __ExecuteConfbuster(string computeDirectoryPath, string fileName, string fileNameWithoutExtension)
    # --------------------------------------------------------
    # Confbuster compute routine
    # 
    #
    # Parameters :
    #   string computeDirectoryPath     : The path of the compute directory
    #   string fileName,                : The name of the file 
    #   string fileNameWithoutExtension : The name of the file without its extension
    #
    # Returns : 
    #   boolean - True if a compute error happened 
    # --------------------------------------------------------
    @staticmethod
    def __ExecuteConfbuster(computeDirectoryPath, fileName, fileNameWithoutExtension):

        # Initilize the error witness
        computeErrorOccured = False

        # Define the compute output indicators
        automaticFileHeader = """\
#
# This file was automatically generated by the ConfBuster compute server
#
# http://confbuster.org
#
"""
        
        separator = """\
#
#
#
"""    

        automaticFileFooter = """\
#
# End of output
#"""
        ConfBusterMinimizationCommand = separator + "# ConfBuster-Single-Molecule-Minimization.py -i " + fileName + "\n" + separator
                                        
        ConfBusterLinearSamplingCommand = separator + "# ConfBuster-Macrocycle-Linear-Sampling.py -i " + fileNameWithoutExtension + ".mol2" + "\n" + separator

        ConfBusterAnalysisCommand = separator + "# ConfBuster-Analysis.py -i " + fileNameWithoutExtension + " -R " + fileNameWithoutExtension + ".mol2" + "\n" + separator

        # Execute compute commands
        systemOutputBuffer  = str( os.system("cd " + computeDirectoryPath + " && echo '" + automaticFileHeader + "' >> compute_output.log") )

        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && echo '" + ConfBusterMinimizationCommand + "' >> compute_output.log") )
        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && ConfBuster-Single-Molecule-Minimization.py -i " + fileName + " >> compute_output.log") )

        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && echo '" + ConfBusterLinearSamplingCommand + "' >> compute_output.log") )
        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && ConfBuster-Macrocycle-Linear-Sampling.py -i " + fileNameWithoutExtension + ".mol2" + " >> compute_output.log") )

        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && echo '" + ConfBusterAnalysisCommand + "' >> compute_output.log") )
        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && ConfBuster-Analysis.py -i " + fileNameWithoutExtension + " -R " + fileNameWithoutExtension + ".mol2" + " >> compute_output.log") )

        systemOutputBuffer += str( os.system("cd " + computeDirectoryPath + " && echo -n '" + automaticFileFooter + "' >> compute_output.log") )

        # Generate an error witness if an error happened in the ConfBuster programs
        # Note 1 : os.system returns 0 if no error happened
        # Note 1 : The systemOutputBuffer contains the error code of each os.system command
        # Note 2 : A non 0 error code counts as an error
        if systemOutputBuffer != '00000000':
            computeErrorOccured = True

        return computeErrorOccured


# End ComputeManager.py