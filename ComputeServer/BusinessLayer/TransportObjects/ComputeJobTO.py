#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : ComputeJobTO.py
# DESCRIPTION : See class description.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================

# ============================================================
#  CLASS       : ComputeJobTO
#  DESCRIPTION : Transport class for encapsulating the properties
#                of a Compute Job Object.
#                (TO stands for TransportObject)
# ============================================================
class ComputeJobTO:
    
    # --------------------------------------------------------
    # public ComputeJobTO(string email, string fileName, string fileType, string fileContent, int id = -1, string submissionDateTime = None)
    # --------------------------------------------------------
    # Constructor for a compute job object.
    #
    # Parameters :    
    #   string email                         : The receipiant's email
    #   string fileName                      : The data file name with the extension (eg. macrocycle.mol2)
    #   string fileType                      : The type (ie. "mol2") of the submitted file
    #   string fileContent                   : The content of the submitted input file
    #   int id                    (optional) : The database automatically generated id
    #   string submissionDateTime (optional) : Mysql format of the time the job has been submitted
    # --------------------------------------------------------
    def __init__(self, email, fileName, fileType, fileContent, id = -1, submissionDateTime = None):
        self.id = int(id)
        self.email = email
        self.fileName = fileName
        self.fileType = fileType
        self.fileContent = fileContent
        self.submissionDateTime = submissionDateTime

    # --------------------------------------------------------
    # public toString()
    # --------------------------------------------------------
    # Returns the formatted value of the object in a string format.
    #
    # Parameters :
    #   None
    #
    # Returns :
    #   string - The object in a string format
    # --------------------------------------------------------
    def __str__(self):
        out_str = """\
id={}
email={}
fileName={}
fileType={}
fileContent={}
submissionDateTime={}
"""
        return out_str.format(self.id,
                              self.email,
                              self.fileName,
                              self.fileType,
                              self.fileContent,
                              self.submissionDateTime)
                              
# End ComputeJobTO.py