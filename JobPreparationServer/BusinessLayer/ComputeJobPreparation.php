<?php 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : ComputeJobPreparation.php
# DESCRIPTION : See the script description.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

/*
# Necessary for PHP Debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
*/

# ============================================================
#                         DEPENDENCIES
# ============================================================
require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/Mail/MailManager.php');
require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/TransportObjects/ComputeJobTO.php');

require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/DatabaseLayer/DatabaseManager.php');


# ============================================================
#                         MAIN SCRIPT
# ------------------------------------------------------------
# Main script for managing the preparation/creation of the compute job.
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#          Structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (01) Receive data from the web server.
#
# (02) Create a transport object for the compute job.
#
# (03) Get the number of job the user has currently in queue.
#      If the number of exceeds the limit => Go to step 4.
#
#     (04) Email the user about the situation and stop the job creation process.
#
# (05) Add the job to the database.
#
# (06) Email the user to confirm the job query reception
# ============================================================

# ~~~~~~~~~~
#    (01)
# ~~~~~~~~~~
$email = $_POST["email"];
$fileName = $_POST["filename"];
$fileContent = $_POST["filecontent"];

# ~~~~~~~~~~
#    (02)
# ~~~~~~~~~~
$computeJobTO = new ComputeJobTO($email, $fileName, $fileContent);

# ~~~~~~~~~~
#    (03)
# ~~~~~~~~~~
$jobLimit = DatabaseQuickQueries::GetJobLimitPerUser();
$userJobs = DatabaseQuickQueries::CountUserJobsInQueue($email);

// To add code robustness, the operator >= is used instead of the ==
if( $userJobs >= $jobLimit ) 
{
    # ~~~~~~~~~~
    #    (04)
    # ~~~~~~~~~~
    MailQuickMessages::MaxJobReached($computeJobTO, $userJobs);
    exit(0);
}

# ~~~~~~~~~~
#    (05)
# ~~~~~~~~~~
DatabaseQuickQueries::AddToQueue($computeJobTO);

# ~~~~~~~~~~
#    (06)
# ~~~~~~~~~~
$queuePosition = DatabaseQuickQueries::GetNumberOfJobInQueue();
MailQuickMessages::JobReceptionConfirmation($computeJobTO, $queuePosition);


# End ComputeJobPreparation.php
?>