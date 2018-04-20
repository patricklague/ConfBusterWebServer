<?php
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
#                ("TO" stands for "TransportObject")
# ============================================================
class ComputeJobTO 
{
    # --------------------------------------------------------
    #                Public attributes
    # --------------------------------------------------------
    public $email;
    public $fileName;
    public $fileContent;


    # --------------------------------------------------------
    # public ComputeJobTO(string email, string fileName, string fileContent)
    # --------------------------------------------------------
    # Constructor for a compute job object.
    #
    # Parameters :    
    #   string email       : The receipiant's email
    #   string fileName    : The file name with its extension (ie. macrocycle.mol2)
    #   string fileContent : The content of the submitted input file
    # --------------------------------------------------------
    function __construct($email, $fileName, $fileContent)
    {
        $this->email = $email;
        $this->fileName = $fileName;
        $this->fileContent = $fileContent;
    }
    

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
    public function __toString()
    {
        $str = <<<TO_STRING_DEFINITION
email={$this->email}
fileName={$this->fileName}
fileContent={$this->fileContent}
TO_STRING_DEFINITION;

        return str;
    }
}


// End ComputeJobTO.php
?>