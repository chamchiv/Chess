#This class will run the game and store the user input 


class GameState:

    def __init__(self):
       self.board = [['']*8 for _ in range(8)]
       self.WhitetoMove = True
       self.movelog = []
       self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,'N': self.getKnightMoves, 
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, "K": self.getKingMoves}
       self.setup_board()
       self.WhiteKingLocation = (7,4)
       self.blackKingLocation = (0,4)
       self.inCheck = False 
       self.pins = []
       self.checks = []
       

    
   

    
    def setup_board(self):
        self.board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
        self.board[1] = ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp']
        self.board[6] = ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp']
        self.board[7] = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        for i in range(2, 6):
            self.board[i] = [' ']*8

    """
    Takes a move then executes the move, will not work for castling and en passant and promotion
    """
    def makeMove(self,Move):
         if self.board[Move.Startrow][Move.Startcol] != ' ':
            self.board[Move.Startrow][Move.Startcol] = ' '
            self.board[Move.endrow][Move.endcol] = Move.pieceMoved
            self.movelog.append(Move)
            self.WhitetoMove = not self.WhitetoMove
            #update the kings position 
            if Move.pieceMoved == "wK":
                self.WhiteKingLocation = (Move.endrow, Move.endcol)
            elif Move.pieceMoved == "bK":
                self.blackKingLocation = (Move.endrow, Move.endcol)

        # self.board[Move.Startrow][Move.Startcol] = " "
        # self.board[Move.endrow][Move.endcol] = Move.pieceMoved
        # self.movelog.append(Move)
        # self.WhitetoMove = not self.WhitetoMove  
    """
    Legal moves under check
    """   
    def getValidMove(self):
        # return self.getPossMove() #gets all possible move 
        moves = []
        self.inCheck, self.pins, self.checks = self.PinsAndChecks()
        if self.WhitetoMove:
            kingRow = self.WhiteKingLocation[0]
            kingCol = self.WhiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getPossMove()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                CheckingPiece = self.board[checkRow][checkCol]
                validSquares = []

                if CheckingPiece[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]* i, kingCol + check[3]* i)
                        validSquares.append(validSquare)
                        if validSquare[0] ==  checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endrow, moves[i].endcol) in validSquares:
                            moves.remove(moves[i])
            else:#Double Check
                    self.getKingMoves(kingRow,kingCol, moves)
        else:#if not in check then its all possible moves 
                moves = self.getPossMove()

        return moves



    """
    Legal Moves not under check
    """

    def getPossMove(self):
        moves = []
        for row in range(len(self.board)): #no of rows
            for col in range(len(self.board[row])):#no of cols in rows
                turn = self.board[row][col][0]
                if (turn == 'w' and self.WhitetoMove) or (turn =='b' and not self.WhitetoMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row,col,moves)
        return moves 
    #get all the pawn moves and add to list

    def getPawnMoves(self,row,col,moves):
        isPinned = False
        pinDir = ()
        for pin in self.pins:
            if pin[0] == row and pin[1] == col:
                isPinned = True 
                pinDir = (pin[2], pin[3])
                break
        if self.WhitetoMove:

            if self.board[row-1][col]==" ":
                if not isPinned or pinDir == (-1, 0):
                    moves.append(Move((row,col), (row-1,col), self.board))
                    if row == 6 and self.board[row-2][col] == " ":
                        moves.append(Move((row,col),(row-2,col),self.board))


            if col - 1 >= 0: #captures to the left
                if self.board[row-1][col-1][0] == 'b':
                    if not isPinned or pinDir == (-1, -1): # check if pinned from the left
                        moves.append(Move((row,col),(row-1,col-1),self.board))
            if col + 1 <= 7: #captures to the right 
                if self.board[row-1][col + 1][0] == 'b':
                    if not isPinned or pinDir == (-1, 1):#check if pinned from the right 
                        moves.append(Move((row,col),(row-1,col+1),self.board))
        else:
            if self.board[row+1][col]==" ":
                if not isPinned or pinDir == (1, 0):
                    moves.append(Move((row,col), (row+1,col), self.board))
                    if row == 1 and self.board[row+2][col] == " ":
                        moves.append(Move((row,col),(row+2,col),self.board))

            if col - 1 >= 0: #captures to the left
                if self.board[row+1][col-1][0] == 'w':
                    if not isPinned or pinDir == (1, -1): # check if pinned from the left
                        moves.append(Move((row,col),(row+1,col-1),self.board))
            if col + 1 <= 7: #captures to the right 
                if self.board[row+1][col + 1][0] == 'w':
                    if not isPinned or pinDir == (1, 1):#check if pinned from the right 
                        moves.append(Move((row,col),(row+1,col+1),self.board))
        # pawn promotions


    #get all the rook moves and add to list
    def getRookMoves(self, row, col, moves):
     directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
     enemyColor = 'b' if self.WhitetoMove else 'w'
     isPinned = False
     pinDir = ()
     for pin in self.pins:
            if pin[0] == row and pin[1] == col:
                isPinned = True 
                pinDir = (pin[2], pin[3])
                break
     for d in directions:
         for i in range(1,8):
             endRow = row + d[0] * i 
             endCol = col + d[1] * i
             if 0<= endRow < 8 and 0 <= endCol < 8:
                if not isPinned  or d == pinDir or pinDir == (-d[0], -d[1]):
                 endPiece = self.board[endRow][endCol]
                 if endPiece == ' ':
                     moves.append(Move((row,col),(endRow,endCol), self.board))
                 elif endPiece[0] == enemyColor:
                     moves.append(Move((row,col),(endRow,endCol),self.board))
                     break
                 else:
                     break
             else:
                 break
    
    def getBishopMoves(self,row,col,moves):
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        enemyColor = 'b' if self.WhitetoMove else 'w'
        isPinned = False
        pinDir = ()
        for pin in self.pins:
            if pin[0] == row and pin[1] == col:
                isPinned = True 
                pinDir = (pin[2], pin[3])
                break
        for d in directions:
         for i in range(1,8):
             endRow = row + d[0] * i 
             endCol = col + d[1] * i
             if 0<= endRow < 8 and 0 <= endCol < 8:
                if not isPinned  or d == pinDir:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == ' ':
                        moves.append(Move((row,col),(endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.board))
                        break
                    else:
                        break
             else:
                 break
    def getKnightMoves(self,row,col,moves):
        Knightmoves = ((2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1))
        allyColor = 'w' if self.WhitetoMove else 'b'
        for pin in self.pins:
            if pin[0] == row and pin[1] == col: # if the knight is pinned, return
                return

        for d in Knightmoves:
             endRow = row + d[0] 
             endCol = col + d[1] 
             if 0<= endRow < 8 and 0 <= endCol < 8:
                 endPiece = self.board[endRow][endCol]
                 if endPiece[0] != allyColor:
                     moves.append(Move((row,col),(endRow,endCol),self.board))

    def getQueenMoves(self,row,col,moves):
        self.getRookMoves(row,col,moves)
        self.getBishopMoves(row,col,moves)

    def getKingMoves(self,row,col,moves):
        kingMoves = [(1, 0), (-1, 0), (0, 1), (0, -1),
                     (1, 1), (-1, -1), (1, -1), (-1, 1)]
        allyColor = 'w' if self.WhitetoMove else 'b'
        
        for d in kingMoves:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol] 
                if endPiece[0] != allyColor:
                    #Temporarily move the king
                    if self.WhitetoMove:
                        self.WhiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow , endCol)
                    
                    inCheck, pins, checks = self.PinsAndChecks()
                    
                    #place the king back to initial square
                    if self.WhitetoMove:
                        self.WhiteKingLocation =  (row, col)
                    else:
                        self.blackKingLocation = (row,col)
                    
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

    def PinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.WhitetoMove:
            enemyColor = 'b'
            allycolor = 'w'
            startRow = self.WhiteKingLocation[0]
            startCol = self.WhiteKingLocation[1]
        else:
            enemyColor = 'w'
            allycolor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direction)):
            d = direction[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endcol = startCol + d[1] * i
                if 0<= endRow < 8 and 0<= endcol < 8:
                    endPiece = self.board[endRow][endcol]
                    if endPiece[0] == allycolor and endPiece[1] != 'K':
                        if possiblePin == (): # if there is no pinned piece we add  the first allied piece that could be pinned
                            possiblePin = (endRow, endcol, d[0], d[1])
                        else:# if there is another allied piece inbetween then no pin
                            break
                    elif endPiece [0] == enemyColor:
                        type = endPiece[1]
                        #Diagonal attack 
                        #Straight attack 
                        #Pawn attack 
                        #empty pin 
                        #???
                        if (0 <= j and type == 'R') or (4 <= j and type == 'B') or \
                           (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <=7) or(enemyColor == 'b' and 4 <= j <=5))) or \
                           (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True 
                                checks.append((endRow, endcol, d[0], d[1]))
                                break
                            else:#piece blocking the pin
                                pins.append(possiblePin)
                                break
                        else: #no checks]
                            break
                else:
                    break #board not there


        knightMoves = ((2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1)) 
        for moves in knightMoves:
            endRow = startRow + moves[0]
            endCol = startCol + moves[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True 
                    checks.append((endRow,endCol, moves[0], moves[1]))

        return inCheck,pins, checks









class Move(GameState):
    
    rankToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v : k for k , v in rankToRows.items()}
    filestoCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v: k for k, v in filestoCols.items()}
    
    def __init__(self, startSq, endSq, board,promotionPiece=None):
        super().__init__()
        self.Startrow = startSq[0]
        self.Startcol = startSq[1]
        self.endrow = endSq[0]
        self.endcol = endSq[1]
        self.pieceMoved = board[self.Startrow][self.Startcol]
        self.pieceCapt = board[self.endrow][self.endcol]
        self.moveID = self.Startrow * 1000 + self.Startcol * 100 + self.endrow * 10 + self.endcol
        self.PromotionChoice = promotionPiece

        
    '''
    Overiding the equals method
    '''
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        

    def getChessNotation(self):
        return self.getRankFile(self.Startrow, self.Startcol) + self.getRankFile(self.endrow, self.endcol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    






"""
Classes of Chess pieces
"""

# class Piece(Move):
#     def __init__(self, color,r,c,moves):
#         self.color = color
    
#     def get_valid_moves(self, board, start_row, start_col):
#         pass

# class Pawn(Piece):
#     def get_valid_moves(self, board, start_row, start_col):
#         if self.WhitetoMove:
#             if self.board[start_row -1][start_col] == ' ':
                


# class Rook(Piece):
#     def get_valid_moves(self, board, start_row, start_col):
#         # Logic to calculate valid moves for a rook
#         pass


# class Knight(Piece):
#     def get_valid_moves(self, board, start_row, start_col):
#         # Logic to calculate valid moves for a knight
#         pass


# class Bishop(Piece):
#     def get_valid_moves(self, board, start_row, start_col):
#         # Logic to calculate valid moves for a bishop
#         pass


# class Queen(Piece):
#     def get_valid_moves(self, board, start_row, start_col):
#         # Logic to calculate valid moves for a queen
#         pass


# class King(Piece):
#     def get_valid_moves(self, board, start_row, start_col):
#         # Logic to calculate valid moves for a king
#         pass
