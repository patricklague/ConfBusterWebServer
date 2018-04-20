<?php
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : DataReception.php
# DESCRIPTION : See the script description.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Necessary for PHP Debugging
/*
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
*/

# ============================================================
#                         DEPENDENCIES
# ============================================================


# ============================================================
#                         MAIN SCRIPT
# ------------------------------------------------------------
# Script for managing the transfert of the compute job to
# the Job Preparation Server.
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Notice for developpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Only one header can be set for a PHP page. 
#
# Page redirection were made in Javascript to allow more 
# then one possible redirection (Home/Confirmation).
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#          Structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (01) Receive data from the web interface.
#
# (02) Get the text content of the file.
#
# (03) Validate the data. 
#        True  : If one of the criteria is wrong, then the
#                user desactivated the browser javascript
#                and thus found a way to submit the
#                data anyway. => Go to step 4
#        False : The javascript validation worked. => Go to step 5
#
#     (04) Redirect the user to the home page without sending the job.
#
# (05) Send the data to the compute server.
#
# (06) Redirect the user to the confirmation page.
# ============================================================


# ~~~~~~~~~~
#    (01)
# ~~~~~~~~~~
$email = $_POST['email'];
$fileName = $_FILES["datafile"]["name"];
$fileTMPName = $_FILES["datafile"]["tmp_name"]; // The file is uploaded in the /tmp directory of the linux kernel by default.  
                                                // This variable contains the name automaticaly generated for this file. 

# ~~~~~~~~~~
#    (02)
# ~~~~~~~~~~
$fileHandle = fopen($fileTMPName, "r");
$fileContent = fread($fileHandle, filesize($fileTMPName));
fclose($fileHandle);

# ~~~~~~~~~~
#    (03)
# ~~~~~~~~~~
if(ValidationUtil::ValidateInputData($email,$fileName,$fileContent) == false)
{
    # ~~~~~~~~~~
    #    (04)
    # ~~~~~~~~~~    
    echo "<!DOCTYPE html>
          <html>
              <head>
                  <script>
                      document.location.href = '403.html';
                  </script>
              </head>
              <body></body>
          </html>";    
}
    
# ~~~~~~~~~~
#    (05)
# ~~~~~~~~~~
TransferUtil::SendSynchronousPostRequest("http://***.***.***.***:8080/JobPreparationServer/BusinessLayer/ComputeJobPreparation.php",
                                         $email,
                                         $fileName,
                                         $fileContent);

# ~~~~~~~~~~
#    (06)
# ~~~~~~~~~~
echo   "<!DOCTYPE html>
        <html>
            <head>
                <script>
                    document.location.href = 'Confirmation.html';
                </script>
            </head>
            <body></body>
        </html>";  

# ============================================================
#                       END OF SCRIPT 
# ============================================================


# ============================================================
#                     CLASSES DEFINITION
# ============================================================

# ============================================================
#  CLASS       : TransferUtil
#  DESCRIPTION : Container class transfering data between
#                servers.
# ============================================================
class TransferUtil
{
    # --------------------------------------------------------
    # public static void SendSynchronousPostRequest(string $serverLocation, string $email, string $fileName, string $fileContent)
    # --------------------------------------------------------
    # Send the data from this server to another web server by
    # using an HTTP POST transaction.
    #
    # Parameters :
    #     string $serverLocation : The server URL
    #     string $email          : The receipiant's email address
    #     string $fileName       : The name of the data file
    #     string $fileContent    : The content (data) of the data file
    # 
    # Returns : 
    #   void
    # --------------------------------------------------------
    public static function SendSynchronousPostRequest($serverLocation, $email, $fileName, $fileContent)
    {
        // PHP Post resquest preparation
        $postRequestData = array('email' => $email,
                                'filename' => $fileName,
                                'filecontent' => $fileContent);
        $postRequestConfiguration = array(
            'http' => array(
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                'method'  => 'POST',
                'content' => http_build_query($postRequestData)
            )
        );
        
        // Send the data to server
        $postRequestContext = stream_context_create($postRequestConfiguration);
        $postRequestResult = file_get_contents($serverLocation, false, $postRequestContext);

        /*
        //  ****************************************
        //  For debugging the Job Preparation Server
        //  ****************************************
        if ($postRequestResult == FALSE) 
        {
            echo 'A problem happened when sending the data to the compute server:';
            echo '<br><br>';
            var_dump($postRequestResult); // Echo the results from the remote server file ComputeJobPreparation.php
        }
        */
    }
}


# ============================================================
#  CLASS       : ValidationUtil
#  DESCRIPTION : Container class for the second input data
#                validation. (The first validation is made
#                in Javascript on the home web page).
# ============================================================
class ValidationUtil
{
    # --------------------------------------------------------
    # public static boolean ValidateInputData(string $email, string $fileName, string $fileContent)
    # --------------------------------------------------------
    # Validate a second time the data sent by the user. 
    #
    # Note : The first validation is made on the home web page
    #        in Javascript.
    #
    # Parameters :
    #     string $email       : The receipiant's email address
    #     string $fileName    : The name of the data file
    #     string $fileContent : The content (data) of the data file
    # 
    # Returns : 
    #   boolean
    # --------------------------------------------------------
    public static function ValidateInputData($email, $fileName, $fileContent)
    {
        return  ValidationUtil::ValidateEmail($email) &&
                ValidationUtil::ValidateFileName($fileName) &&
                ValidationUtil::ValidateFileContent($fileContent);
    }


    # --------------------------------------------------------
    # public static boolean ValidateEmail(string $email)
    # --------------------------------------------------------
    # Validate the user email.
    #
    # (1) Has to be not be empty.
    # (2) Has to respect the maximum length.
    # (3) Has to respect the REGEX used in the Javascript validation.
    #
    #
    # Parameters :
    #     string $email : The receipiant's email address
    # 
    # Returns : 
    #   boolean
    # --------------------------------------------------------
    public static function ValidateEmail($email)
    {
        $isValid = true;

        // (1)
        if(empty($email))
            $isValid = false;

        // (2)
        if(strlen($email) > 50)
            $isValid = false;

        // (3)
        $regex = <<<REGEX_EMAIL
/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
REGEX_EMAIL;
        if( ! preg_match($regex,$email) )
            $isValid = false;


        return $isValid;
    }

    # --------------------------------------------------------
    # public static boolean ValidateFileName(string $fileName)
    # --------------------------------------------------------
    # Validate the name of the data file.
    #
    # (1) Has to be not be empty.
    # (2) Has to respect the REGEX used in the Javascript validation.
    # (3) Has to respect the maximum length.
    # (4) Has to respect the accepted extension.
    #
    #
    # Parameters :
    #     string $fileName : The name of the data file
    # 
    # Returns : 
    #   boolean
    # --------------------------------------------------------
    public static function ValidateFileName($fileName)
    {
        $isValid = true;

        // (1)
        if(empty($fileName))
            $isValid = false;

        // (2)
        $regex = <<<REGEX_FILENAME
/^[a-zA-Z0-9_.\-]+\.[a-zA-Z0-9_.\-]+$/
REGEX_FILENAME;
        if( ! preg_match($regex,$fileName) )
            $isValid = false;

        // (3)
        if(strlen($fileName) > 50)
            $isValid = false;

        // (4)
        $fileNameArray = explode(".",$fileName);
        $extension = $fileNameArray[sizeof($fileNameArray) - 1]; // Get the value at the last index
        switch ($extension) 
        {
            case "pdb":
                break;
            case "sdf":
                break;
            case "mol":
                break;
            case "mol2":
                break;
            default:
                $isValid = false;
        }

        return $isValid;
    }


    # --------------------------------------------------------
    # public static boolean ValidateFileContent(string $fileName)
    # --------------------------------------------------------
    # Validate the name of the data file.
    #
    # (1) Must not be empty.
    # (2) Must respect the maximum length.
    #
    #
    # Parameters :
    #     string $fileContent : The content (data) of the data file
    # 
    # Returns : 
    #   boolean
    # --------------------------------------------------------
    public static function ValidateFileContent($fileContent)
    {
        $isValid = true;

        // (1)
        if(empty($fileContent))
            $isValid = false;

        // (2)
        if(strlen($fileContent) > 1000000) // 1 MB
            $isValid = false;


        return $isValid;
    }
}


// End DataReception.php
?>
