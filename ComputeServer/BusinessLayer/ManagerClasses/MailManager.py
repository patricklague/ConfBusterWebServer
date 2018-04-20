#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : MailManager.py
# DESCRIPTION : See class description.
# CLASSES     : MailManager
#               MailQuickMessages
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================
# System dependency
from os.path import basename

# Mail dependencies
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.utils import COMMASPACE, formatdate

# Configuration of the Compute server path
import sys
sys.path.insert(0, '/var/www/ConfBuster/ComputeServer')

# Server modules
from BusinessLayer.TransportObjects.ComputeJobTO import ComputeJobTO


# ============================================================
#  CLASS       : MailManager
#  DESCRIPTION : Manager class for sending emails.
# ============================================================
class MailManager:
    
    # --------------------------------------------------------
    #              Private Static attributes
    # --------------------------------------------------------
    __smtp_server = "***.***.***.***"
    __sender_name = "***"
    __sender_address = "***@***.***"


    # --------------------------------------------------------
    # private static MIMEMultipart __GetEmailTemplate()
    # --------------------------------------------------------
    # Create an email template.
    #
    # Parameters :
    #   None
    # 
    # Returns : 
    #   MIMEMultipart 
    # --------------------------------------------------------
    @staticmethod
    def __GetEmailTemplate():
        # 'alternative' : allows sending the message with a text and html version 
        email = MIMEMultipart('alternative')
        # Other properties
        email['From'] = formataddr((str(Header(MailManager.__sender_name,'utf-8')),
                                    MailManager.__sender_address) )
        email['Date'] = formatdate(localtime=True)
        
        return email


    # --------------------------------------------------------
    # private static boolean __SendEmailToSMTPServer(MIMEMultipart email)
    # --------------------------------------------------------
    # Send an email and manage the exceptions.
    #
    # Parameters :
    #   MIMEMultipart email : The email to send.
    # 
    # Returns : 
    #   True - If the message has been sucessfully sent 
    # --------------------------------------------------------
    @staticmethod
    def __SendEmailToSMTPServer(email):

        #successMessage = 'Message sent to receipiant : ' + email['to']
        #errorMessage = 'Message could not be sent to receipiant : ' + email['to']
        
        messageSent = False

        smtp = None

        try:
            smtp = smtplib.SMTP(MailManager.__smtp_server)
            smtp.sendmail(email['From'], email['To'], email.as_string())
            messageSent = True
            #print(successMessage)
        except:
            messageSent = False
            #print(errorMessage)
        finally:
            if smtp is not None:
                smtp.close()

        return messageSent

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
    @staticmethod
    def SendEmail(receipiantAddress, subject, textMessage, htmlMessage=None, filePath=None):
        # Add the other email headers
        email = MailManager.__GetEmailTemplate()
        email['To'] = receipiantAddress
        email['Subject'] = subject

        # Add the text message to the email
        mime_text_msg = MIMEText(textMessage, 'plain', "utf-8")
        email.attach(mime_text_msg)
        
        # If provided : Add the html message
        if (htmlMessage is not None) :
            mime_html_msg = MIMEText(htmlMessage, 'html',  "utf-8")
            email.attach(mime_html_msg)
        

        # If provided : Add a file in attachment
        if (filePath is not None) : 
            with open(filePath, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=basename(filePath))
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filePath)
                email.attach(part)

        # Send the email
        return MailManager.__SendEmailToSMTPServer(email)



# ============================================================
#  CLASS       : MailQuickMessages
#  DESCRIPTION : Container class for all the email used by
#                the ComputeServer.
# ============================================================
class MailQuickMessages:

    # --------------------------------------------------------
    #              Private Static attributes
    # --------------------------------------------------------
    # For HTML supported client
    __html_footer ="""\
    
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
"""

    # For HTML not supported client
    __text_footer ="""\


Please Cite !

Begin, G., Barbeau, X., Vincent, A.T. & Lague, P. ConfBuster Web Server: a free web application for macrocycle conformational search and analysis (in preparation).

Barbeau, X., Vincent, A.T. & Lague, P., (2018). ConfBuster: Open-Source Tools for Macrocycle Conformational Search and Analysis. Journal of Open Research Software. 6(1), p.1. DOI: http://doi.org/10.5334/jors.189


Thank you for using ConfBuster !
http://confbuster.org
"""


    # --------------------------------------------------------
    # public static boolean JobInitialization(ComputeJobTO computeJobTO)
    # --------------------------------------------------------
    # Send an email to inform the user that the compute job just started.
    # 
    #
    # Parameters :
    #   ComputeJobTO computeJobTO : The compute job information
    #
    # Returns : 
    #   True - If the message has been sucessfully sent 
    # --------------------------------------------------------
    @staticmethod
    def JobInitialization(computeJobTO):
        # Message for HTML Supported Client
        htmlMessage = """\
<html>
<head></head>
<body>
    <h3>Compute Job Started</h3>
 
    <p>This is an automated message to indicate that the compute job is out of queue and is now in process.</p>

    <p>A message with the result data will follow as soon as possible.</p>

    <p>Job information:</p>
    <ul>
        <li>Email : {}</li>
        <li>Data file : {}</li>
    </ul>
"""
        # Message for non-supported HTML Client
        textMessage = """\
Compute Job Started

This is an automated message to indicate that the compute job is out of queue and is now in process.

A message with the result data will follow as soon as possible.


Job information:
    * Email : {}
    * Data file : {}
"""

        # Add the missing value to the prepared messages
        htmlMessage = htmlMessage.format(computeJobTO.email,
                                         computeJobTO.fileName)

        textMessage = textMessage.format(computeJobTO.email,
                                         computeJobTO.fileName)

        # Send the message to the user
        return MailManager.SendEmail(computeJobTO.email,
                                     "Compute Job Started",
                                     textMessage + MailQuickMessages.__text_footer,
                                     htmlMessage + MailQuickMessages.__html_footer)


    # --------------------------------------------------------
    # public static void ComputeResults(ComputeJobTO computeJobTO, string resultFilePath)
    # --------------------------------------------------------
    # Send an email to inform the user that the compute job just started.
    # 
    #
    # Parameters :
    #   ComputeJobTO computeJobTO : The compute job information
    #   string resultFilePath     : The path of the results file
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def ComputeResults(computeJobTO, resultFilePath):
        # Message for HTML Supported Client
        htmlMessage = """\
<html>
<head></head>
<body>
    <h3>Compute Job Finished</h3>
 
    <p>Here is the archive file containing the results of ConfBuster Macrocycle Conformation Search.</p>

    <p>Job information:</p>
    <ul>
        <li>Email : {}</li>
        <li>Data file : {}</li>
    </ul>
    
    <p>Attention:</p>
    <ul>
        <li>The email client has to allow attachment.</li>
        <li>The email provider has to allow attachment.</li>
        <li>If the .zip file is not included this message, please try again with another email client or another email address.</li>
    </ul>
"""

        # Message for non-supported HTML Client
        textMessage = """\
Compute Job Finished

Here is the archive file containing the results of ConfBuster Macrocycle Conformation Search.

Job information:
    * Email : {}
    * Data file : {}

Attention :
    * The email client has to allow attachment.
    * The email provider has to allow attachment.
    * If the .zip file is not included this message, please try again with another email client or another email address.
"""

        # Add the missing value to the prepared messages
        htmlMessage = htmlMessage.format(computeJobTO.email,
                                         computeJobTO.fileName)

        textMessage = textMessage.format(computeJobTO.email,
                                         computeJobTO.fileName)

        # Send the message to the user
        MailManager.SendEmail(computeJobTO.email,
                              "Compute Job Finished",
                              textMessage + MailQuickMessages.__text_footer,
                              htmlMessage + MailQuickMessages.__html_footer,
                              resultFilePath)


    # --------------------------------------------------------
    # public static void ComputeError(ComputeJobTO computeJobTO)
    # --------------------------------------------------------
    # Send an email to inform the user of the interruption of the
    # compute process.
    # 
    # Note : Error managing is kept simple here ; only one error 
    #        message is available.
    #
    # Parameters :
    #   ComputeJobTO computeJobTO : The compute job information
    #
    # Returns : 
    #   void 
    # --------------------------------------------------------
    @staticmethod
    def ComputeError(computeJobTO):
        # Message for HTML Supported Client
        htmlMessage = """\
<html>
<head></head>
<body>
    <h3>Compute Job Aborted</h3>
 
    <p>This is an automated message to indicate the interruption of the compute query.</p>

    <br>

    <p>Job information:</p>
    <ul>
        <li>Email : {}</li>
        <li>Data file : {}</li>
    </ul>

    <br>

    <p>The following errors prevented ConfBuster to work properly :</p>
    <ul>
        <li>Unnappropriate datafile content.</li>
    </ul>

    <br>

    <p>Please make sure :</p>
    <ul>
        <li>The file contains 3D coordinates.</li>
        <ul>
            <li>A file with only 2D coordinates will be rejected.</li>
        </ul> 

        <li>The file contains hydrogen atoms.</li>
        <ul>
            <li>A file without hydrogens will be rejected.</li>
        </ul> 

        <li>The data file contains only one molecule.</li>
        <ul>
            <li>A file with more than one molecule coordinates will be rejected.</li>
        </ul>

        <li>The molecule contains only one macrocycle.</li>
        <ul>
            <li>A molecule with more than one ring of at least 7 atoms will be rejected.</li>
        </ul>

        <li>The file contains the appropriate data format according to its extension.</li>
        <ul>
            <li>Example : The example.mol2 file should contain data corresponding to the MOL2 format.</li>
        </ul>
    </ul>

    <br>

    <p>To ensure data confidentiality, all the information about the compute query was deleted.</p>
    <p>If the error persist, please contact a representative on the ConfBuster website.</p>
"""

        # Message for non-supported HTML Client
        textMessage = """\
Compute Job Aborted

This is an automated message to indicate the interruption of the compute query.

Job information:
    * Email : {}
    * Data file : {}


The following errors prevented ConfBuster to work properly :
    * Unnappropriate datafile content.

Please make sure :
    * The file contains 3D coordinates.
        * A file with only 2D coordinates will be rejected.

    * The file contains hydrogen atoms.
        * A file without hydrogens will be rejected.

    * The data file contains only one molecule.
        * A file with more than one molecule coordinates will be rejected.

    * The molecule contains only one macrocycle.
        * A molecule with more than one ring of at least 7 atoms will be rejected.

    * The file contains the appropriate data format according to its extension.
        * Example : The example.mol2 file should contain data corresponding to the MOL2 format.


To ensure data confidentiality, all the information about the compute query was deleted.
If the error persists, please contact a representative on the ConfBuster website.
"""

        # Add the missing value to the prepared messages
        htmlMessage = htmlMessage.format(computeJobTO.email,
                                         computeJobTO.fileName)

        textMessage = textMessage.format(computeJobTO.email,
                                         computeJobTO.fileName)

        # Send the message to the user
        MailManager.SendEmail(computeJobTO.email,
                              "Compute Job Aborted",
                              textMessage + MailQuickMessages.__text_footer,
                              htmlMessage + MailQuickMessages.__html_footer)

# End MailManager.py