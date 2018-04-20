#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : QueueManager.py
# DESCRIPTION : See the program description.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================
# Configuration of the Compute server path
import sys
sys.path.insert(0, '/var/www/ConfBuster/ComputeServer')

# Other core dependency
import thread
import time

# Server modules
from BusinessLayer.ManagerClasses.ComputeManager import ComputeManager
from BusinessLayer.ManagerClasses.MailManager import MailManager

from BusinessLayer.TransportObjects.ComputeJobTO import ComputeJobTO

from DatabaseLayer.DatabaseManager import DatabaseQuickQueries



# ============================================================
#                         MAIN METHOD
# ------------------------------------------------------------
# Autonomous server for managing the compute job queue.
#
# Note : This program should be launched manually 
#        with the following command :
# 
#        python QueueManager.py         
# 
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#          Structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (1) Configure the queue server 
#
# (2) Get the number of jobs currently in process.
#     If the number does not exceed the configured limit : Go to step 3
#       
#       (3) Check in database for potential compute jobs in the queue.
#           If one is found : Go to step 4
# 
#               (4) Retreive and delete the compute job information from the queue.
#
#               (5) Update the number of current active jobs.
#
#               (6) Launch the compute session in a thread.
#
# (7) Wait before looping to step 2 (prevents query overload)
# ============================================================
if __name__ == "__main__":

    # ~~~~~~~~~~
    #    (1)
    # ~~~~~~~~~~
    jobLimit_ComputeServer = 1          # The maximum number of job the server will compute at the same time
    jobLimit_Queue = 1                  # The maximum number of job a user can have in queue
    waitTimeBeforeNextQueueCheck = 15   # The time in second
    
    DatabaseQuickQueries.ConfigureComputeServer(jobLimit_ComputeServer)
    DatabaseQuickQueries.ConfigureQueue(jobLimit_Queue)
    
    # ~~~~~~~~~~
    #    (2)
    # ~~~~~~~~~~
    while True :

        numberOfCurrentJobsInProcess = DatabaseQuickQueries.GetNumberOfJobInProcess()

        if(numberOfCurrentJobsInProcess < jobLimit_ComputeServer):
            
            # ~~~~~~~~~~
            #    (3)
            # ~~~~~~~~~~
            computeJobTO = DatabaseQuickQueries.RetreiveOldestQueuedJob()
            
            if(computeJobTO is not None):
            
                # ~~~~~~~~~~
                #    (4)
                # ~~~~~~~~~~    
                DatabaseQuickQueries.RemoveJobFromQueue(computeJobTO.id)
                
                # ~~~~~~~~~~
                #    (5)
                # ~~~~~~~~~~
                DatabaseQuickQueries.IncrementNumberOfJobInProcess()
                
                # ~~~~~~~~~~
                #    (6)
                # ~~~~~~~~~~
                thread.start_new_thread( ComputeManager.StartNewJob, (computeJobTO,) )

        # ~~~~~~~~~~
        #    (7)
        # ~~~~~~~~~~
        time.sleep(waitTimeBeforeNextQueueCheck)

# End QueueManager.py
