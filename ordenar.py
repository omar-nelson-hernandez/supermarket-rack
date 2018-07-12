#!/usr/bin/env python3

import datetime # Date for the log filename
import configparser
import csv
import glob # Use regular expression to iterate over contents of a folder
import os
import logging
import logging.config

######################################## Point2D ########################################

class Point2D( object ):

    def __init__( self, x, y ):
        self.x = x
        self.y = y

    def __repr__( self ):
        return "( %f, %f )" % ( self.x, self.y )

######################################## Article ########################################

class Article( object ):

    def __init__( self, iArticleId, strArticleName, dArea, p2dCenter, p2dUpperLeftCorner, p2dLowerRightCorner ):
        self.iArticleId          = iArticleId
        self.strArticleName      = strArticleName
        self.dArea               = dArea
        self.p2dCenter           = p2dCenter
        self.p2dUpperLeftCorner  = p2dUpperLeftCorner
        self.p2dLowerRightCorner = p2dLowerRightCorner

    def __repr__( self ):
        return "ArticleId [%s] ArticleName [%s] Area [%s] p2dCenter [%s] p2dUpperLeftCorner [%s] p2dLowerRightCorner [%s]" \
                % ( self.iArticleId, self.strArticleName, self.dArea, self.p2dCenter, self.p2dUpperLeftCorner, self.p2dLowerRightCorner )

    def get75pctHeightY( self ):
        return ( self.p2dCenter.y - ( self.p2dCenter.y - self.p2dUpperLeftCorner.y ) )

######################################## loadFile ########################################

def loadFile( file ):
    articles = list()
    logger.info( "======================================== Reading file... ========================================" )
    with open( file, newline = "" ) as inputFile:
        inputReader = csv.DictReader( inputFile,
                fieldnames = ("iArticleId", "strArticleName", "dArea", "dCenterX", "dCenterY", "dUpperLeftCornerX",
                "dUpperLeftCornerY", "dLowerRightCornerX", "dLowerRightCornerY"))
        for row in inputReader:
            if row[ "strArticleName" ] != "ANAQUEL":
                myArticle = Article( row[ "iArticleId" ]
                                    ,row[ "strArticleName" ]
                                    ,row[ "dArea" ]
                                    ,Point2D( float( row[ "dCenterX" ] ), float( row[ "dCenterY" ] ) )
                                    ,Point2D( float( row[ "dUpperLeftCornerX" ] ), float( row[ "dUpperLeftCornerY" ] ) )
                                    ,Point2D( float( row[ "dLowerRightCornerX" ] ), float( row[ "dLowerRightCornerY" ] ) )
                                    )
                logger.info( myArticle )
                articles.append( myArticle )
    return articles

######################################## orderRack ########################################

def orderRack( articleList ):
    logger.info( "======================================== Sorting... ========================================" )
    articleList.sort( key = lambda Article: Article.p2dLowerRightCorner.y, reverse = True )
    # Print the list of items after sorting
    for art in articleList:
        logger.info( art )
    logger.info( "======================================== Splitting... ========================================" )
    lShelves = list()
    # Loop until the list is completely empty
    while len( articleList ) > 0:
        # Grab the first item, it's the lowest, we use it to compare it to the others
        firstArticle = articleList[ 0 ]
        # Get a list of all the items below 75% of the height of the first item
        lShelf = [ article for article in articleList if article.p2dLowerRightCorner.y > firstArticle.get75pctHeightY() ]
        # Remove the items in the shelf from the item pool
        articleList = [ article for article in articleList if article not in lShelf ]
        # Order shelf
        lShelf.sort( key = lambda Article: Article.p2dCenter.x )
        # Put all shelves into an ordered list
        lShelves.insert( 0, lShelf )
    logger.info( "======================================== Finished. ========================================" )
    for repisa in lShelves:
        for articulo in repisa:
            logger.info( articulo )
    return lShelves

######################################## generateOutput ########################################

def generateOutput( rack, file ):
    logger.info( "======================================== Output %s ========================================", file )
    separator = ','
    output = list()
    isFirstArticle = True
    for repisa in rack:
        if isFirstArticle == True:
            isFirstArticle = False
        else:
            output.append( 'N' )
        for articulo in repisa:
            output.append( articulo.strArticleName )
    outString = separator.join( output )
    logger.info( outString )
    outfile = open( config[ "PATH" ][ "ORDENADO_DIR" ] + file, "w" )
    outfile.write( outString )
    outfile.close()

######################################## START MAIN ########################################

config = configparser.ConfigParser()
config.read( "config.ini" )

logging.config.fileConfig( "logging.conf" )
logger = logging.getLogger( "ordenar" )

logger.info( "Start" )

for file in glob.glob( config[ "PATH" ][ "OUTPUT_DIR" ] + "*.res" ):
    logger.info( "======================================== Processing %s ========================================", file )
    articles = loadFile( file )
    rack = orderRack( articles )
    filename = os.path.split( file )[1]
    fnameNewExt = os.path.splitext( filename )[0] + ".ord"
    generateOutput( rack, fnameNewExt )
    os.rename( file, config[ "PATH" ][ "OUTPUT_DIR_BAK" ] + filename )

logger.info( "End" )
