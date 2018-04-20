#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : DatabaseManager.py
# DESCRIPTION : See classes description.
# CLASSES     : DatabaseConnection
#               DatabaseManager
#               DatabaseQuickQueries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================
# Configuration of the Compute server path
import sys
sys.path.insert(0, '/var/www/ConfBuster/ComputeServer')

# Other core dependency
import MySQLdb

# Server modules
from BusinessLayer.TransportObjects.ComputeJobTO import ComputeJobTO


# ============================================================
#  CLASS       : DatabaseConnection
#  DESCRIPTION : Database connection class for handling the 
#                database connectivity.
#  IMPORTANT   : This class is NOT static. 
# ============================================================
class DatabaseConnection:

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
    #   string user     : The connection user name
    #   string password : The connection password
    #   string database : The database name
    # --------------------------------------------------------
    def __init__(self, ip, user, password, database):
        self.ip = ip
        self.user = user
        self.password = password
        self.database = database
        self.connection = MySQLdb.connect(self.ip, self.user, self.password, self.database)
        self.cursor = self.connection.cursor()


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
    def CloseDatabaseConnection(self):
        self.connection.close()



# ============================================================
#  CLASS       : DatabaseManager
#  DESCRIPTION : Manager class for handling the database.
# ============================================================
class DatabaseManager:
        
    # --------------------------------------------------------
    #                Private Static attributes
    # --------------------------------------------------------
    __db_ip = "localhost"
    __db_user = "***"
    __db_password = "***"
    __db_database = "confbuster"


    # --------------------------------------------------------
    # public void ExecuteNonQuery(string sqlNonQuery)
    # --------------------------------------------------------
    # Execute an INSERT, UPDATE or DELETE non query command on the database.
    # 
    #
    # Parameters :
    #   string sqlNonQuery : The insert, update or delete sql non query
    #
    # Returns : 
    #   void 
    # --------------------------------------------------------
    @staticmethod
    def ExecuteNonQuery(sqlNonQuery):
        try:
            connect = DatabaseConnection(DatabaseManager.__db_ip,
                                         DatabaseManager.__db_user,
                                         DatabaseManager.__db_password,
                                         DatabaseManager.__db_database)
            connect.cursor.execute(sqlNonQuery)
            connect.connection.commit()

        except Exception as e: 
            print('An error occured while executing the command : '+ sqlNonQuery)
            print str(e)

        finally :
            # Makes sure the connection is closen
            try:
                connect.CloseDatabaseConnection()
            except Exception as e: 
                print('An error occured while closing the database connexion with the command : '+ sqlNonQuery)
                print str(e)


    # --------------------------------------------------------
    # public list ExecuteQuery(string sqlQuery)
    # --------------------------------------------------------
    # Execute a SELECT query command on the database.
    # 
    #
    # Parameters :
    #   string sqlQuery : The SELECT sql query
    #
    # Returns : 
    #   list - The selected data
    # --------------------------------------------------------
    @staticmethod
    def ExecuteQuery(sqlQuery):
        try:
            connect = DatabaseConnection(DatabaseManager.__db_ip,
                                         DatabaseManager.__db_user,
                                         DatabaseManager.__db_password,
                                         DatabaseManager.__db_database)
            connect.cursor.execute(sqlQuery)

            #Calls the query fetcher and returns the all rows in a list
            rowList = DatabaseManager.__QueryFetcher(connect.cursor)

        except Exception as e:
            print('An error occured while executing the command : '+ sqlQuery)
            print str(e)

        finally :
            # Makes sure the connection is closen
            try:
                connect.CloseDatabaseConnection()
            except Exception as e: 
                print('An error occured while closing the database connexion with the command : '+ sqlQuery)
                print str(e)

        return rowList


    # --------------------------------------------------------
    # private static void __QueryFetcher(cursor connectionCursor)
    # --------------------------------------------------------
    # Fetch each row of a SELECT query one by one.
    # 
    #
    # Parameters :
    #   string sqlQuery : The SELECT sql query
    #
    # Returns : 
    #   list - A list containing each row 
    # --------------------------------------------------------
    @staticmethod
    def __QueryFetcher(connectionCursor):

        #Extract the number of row
        number_of_rows = int(connectionCursor.rowcount)

        #Create an empty list
        rowList = list()

        #Fetch and add each row to the list
        for _ in range(number_of_rows):
            row = connectionCursor.fetchone()
            rowList.append( row )

        return rowList



# ============================================================
#  CLASS       : DatabaseQuickQueries
#  DESCRIPTION : Container class for all the database function
#                used by the ComputeServer.
# ============================================================
class DatabaseQuickQueries:

    # --------------------------------------------------------
    #                Private Static attributes
    # --------------------------------------------------------
    # The compute server configuration should be on the first record of the compute server configuration table.
    __serverID = int(1)
    

    # --------------------------------------------------------
    #                Public Static attributes
    # --------------------------------------------------------
    # The number convention is defined in the SQL file that was used to create the database.
    PDB  = int(1)
    SDF  = int(2)
    MOL  = int(3)
    MOL2 = int(4)
    


    # --------------------------------------------------------
    # public static void ConfigureComputeServer(int jobLimit)
    # --------------------------------------------------------
    # Configure the initial properties of the compute server.
    # 
    #
    # Parameters :
    #   string jobLimit : The limit of job that can be computed at the same time.
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def ConfigureComputeServer(jobLimit):
        sql = """\
UPDATE tblConfiguration_ComputeServer
SET jobComputeLimit = {}, jobInProcess = 0
WHERE id = {}
""" 
        sql = sql.format(jobLimit, DatabaseQuickQueries.__serverID)

        DatabaseManager.ExecuteNonQuery(sql)


    # --------------------------------------------------------
    # public static void ConfigureQueue(int jobLimit)
    # --------------------------------------------------------
    # Configure the initial properties of the queue.
    # 
    #
    # Parameters :
    #   string jobLimit : The limit of job that a user (ie. an email address)
    #                     can have at the same time the queue.
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def ConfigureQueue(jobLimit):
        sql = """\
UPDATE tblConfiguration_Queue
SET jobLimitPerUser = {}
WHERE id = {}
""" 
        sql = sql.format(jobLimit, DatabaseQuickQueries.__serverID)

        DatabaseManager.ExecuteNonQuery(sql)


    # --------------------------------------------------------
    # public static int GetNumberOfJobInProcess()
    # --------------------------------------------------------
    # Returns the number of jobs currently computed by the 
    # ConfBuster Compute Server.
    #
    # Parameters :
    #   None
    #
    # Returns : 
    #   int - The nomber of jobs in process
    # --------------------------------------------------------
    @staticmethod
    def GetNumberOfJobInProcess():
        sql = """\
SELECT jobInProcess 
FROM tblConfiguration_ComputeServer
WHERE id = {};
"""
        sql = sql.format(DatabaseQuickQueries.__serverID)

        # 1) Get the first element of the list
        # 2) Get the first element of the tuple
        # 3) Cast in integer
        return int( (DatabaseManager.ExecuteQuery(sql)[0])[0] )


    # --------------------------------------------------------
    # public static ComputeJobTO RetreiveOldestQueuedJob()
    # --------------------------------------------------------
    # Returns a computeJob Transport Object containing the
    # informations submitted by the user.
    #
    # Parameters :
    #   None
    #
    # Returns : 
    #   ComputeJobTO - The oldest job currently in queue
    #   None - If there is no job currently in queue
    # --------------------------------------------------------
    @staticmethod
    def RetreiveOldestQueuedJob():
        
        # Ends the function if there is no job in queue
        numberOfJobInQueue = DatabaseQuickQueries.GetNumberOfJobInQueue()
        if(numberOfJobInQueue == 0):
            return None


        # Encapsulate the lowest job ID into a transport object
        sql = """\
SELECT MIN(id),email,fileName,fileType,dataFile,submissionDateTime
FROM tblQueue;
"""
        # Create the transport object
        queryResult = DatabaseManager.ExecuteQuery(sql)       
        computeJobTO = ComputeJobTO(id                =int(queryResult[0][0]),
                                    email             =str(queryResult[0][1]),
                                    fileName          =str(queryResult[0][2]),
                                    fileType          =int(queryResult[0][3]),
                                    fileContent       =str(queryResult[0][4]),
                                    submissionDateTime=str(queryResult[0][5]))
        # Convertion for the input file extension
        if(computeJobTO.fileType == DatabaseQuickQueries.PDB):
            computeJobTO.fileType = "pdb" 
        elif(computeJobTO.fileType == DatabaseQuickQueries.SDF):
            computeJobTO.fileType = "sdf" 
        elif(computeJobTO.fileType == DatabaseQuickQueries.MOL):
            computeJobTO.fileType = "mol" 
        elif(computeJobTO.fileType == DatabaseQuickQueries.MOL2):
            computeJobTO.fileType = "mol2" 
        else:
            computeJobTO.fileType = "mol2" # This line should never be executed. If so, the file will simply be rejected during the compute process.

        # Return the transport object
        return computeJobTO


    # --------------------------------------------------------
    # public static int GetNumberOfJobInQueue()
    # --------------------------------------------------------
    # Returns the number of jobs currently in queue.
    #
    # Parameters :
    #   None
    #
    # Returns : 
    #   int - The nomber of jobs in queue
    # --------------------------------------------------------
    @staticmethod
    def GetNumberOfJobInQueue():
        sql = """\
SELECT COUNT(*) 
FROM tblQueue;
"""
        return int( (DatabaseManager.ExecuteQuery(sql)[0])[0] )


    # --------------------------------------------------------
    # public static void RemoveJobFromQueue(int jobId)
    # --------------------------------------------------------
    # Remove a job from the queue
    # 
    # Parameters :
    #   int jobId : The id corresponding to the compute job (idQueue)
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def RemoveJobFromQueue(jobId):
        sql = """\
DELETE FROM tblQueue
WHERE id = {}
""" 
        sql = sql.format(jobId)
        DatabaseManager.ExecuteNonQuery(sql)


    # --------------------------------------------------------
    # public static void IncrementNumberOfJobInProcess()
    # --------------------------------------------------------
    # Augment by 1 the number of job currently in process.
    # 
    # Parameters :
    #   None
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def IncrementNumberOfJobInProcess():

        nbJob = DatabaseQuickQueries.GetNumberOfJobInProcess()
        nbJob = nbJob + 1

        sql = """\
UPDATE tblConfiguration_ComputeServer
SET jobInProcess = {}
WHERE id = {}
""" 
        sql = sql.format(nbJob, 
                         DatabaseQuickQueries.__serverID)

        DatabaseManager.ExecuteNonQuery(sql)


    # --------------------------------------------------------
    # public static void DecrementNumberOfJobInProcess()
    # --------------------------------------------------------
    # Reduce by 1 the number of job currently in process.
    # 
    # Parameters :
    #   None
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def DecrementNumberOfJobInProcess():

        nbJob = DatabaseQuickQueries.GetNumberOfJobInProcess()
        nbJob = nbJob - 1
        
        # Prevent the number of job to fall under 0
        if(nbJob < 0):
            nbJob = 0

        sql = """\
UPDATE tblConfiguration_ComputeServer
SET jobInProcess = {}
WHERE id = {}
""" 
        sql = sql.format(nbJob, 
                         DatabaseQuickQueries.__serverID)
                         
        DatabaseManager.ExecuteNonQuery(sql)


# End DatabaseManager.py