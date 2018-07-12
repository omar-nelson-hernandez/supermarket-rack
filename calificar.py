#!/usr/bin/env python3

import re # Regular expressions
import csv # Files are CSV
from levenshtein import iterative_levenshtein_weighted # Levensthein implementations
import configparser # Configuration file
import logging # Logging
import logging.config # Logging configuration files
import glob # Search files using regex
import os

######################################## START MAIN ########################################

config = configparser.ConfigParser()
config.read( "config.ini" )

logging.config.fileConfig( "logging.conf" )
logger = logging.getLogger( "calificar" )

logger.info( "Start" )

for file in glob.glob( config[ "PATH" ][ "ORDENADO_DIR" ] + "*.ord" ):
    logger.info( "======================================== Processing %s ========================================", file )

    # Getting rack template
    matchResult = re.search( "__.*__", file )
    if matchResult:
        rackTemplate = matchResult.group( 0 )
    else:
        logger.error( "No template keyword found for: %s", file )
        logger.info( "Skipping %s", file )
        continue

    # Find template or throw an error
    templatesDir = config[ "PATH" ][ "TEMPLATES_DIR" ]
    with open( templatesDir + rackTemplate + ".txt" ) as templateFile:
        templateCsvReader = csv.reader( templateFile )
        for row in templateCsvReader:
            templateContents = row
    # Read both files
    with open( file ) as rackFile:
        rackCsvReader = csv.reader( rackFile )
        for row in rackCsvReader:
            rackContents = row
    # Compare both files
    logger.debug( "RackContents: %s", rackContents )
    logger.debug( "TemplateContents: %s", templateContents )
    levRes = iterative_levenshtein_weighted( rackContents, templateContents )
    levResNormalized = levRes / len( templateContents )
    logger.debug( "Result from levenshtein: %f", levRes )
    logger.info( "Normalized result: %f", levResNormalized )
    # Write result in a new file
    filename = os.path.split( file )[1]
    fnameNewExt = os.path.splitext( filename )[0] + ".cal"
    outputFile = open( config[ "PATH" ][ "CALIFICADO_DIR" ] + fnameNewExt, "w" )
    outputFile.write( str( levResNormalized ) )
    outputFile.close()
    # Move processed item to bak
    os.rename( file, config[ "PATH" ][ "ORDENADO_DIR_BAK" ] + filename )

logger.info( "End" )
