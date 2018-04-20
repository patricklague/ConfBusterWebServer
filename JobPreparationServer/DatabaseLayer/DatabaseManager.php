<?php
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : DatabaseManager.php
# DESCRIPTION : See classes description.
# CLASSES     : DatabaseConnection
#               DatabaseManager
#               DatabaseQuickQueries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Necessary for PHP Debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

# ============================================================
#                         DEPENDENCIES
# ============================================================
require_once ($_SERVER['DOCUMENT_ROOT']  . '/' . 'JobPreparationServer/BusinessLayer/TransportObjects/ComputeJobTO.php');

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Need the installation of the mysql pdo driver on the server.
#
# Example for debian :
# sudo apt install php-mysql
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#  CLASS       : DatabaseConnection
#  DESCRIPTION : Database connection class for handling the 
#                database connectivity.
#  IMPORTANT   : This class is NOT static. 
# ============================================================
class DatabaseConnection
{
    /* Inheritance would have been also possible here. */   
    protected $pdo;

    protected $database;
    protected $ip;
    protected $port;
    protected $user;
    protected $password;
    protected $encoding = array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8');

    # --------------------------------------------------------
    # public DatabaseConnection(string ip, string user, string password, string database)
    # --------------------------------------------------------
    # Constructor for a database connection object.
    #
    #
    # ~~~~~~~~~~~~~~~~~~~~~
    # Constructor structure
    # ~~~~~~~~~~~~~~~~~~~~~
    # (1) Allocates instance variables
    # (2) Opens the connection
    #
    #
    # Parameters :
    #   string ip       : The connection ip (can also be a DNS or the server hostname)
    #   int port        : (Mysql default = 3306 )
    #   string user     : The connection user name
    #   string password : The connection password
    #   string database : The database name
    # --------------------------------------------------------
    function __construct($ip, $port, $user, $password, $database)
    {
        $this->ip = $ip;
        $this->port    = $port;
        $this->user     = $user;
        $this->password = $password;
        $this->database = $database;

        $this->pdo = new PDO("mysql:host=" . $this->ip . ";" . 
                             "port=" . $this->port . ";" .
                             "dbname=" . $this->database,
                             $this->user,
                             $this->password,
                             $this->encoding);
    }


    # --------------------------------------------------------
    # public void CloseDatabaseConnection()
    # --------------------------------------------------------
    # Close the connection to the database
    # 
    #
    # Parameters :
    #   None
    #
    # Returns : 
    #   void 
    # --------------------------------------------------------
    public function CloseDatabaseConnection()
    {
        if( !is_null($this->pdo) )
        {
            $this->pdo = null;
        }            
    }
}



# ============================================================
#  CLASS       : DatabaseManager
#  DESCRIPTION : Manager class for handling the database.
# ============================================================
class DatabaseManager extends DatabaseConnection
{

    # --------------------------------------------------------
    #                Private Static attributes
    # --------------------------------------------------------
    private static $DATABASE = "confbuster";
    private static $IP       = "localhost";
    private static $PORT     = "3306";
    private static $USER     = "***";
    private static $PASSWORD = "***";
    private static $ENCODING = array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8');

 
    # --------------------------------------------------------
    # public void ExecuteDatabaseNonQuery(string sqlNonQuery, array $params)
    # --------------------------------------------------------
    # Execute an INSERT, UPDATE or DELETE non query command on the database.
    # 
    #
    # Parameters :
    #   string sqlNonQuery : The insert, update or delete sql non query
    #    array params        : The parameters used for the non query. (needed for prepared statement) 
    #
    # Returns : 
    #   void 
    # --------------------------------------------------------
    public static function ExecuteDatabaseNonQuery($sqlNonQuery, $params)
    {
        try {
            $connect = new DatabaseConnection(DatabaseManager::$IP,
                                                DatabaseManager::$PORT,
                                                DatabaseManager::$USER,
                                              DatabaseManager::$PASSWORD,
                                                DatabaseManager::$DATABASE);

            $stmt = $connect->pdo->prepare($sqlNonQuery);
            $stmt->execute($params);
            
        } catch(Exeception $e) {
            print_r($stmt->errorInfo());
            print_r($e->getMessage());
            $stmt = null;

        } finally {
            # Makes sure the connection is closen
            try {
                if(!is_null($connect->pdo))
                    $connect->CloseDatabaseConnection();

            } catch(Exeception $e) {
                print_r($e->getMessage());
            }
        }
    }
    
    # --------------------------------------------------------
    # public void ExecuteDatabaseQuery(string sqlQuery)
    # --------------------------------------------------------
    # Execute a SELECT query command on the database.
    # 
    #
    # Parameters :
    #   string sqlQuery : The SELECT sql query
    #    array params     : The parameters used for the non query. (needed for prepared statement) 
    #
    # Returns : 
    #   array - A dictionnary (key/value) containing the result of the query. 
    # --------------------------------------------------------
    public static function ExecuteDatabaseQuery($sqlQuery, $params)
    {
        try {
            $connect = new DatabaseConnection(DatabaseManager::$IP,
                                                DatabaseManager::$PORT,
                                                DatabaseManager::$USER,
                                              DatabaseManager::$PASSWORD,
                                                DatabaseManager::$DATABASE);

            $stmt = $connect->pdo->prepare($sqlQuery);
            $stmt->execute($params);
            
        } catch(Exeception $e) {
            print_r($stmt->errorInfo());
            print_r($e->getMessage());
            $stmt = null;

        } finally {
            # Makes sure the connection is closen
            try {
                if(!is_null($connect->pdo))
                    $connect->CloseDatabaseConnection();

            } catch(Exeception $e) {
                print_r($e->getMessage());
            }
        }

        return $stmt->fetch();
    }
} 



# ============================================================
#  CLASS       : DatabaseQuickQueries
#  DESCRIPTION : Container class for all the database function
#                used by the ComputeServer.
# ============================================================
class DatabaseQuickQueries
{
    # --------------------------------------------------------
    #                Private Static attributes
    # --------------------------------------------------------
    # The compute server configuration should be on the first record of the compute server configuration table.
    private static $SERVER_ID = 1;
    

    # --------------------------------------------------------
    #                Public Static attributes
    # --------------------------------------------------------
    # The number convention is defined in the SQL file that was used to create the database.
    public static $PDB  = 1;
    public static $SDF  = 2;
    public static $MOL  = 3;
    public static $MOL2 = 4;


    # --------------------------------------------------------
    # public static int GetJobLimitPerUser()
    # --------------------------------------------------------
    # Gets the number of jobs the user can have in queue.
    # 
    #
    # Parameters :
    #   None
    #
    # Returns : 
    #   int - The limit of job a user can have in queue.
    # --------------------------------------------------------
    public static function GetJobLimitPerUser()
    {
        $sql = <<<SQL
SELECT jobLimitPerUser
FROM tblConfiguration_Queue
WHERE id = :id;
SQL;

        $params = array( 
            ':id' => DatabaseQuickQueries::$SERVER_ID
        );

        return DatabaseManager::ExecuteDatabaseQuery($sql, $params)['jobLimitPerUser'];
    }

    
    # --------------------------------------------------------
    # public static int CountUserJobsInQueue(string $email)
    # --------------------------------------------------------
    # Gets the number of jobs the user has currently in queue.
    # 
    #
    # Parameters :
    #   string $email : The user's email
    #
    # Returns : 
    #   int - The number of job in queue corresponding to the given email.
    # --------------------------------------------------------
    public static function CountUserJobsInQueue($email)
    {
        $sql = <<<SQL
SELECT COUNT(id)
FROM tblQueue
WHERE email = :email;
SQL;

        $params = array( 
            ':email' => $email
        );

        return DatabaseManager::ExecuteDatabaseQuery($sql, $params)['COUNT(id)'];
    }


    # --------------------------------------------------------
    # public static int GetNumberOfJobInQueue()
    # --------------------------------------------------------
    # Gets the number of jobs currently in queue.
    # 
    #
    # Parameters :
    #   None
    #
    # Returns : 
    #   int - The number of jobs in queue
    # --------------------------------------------------------
    public static function GetNumberOfJobInQueue()
    {
        $sql = <<<SQL
SELECT COUNT(*)
FROM tblQueue;
SQL;

        $params = array();

        return DatabaseManager::ExecuteDatabaseQuery($sql, $params)['COUNT(*)'];
    }


    # --------------------------------------------------------
    # public static void AddToQueue(ComputeJobTO $computeJobTO)
    # --------------------------------------------------------
    # Add the job to the queue.
    # 
    #
    # Parameters :
    #   ComputeJobTO $computeJobTO : The compute job information
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    public static function AddToQueue($computeJobTO)
    {
        // Extract the file extension
        $fileExtension = substr( $computeJobTO->fileName, strrpos($computeJobTO->fileName,'.') ); 
        
        // Get the type of the file according to the database convention (see the database creation script)
        $fileType = -1;
        switch ($fileExtension) 
        {
            case ".pdb":
                $fileType = 1;
            break;

            case ".sdf":
                $fileType = 2;
                break;

            case ".mol":
                $fileType = 3;
                break;

            case ".mol2":
                $fileType = 4;
                break;

            default:
                // The fileName was filtered already by the Web Server.
                // Therefore, the code should never reach this point.
                //
                // However, in the worst case, the file will be rejected on the Compute Server.
                $fileType = 1;    
                break;
        }

        // SQL query definition
        $sql = <<<SQL
INSERT INTO tblQueue (email,fileName,fileType,dataFile,submissionDateTime)
VALUES (:email,
        :fileName,
        :fileType,
        :dataFile,
        NOW()      /* MySQL Build-in DateTime Function */
        );
SQL;

        // Parameters definition
        $params = array(
            ':email' => $computeJobTO->email,
            ':fileName' => $computeJobTO->fileName,
            ':fileType' => $fileType,
            ':dataFile' => $computeJobTO->fileContent
        );

        // Send the query to the database
        DatabaseManager::ExecuteDatabaseNonQuery($sql, $params);
    }
}


// End DatabaseManager.php    
?>
