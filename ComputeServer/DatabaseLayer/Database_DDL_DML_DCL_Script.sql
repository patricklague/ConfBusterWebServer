-- ======================================================
-- AUTHOR      : GABRIEL BÉGIN
-- FILE        : Database_DDL_DML_DCL_Script.sql
-- DESCRIPTION : Database creation/initialization script.
-- ======================================================


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--              DDL
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE DATABASE confbuster CHARACTER SET utf8;
USE confbuster;


/*
 *  Table for the job submission.
 *
 * 
 *  Numeric code of all the supported file type :
 *  1 = PDB
 *  2 = SDF
 *  3 = MOL
 *  4 = MOL2
 */
CREATE TABLE tblQueue
(
    id INT (11) UNSIGNED NOT NULL AUTO_INCREMENT,

    email VARCHAR(50) DEFAULT NULL,
    fileName VARCHAR(50) DEFAULT NULL,                  -- The file name with its extension (ie. "Macrocyle.mol2" and not "Macrocycle")
    fileType INT (11) DEFAULT NULL,                     -- The number associated to the file type
    dataFile MEDIUMTEXT DEFAULT NULL,

    submissionDateTime DATETIME DEFAULT NULL,
    
    spare1 VARCHAR(50) DEFAULT NULL,
    spare2 VARCHAR(50) DEFAULT NULL,
    spare3 VARCHAR(50) DEFAULT NULL,
    spare4 VARCHAR(50) DEFAULT NULL,
    spare5 VARCHAR(50) DEFAULT NULL,

    PRIMARY KEY (id)
);

/* 
 * Configuration for the compute server responsible of managing the queue.
 *
 * Note : This table will contain only one field since there is only one server.
 */
CREATE TABLE tblConfiguration_ComputeServer
(
    id INT (11) UNSIGNED NOT NULL AUTO_INCREMENT,

    jobComputeLimit INT (11) UNSIGNED DEFAULT 1,        -- The quantity of job that can be computed at the same time. Must be at least : 1
    jobInProcess INT (11) UNSIGNED DEFAULT 0,           -- The quantity of job currently in process

    spare1 VARCHAR(50) DEFAULT NULL,
    spare2 VARCHAR(50) DEFAULT NULL,
    spare3 VARCHAR(50) DEFAULT NULL,
    spare4 VARCHAR(50) DEFAULT NULL,
    spare5 VARCHAR(50) DEFAULT NULL,

    PRIMARY KEY (id)
);

/* 
 * Configuration for the queue itself.
 *
 * Note : This table will contain only one field since there is only one queue.
 */
CREATE TABLE tblConfiguration_Queue
(
    id INT (11) UNSIGNED NOT NULL AUTO_INCREMENT,

    jobLimitPerUser INT (11) UNSIGNED DEFAULT 1,        -- The quantity of job that can be hold in queue for a user's email. Must be at least : 1

    spare1 VARCHAR(50) DEFAULT NULL,
    spare2 VARCHAR(50) DEFAULT NULL,
    spare3 VARCHAR(50) DEFAULT NULL,
    spare4 VARCHAR(50) DEFAULT NULL,
    spare5 VARCHAR(50) DEFAULT NULL,

    PRIMARY KEY (id)
);



-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--              DML
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- Insertion of the unique server configuration record
INSERT INTO tblConfiguration_ComputeServer (id) VALUES (1);
-- Insertion of the unique queue configuration record
INSERT INTO tblConfiguration_Queue (id) VALUES (1);



-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--              DCL
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-- Create a user to allow the ComputeServer to access to the database located on the same computer.
-- The credential of the user has to be configured here.
CREATE USER '******'@'localhost' IDENTIFIED BY '******';
GRANT ALL PRIVILEGES ON confbuster.* TO '******'@'localhost';
FLUSH PRIVILEGES;


-- End Database_DDL_DML_DCL_Script.sql