import pygame as p
import chess
import Engine



width = height = 720 
boardDimensions = 8 
square_size = height//boardDimensions
max_fps = 60
Images = {}


#loading images / Load global dictionary

def load_image():
    pieces = ['wp','wR','wK','wQ','wN', 'wB','bp','bR','bK','bQ','bN', 'bB']
    for piece in pieces:
        Images[piece] =  p.transform.scale(p.image.load("Images/"+ piece +".png"),(square_size,square_size))


def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gamestart = Engine.GameState()
    validMoves = gamestart.getValidMove()
    madeMove = False #flag variable 

    print(gamestart.board)
    load_image()
    running = True
    squareSelect = () #Keeps track of users last click
    playerClick = [] # up to 3 elements keep track of player clicks, two tuples
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running == False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # mouse location
                col = location[0] // square_size
                row = location[1] // square_size
                if squareSelect == (row,col):
                    squareSelect = () #deseleect
                    playerClick = [] #clears user clicks
                else:
                    squareSelect = (row, col)
                    playerClick.append(squareSelect)
                if len(playerClick) == 2:
                    move = Engine.Move(playerClick[0], playerClick[1], gamestart.board)
                    print(move.getChessNotation())
                    for valid_move in validMoves:
                        if move == valid_move:
                            gamestart.makeMove(valid_move)
                            madeMove = True
                            squareSelect = () #resets user clicks 
                            playerClick = []
                    
                    if not madeMove:
                        playerClick = [squareSelect]
            #Key Handler 
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r: #restart the game 
                    pass
        if madeMove:
            validMoves = gamestart.getValidMove()
            madeMove = False

        drawGameState(screen,gamestart)
        clock.tick(max_fps)
        p.display.flip()


#Does all the graphics in the current game state

def drawGameState(screen, gamestart):
    drawBoard(screen)
    #for later adding piece highlights etc
    drawPieces(screen, gamestart.board)

#draw the chessboard
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(boardDimensions):
        for c in range(boardDimensions):
           color = colors[((r+c)%2)]
           p.draw.rect(screen,color,p.Rect(c*square_size, r*square_size, square_size, square_size))





#draws chess peices with current gamestate.Board
def drawPieces(screen, board):
    for row in range(boardDimensions):
        for columns in range(boardDimensions):
            piece = board[row][columns]
            if piece != ' ':
                screen.blit(Images[piece], p.Rect(columns*square_size, row*square_size, square_size, square_size))

#draws the piece promotion popout 
def drawPawnPromo(screen):
    dialog_width = 200
    dialog_height = 200
    dialog_surface = p.Surface((dialog_width,dialog_height))
    dialog_rect = dialog_surface.get_rect(center = (width//2, height//2))

    for i, piece in enumerate(['R','N','B','Q']):
        rect = Images[piece].get_rect(center=(dialog_width//2,dialog_height//len(['R','N','B','Q'])*(i+0.5)))
        dialog_surface.blit(Images[piece], rect)
    
    screen.blit(dialog_surface, dialog_rect)
    p.display.update()

    while True:
        for event in p.event.get():
            if even.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                if dialog_rect.collidepoint(mouse_pos):
                    piece_index = (mouse_pos[1] -  dialog_rect.y) // (dialog_height//len(['R','N','B','Q']))
                    return ['R','N','B','Q'][piece_index]
            elif event.type == p.QUIT:
                p.quit()
    
if __name__ == "__main__":
    main()




# main()