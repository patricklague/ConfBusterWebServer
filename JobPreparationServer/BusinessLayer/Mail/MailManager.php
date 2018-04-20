<?php
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : MailManager.php
# DESCRIPTION : See class description.
# CLASSES     : MailManager
#               MailQuickMessages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================
# Namespace used by PHPMailer
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

# File dependencies
require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/Mail/PHPMailer/src/PHPMailer.php');
require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/Mail/PHPMailer/src/SMTP.php');
require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/Mail/PHPMailer/src/Exception.php');

require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/TransportObjects/ComputeJobTO.php');

/*
# Necessary for PHP Debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
*/

# ============================================================
#  CLASS       : MailManager
#  DESCRIPTION : Manager class for sending emails.
# ============================================================
class MailManager
{
    # --------------------------------------------------------
    #              Private Static attributes
    # --------------------------------------------------------
    /* 
     * Verbose information taken from PHPMailer/src/SMTP.php
     * 
     * 0 : No debug output, default
     * 1 : Client commands
     * 2 : Client commands and server responses
     * 3 : As DEBUG_SERVER plus connection status
     * 4 : Low-level data output, all messages.
     */
    private static $SMTP_DEBUG_VERBOSE = 2;

    private static $SMTP_SERVER_ADDRESS = "***.***.***.***";
    private static $SENDER_EMAIL = "***@***.***";
    private static $SENDER_NAME = "***";

    # --------------------------------------------------------
    # private static PHPMailer GetEmailTemplate ()
    # --------------------------------------------------------
    # Create an email template.
    #
    # Parameters :
    #   None
    # 
    # Returns : 
    #   PHPMailer 
    # --------------------------------------------------------
    private static function GetEmailTemplate()
    {
        $email = new PHPMailer(true);                                          // True = Enable exception

        $email->SMTPDebug = MailManager::$SMTP_DEBUG_VERBOSE;
        $email->isSMTP();
        $email->Host = MailManager::$SMTP_SERVER_ADDRESS;
        $email->SMTPAuth = false;                                               // True = Enable Authentication to SMTP Account

        $email->CharSet = 'UTF-8';                                              // Override default : 'iso-8859-1'

        $email->setFrom(MailManager::$SENDER_EMAIL, MailManager::$SENDER_NAME); // (email_address, email_name)

        return $email;
    }

    # --------------------------------------------------------
    # private static boolean SendEmailToSMTPServer(MIMEMultipart email)
    # --------------------------------------------------------
    # Send an email and manage the exceptions.
    #
    # Parameters :
    #   MIMEMultipart email : The email to send.
    # 
    # Returns : 
    #   True - If the message has been sucessfully sent 
    # --------------------------------------------------------
    private static function SendEmailToSMTPServer($email)
    {
        $messageSent = false;

        try {
            $messageSent = $email->send();
            $messageSent = true;
            
        } catch (Exception $e) {
            $messageSent = false;
            echo $e->getMessage();
        }
        
        return $messageSent;
    }

    # --------------------------------------------------------
    # public static boolean SendEmail(string receipiantEmail, string subject, string textMessage, string htmlMessage = None, string filePath = None)
    # --------------------------------------------------------
    # Send an email. A file can be provided in attachment.
    #
    # Parameters :
    #   string receipiantAddress            : The receipiant's email address
    #   string subject                      : The email subject
    #   string textMessage                  : A plain text message
    #   string htmlMessage       (optional) : A message with html tags
    #   string filePath          (optional) : The full path of the file
    #
    # Returns : 
    #   True - If the message has been sucessfully sent
    # --------------------------------------------------------
    public static function SendEmail($receipiantAddress, $subject, $textMessage, $htmlMessage=null, $filePath=null)
    {
        $email = MailManager::GetEmailTemplate();

        // General properties
        $email->addAddress($receipiantAddress);
        $email->Subject = $subject;

        // Check if an html message is provided
        $isHTML = !is_null($htmlMessage);
        $email->isHTML($isHTML);
        
        // Ajust the body consequently to the html message
        if($isHTML)
        {
            $email->Body = $htmlMessage;
            $email->AltBody = $textMessage;
        }
        else
        {
            $email->Body = $textMessage;
        }        

        // Add the attachment if provided
        if(!is_null($filePath))
            $email->addAttachment($filePath);


        return MailManager::SendEmailToSMTPServer($email);
    }
}



# ============================================================
#  CLASS       : MailQuickMessages
#  DESCRIPTION : Container class for all the email used by
#                the JobPreparationServer.
# ============================================================
class MailQuickMessages
{
    # --------------------------------------------------------
    #              Private Static attributes
    # --------------------------------------------------------
    # For HTML supported client
    public static $HTML_EMAIL_FOOTER = <<<HTML_EMAIL_FOOTER_DEFINITION

    <br>

    <p>
        Please Cite !
        <p>
            <em>
            B&eacute;gin,&nbsp;G., Barbeau,&nbsp;X., Vincent,&nbsp;A.T. &amp; Lag&uuml;e,&nbsp;P. ConfBuster&nbsp;Web&nbsp;Server: a free web application for macrocycle conformational search and analysis (in preparation).
            </em>
        </p>
        <p>
            <em>
                Barbeau,&nbsp;X., Vincent,&nbsp;A.T. &amp; Lag&uuml;e,&nbsp;P., (2018). ConfBuster: Open-Source Tools for Macrocycle Conformational Search and Analysis. Journal of Open Research Software. 6(1),&nbsp;p.1. DOI: <a href="http://doi.org/10.5334/jors.189">http://doi.org/10.5334/jors.189</a>
            </em>
        </p>
    </p>

    <br>

    <p>
        <em>
            Thank you for using ConfBuster!
            <br>
            <a href="http://confbuster.org">http://confbuster.org</a>
        </em>
    </p>
</body>
</html>
HTML_EMAIL_FOOTER_DEFINITION;


    # For HTML not supported client
    public static $TEXT_EMAIL_FOOTER = <<<TEXT_EMAIL_FOOTER_DEFINITION


Please Cite !

Begin, G., Barbeau, X., Vincent, A.T. & Lague, P. ConfBuster Web Server: a free web application for macrocycle conformational search and analysis (in preparation).

Barbeau, X., Vincent, A.T. & Lague, P., (2018). ConfBuster: Open-Source Tools for Macrocycle Conformational Search and Analysis. Journal of Open Research Software. 6(1), p.1. DOI: http://doi.org/10.5334/jors.189


Thank you for using ConfBuster !
http://confbuster.org
TEXT_EMAIL_FOOTER_DEFINITION;


    # --------------------------------------------------------
    # public static boolean JobReceptionConfirmation(ComputeJobTO $computeJobTO, int queuePosition)
    # --------------------------------------------------------
    # Send an email to acknowledge the reception of the
    # data input file.
    #
    # Parameters :
    #   ComputeJobTO $computeJobTO : The compute job information
    #   int $queuePosition         : The job position in queue
    # 
    # Returns : 
    #   True - If the message has been sucessfully sent
    # --------------------------------------------------------
    public static function JobReceptionConfirmation($computeJobTO, $queuePosition)
    {    
        // For HTML supported mail client
        $htmlMessage = <<<HTML_MESSAGE_DEFINITION
<html>
<head></head>
<body>
    <h3>Compute Job Received</h3>
       
    <p>This is an automated message to indicate the reception of the compute query.</p>

    <br>
    
    <p>Submitted information:</p>
    <ul>
        <li>Email : {$computeJobTO->email}</li>
        <li>Data file : {$computeJobTO->fileName}</li>
    </ul>

    <br>
    
    <p>The compute job was added to queue:</p>
    <ul>
        <li>Current position in queue : {$queuePosition}</li>
    </ul>
 
    <br>

    <p>Another message will be sent when the job is out of queue.<p>
HTML_MESSAGE_DEFINITION;

    
        // For HTML not supported mail client
        $textMessage = <<<TEXT_MESSAGE_DEFINITION
Compute Job Received

This is an automated message to indicate the reception of the compute query.

Submitted information:
    * Email : {$computeJobTO->email}
    * Data file : {$computeJobTO->fileName}

The compute job was added to queue:
    * Current position in queue : {$queuePosition}

Another message will be sent when the job is out of queue.
TEXT_MESSAGE_DEFINITION;


        // Send the prepared message
        return MailManager::SendEmail($computeJobTO->email,
                                      "Compute Job Received",
                                      $textMessage . MailQuickMessages::$TEXT_EMAIL_FOOTER,
                                      $htmlMessage . MailQuickMessages::$HTML_EMAIL_FOOTER);
    }


    # --------------------------------------------------------
    # public static boolean MaxJobReached(ComputeJobTO $computeJobTO, int $maxJobPerUser)
    # --------------------------------------------------------
    # Inform the user that the maximum number of job in 
    # queue for this email address is reached.
    # 
    # Parameters :
    #   ComputeJobTO $computeJobTO : The compute job information
    #   int $maxJobPerUser         : The number of job in queue allowed by user
    # 
    # Returns : 
    #   True - If the message has been sucessfully sent
    # --------------------------------------------------------
    public static function MaxJobReached($computeJobTO, $maxJobPerUser)
    {    
        // For HTML supported mail client
        $htmlMessage = <<<HTML_MESSAGE_DEFINITION
<html>
<head></head>
<body>
    <h3>Compute Job Denied</h3>
    
    <p>This is an automated message to indicate the refusal of the compute query.</p>

    <br>
    
    <p>Job information:</p>
    <ul>
        <li>Email : {$computeJobTO->email}</li>
        <li>Data file : {$computeJobTO->fileName}</li>
    </ul>
    
    <br>

    <p>The following errors prevented the job to be add to queue.</p>
    <ul>
        <li>Maximum number of jobs per user reached. Only {$maxJobPerUser} jobs are allowed in queue for each user.</li>
        <ul>
            <li>Number of jobs in queue for the user {$computeJobTO->email} : {$maxJobPerUser}.</li>
        </ul>
    </ul>

    <br>

    <p>Please come back when one compute job related to this email will be out of queue.</p>
    <p>To ensure data confidentiality, all the information about the compute query was deleted.</p>
    <p>If the error persists, please contact a representative on the ConfBuster website.</p>
HTML_MESSAGE_DEFINITION;


        // For HTML not supported mail client
        $textMessage = <<<TEXT_MESSAGE_DEFINITION
Compute Job Denied

This is an automated message to indicate the refusal of the compute query.

Job information:
    * Email : {$computeJobTO->email}
    * Data file : {$computeJobTO->fileName}


The following errors prevented the job to be added to queue.
    * Maximum number of jobs per user reached. Only {$maxJobPerUser} jobs are allowed in queue for each user.
        * Number of jobs in queue for the user {$computeJobTO->email} : {$maxJobPerUser}.

Please come back when one compute job related to this email will be out of queue.

To ensure data confidentiality, all the information about the compute query was deleted.

If the error persists, please contact a representative on the ConfBuster website.
TEXT_MESSAGE_DEFINITION;


        // Send the prepared message
        return MailManager::SendEmail($computeJobTO->email,
                                      "Compute Job Denied",
                                      $textMessage . MailQuickMessages::$TEXT_EMAIL_FOOTER,
                                      $htmlMessage . MailQuickMessages::$HTML_EMAIL_FOOTER);
    }
}

// End MailManager.php
?>
