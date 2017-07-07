import sys

# save the current chessboard situation
def Save_ChessBoard(situation_matrix,filename):
    filepath = "resources//doc//" + filename
    fp = open(filepath,'w')
    for i in range(0,15):
        for j in range(0,15):
            if j != 14:
                fp.write( str(situation_matrix[i][j]) + ' ')
            else:
                fp.write(str(situation_matrix[i][j]) + '\n')
    fp.close()
    pass

# load the previous chessboard situation
def Load_ChessBoard(filename):
    filepath = "resources//doc//" + filename
    fp = open(filepath,'r')
    situation_matrix = [([0] * 15) for i in range(0, 15)]
    # read the number
    
    fp.close()
    return situation_matrix
    pass

