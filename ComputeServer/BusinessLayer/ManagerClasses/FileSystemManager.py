#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHOR      : GABRIEL BÉGIN
# FILE        : FileSystemManager.py
# DESCRIPTION : See class description.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============================================================
#                         DEPENDENCIES
# ============================================================
import os
import shutil


# ============================================================
#  CLASS       : FileSystemManager
#  DESCRIPTION : Manager class for using the file system.
# ============================================================
class FileSystemManager:

    # --------------------------------------------------------
    # public static void CreateDirectory(string directoryPath)
    # --------------------------------------------------------
    # Create a directory to the specified path.
    #
    # Parameters :
    #   string directoryPath : The path with the directory name (ie. /path/NewDirectoryName)
    # 
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def CreateDirectory(directoryPath):
        try:
            #Verify if the directory exist before creating it
            if not os.path.exists(directoryPath):
                os.makedirs(directoryPath)

        except Exception, e:
            print('An error happended upon creation of the directory :'+ ' ' + directoryPath)
            print('%s' % e)


    # --------------------------------------------------------
    # public static void DeleteDirectory(string directoryPath)
    # --------------------------------------------------------
    # Delete a directory to the specified path.
    #
    # Parameters :
    #   string directoryPath : The path with the directory name (ie. /path/NewDirectoryName)
    # 
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def DeleteDirectory(directoryPath):
        try:
            shutil.rmtree(directoryPath)

        except Exception, e:
            print('An error happended upon deletion of the directory :'+ ' ' + directoryPath)
            print('%s' % e)


    # --------------------------------------------------------
    # public static void WriteFile(string filePath, string content)
    # --------------------------------------------------------
    # Write a new file, erase the content of an existing one.
    #
    # Parameters :
    #   string filePath : The path of the file (ie. /path/NewFile.txt)
    #   string content  : The text content of the file
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def WriteFile(filePath, content):
        try:
            f = open(filePath, "w")
            f.write(content)
            f.close()    
        except Exception, e:
            print('An error happended upon writing the file :'+ ' ' + filePath)
            print('%s' % e)
    

    # --------------------------------------------------------
    # public static void AppendFile(string filePath, string content)
    # --------------------------------------------------------
    # Append text to the existing content of a file.
    #
    # Parameters :
    #   string filePath : The path of the file (ie. /path/NewFile.txt)
    #   string content  : The text to append to the file
    #
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def AppendFile(filePath, content):
        try:
            f = open(filePath, "a")
            f.write(content)
            f.close()    
        except Exception, e:
            print('An error happended upon appending to the file :'+ ' ' + filePath)
            print('%s' % e)
       
       
    # --------------------------------------------------------
    # public static array ReadFile(string filePath)
    # --------------------------------------------------------
    # Read the content of a file (in text mode).
    #
    # Parameters :
    #   string filePath : The path of the file (ie. /path/NewFile.txt)
    #   
    # Returns : 
    #   array fileContent  : A list containing each line of text
    # --------------------------------------------------------
    @staticmethod
    def ReadFile(filePath):
        try:
            f = open(filePath, "r")
            
            fileContent = list()
            
            for line in f :
                fileContent.append( line )
                
            f.close()    

        except Exception, e:
            print('An error happended upon reading the file :'+ ' ' + filePath)    
            print('%s' % e)

        return fileContent


    # --------------------------------------------------------
    # public static void MoveAllItems(string sourceDirectory, string destinationDirectory)
    # --------------------------------------------------------
    # Move all item from a directory to another.
    #
    # Parameters :
    #   string sourceDirectory      : The source directory path
    #   string destinationDirectory : The destination directory path
    #   
    # Returns : 
    #   void
    # --------------------------------------------------------
    @staticmethod
    def MoveAllItems(sourceDirectory, destinationDirectory):

        try:
            # List all the items in the source directory
            items = os.listdir(sourceDirectory) 

            # Move each item to the destination directory
            for item in items :

                # Configure the source directory with the item
                src = sourceDirectory + '/' + item 
                
                # Prevent moving a directory into itself
                if src != destinationDirectory :                          
                    os.system('mv -f' + ' ' + src + ' ' + destinationDirectory + "/")

        except Exception, e:
            print('An error happended upon moving all the content of '+ sourceDirectory + ' to ' + destinationDirectory)    
            print('%s' % e)


# End FileSystemManager.py