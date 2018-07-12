#!/usr/bin/env python3

def iterative_levenshtein_weighted( pSource = [], pTarget = [], pCosts=( 1, 1 ,1 ) ):
    # Print input parameters
    print( "pSource: ", pSource )
    print( "pTarget: ", pTarget )
    print( "pCosts: ", pCosts )

    # Save sizes for distance matrix
    # Save operation costs
    rows = len( pSource ) + 1
    cols = len( pTarget ) + 1
    delCost, insCost, replCost = pCosts

    # Generate distance matrix
    distMatrix = [ [ 0 for x in range( cols ) ] for x in range( rows ) ]

    # Source can be transformed into empty strings through deletions
    for row in range( 1, rows ):
        distMatrix[ row ][ 0 ] = row * delCost

    # Target can be created from an empty string through insertions
    for col in range( 1, cols ):
        distMatrix[ 0 ][ col ] = col * insCost

    # Compute distance
    for col in range( 1, cols ):
        for row in range( 1, rows):
            if pSource[ row - 1 ] == pTarget [ col - 1 ]:
                opCost = 0
            else:
                opCost = replCost
            distMatrix[ row ][ col ] = min( distMatrix[ row - 1 ][ col ] + delCost,
                                            distMatrix[ row ][ col - 1 ] + insCost,
                                            distMatrix[ row - 1 ][ col - 1] + opCost)

    return distMatrix[ row ][ col ]
