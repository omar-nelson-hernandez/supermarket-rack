#!/usr/bin/env python3

import logging
import os
import datetime
import configparser

class fileProcessFileHandler( logging.FileHandler ):

    def __init__( self, pLogOwner ):

        config = configparser.ConfigParser()
        config.read( "config.ini" )

        logDir = config[ "PATH" ][ "LOG_DIR" ]
        timestamp = datetime.datetime.now().strftime( "%Y-%m-%d_%H-%M-%S" )
        logPid = str( os.getpid() )

        fname = logDir + pLogOwner + "."  + timestamp + "." + str( os.getpid() ) + ".log"
        super( fileProcessFileHandler, self ).__init__( fname, "w" )

class fileGlobalFileHandler( logging.FileHandler ):

    def __init__( self ):

        config = configparser.ConfigParser()
        config.read( "config.ini" )

        logDir = config[ "PATH" ][ "LOG_DIR" ]
        logOwner = "global"
        timestamp = datetime.datetime.now().strftime( "%Y-%m-%d_%H-%M-%S" )
        logPid = str( os.getpid() )
        timestamp = datetime.datetime.now().strftime( "%Y-%m-%d_%H-%M-%S" )

        fname = logDir + logOwner + "."  + timestamp + "." + str( os.getpid() ) + ".log"
        super( fileGlobalFileHandler, self ).__init__( fname, "w" )
