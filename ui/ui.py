import pygame
from engine.GameState import GameState as gs
from engine.Move import Move
from .scenes import Button, SimpleScene, HelpScene, ChooseScene, ChooseBot

# WIDTH = 640
# HEIGHT = 480
WIDTH = 832
# HEIGHT = 512
HEIGHT = 640

B_WIDTH = B_HEIGHT = 512  # board_width and board_height
DIMENSION = 8
SQ_SIZE = B_HEIGHT // DIMENSION  # square_size
HEIGHT_BOX = 50
WIDTH_BOX = 400
NUMBER_DEPTH = 4
WIDTH_PER_BOX = WIDTH_BOX // NUMBER_DEPTH
IMAGES = {}

def load_images():
        pieces = ['W', 'B']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(
                pygame.image.load("ui/image/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
            )

class ChessboardScene:
    def __init__(self, title, gs):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(pygame.Color("beige"))  # Fill background with beige color
        bg = pygame.transform.scale(pygame.image.load("UI/image/bg.png"), (B_WIDTH, B_HEIGHT))
        self.background.blit(bg, ((WIDTH - B_WIDTH) // 2 - 64, (HEIGHT - B_HEIGHT) // 2))  # Adjusted position
        self.title = title
        self.gs = gs

    def draw(self, screen):
        # Display the game state on the screen
        font = pygame.font.Font(None, 36)
        text = font.render(self.title, True, (255, 255, 255))
        screen.blit(text, (10, 10))
        board = self.gs.board

        load_images()
        # Draw the chessboard
        colors = [pygame.Color("dark green"), pygame.Color("dark green")]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[((r + c) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect((c * SQ_SIZE) + ((WIDTH - B_WIDTH) // 2) - 64,
                                                            (r * SQ_SIZE) + (HEIGHT - B_HEIGHT) // 2, SQ_SIZE, SQ_SIZE))  # Adjusted position

        # Draw grid lines
        for r in range(DIMENSION):  # Horizontal lines
            pygame.draw.line(screen, pygame.Color("black"),
                             ((WIDTH - B_WIDTH) // 2 - 64, r * SQ_SIZE + (HEIGHT - B_HEIGHT) // 2), (
                             (WIDTH - B_WIDTH) // 2 - 64 + B_WIDTH,
                             r * SQ_SIZE + (HEIGHT - B_HEIGHT) // 2))  # Adjusted position
            # Add row coordinates
            row_text = font.render(str(r + 1), True, pygame.Color("black"))
            screen.blit(row_text, ((WIDTH - B_WIDTH) // 2 - 100, r * SQ_SIZE + (HEIGHT - B_HEIGHT) // 2 + SQ_SIZE // 2))

        for c in range(DIMENSION):  # Vertical lines
            pygame.draw.line(screen, pygame.Color("black"),
                             (c * SQ_SIZE + ((WIDTH - B_WIDTH) // 2) - 64, (HEIGHT - B_HEIGHT) // 2), (
                             c * SQ_SIZE + ((WIDTH - B_WIDTH) // 2) - 64,
                             (HEIGHT - B_HEIGHT) // 2 + B_HEIGHT))  # Adjusted position
            # Add column coordinates
            col_text = font.render(chr(ord('a') + c), True, pygame.Color("black"))
            screen.blit(col_text, (
            c * SQ_SIZE + ((WIDTH - B_WIDTH) // 2) - 64 + SQ_SIZE // 2, (HEIGHT - B_HEIGHT) // 2 + B_HEIGHT))

        # Draw each piece of the chessboard
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                piece = board[r][c]
                if piece in IMAGES:  # Ensure the piece is in IMAGES dictionary
                    screen.blit(IMAGES[piece], pygame.Rect((c * SQ_SIZE) + ((WIDTH - B_WIDTH) // 2) - 64,
                                                           (r * SQ_SIZE) + (HEIGHT - B_HEIGHT) // 2, SQ_SIZE,
                                                           SQ_SIZE))  # Adjusted position


class ChessGUI:
    def __init__(self, gs):
        self.gs = gs
        self.selected_piece = None
        self.valid_moves = []
        self.running = True
        load_images()    

        # Create a ChessboardScene instance
        self.chessboard_scene = ChessboardScene("Chessboard", gs)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    self.handle_mouse_click()

    def handle_mouse_click(self):
        x, y = pygame.mouse.get_pos()
        row = (y - (HEIGHT - B_HEIGHT) // 2) // SQ_SIZE
        col = (x - ((WIDTH - B_WIDTH) // 2) + 64) // SQ_SIZE

        if 0 <= row < DIMENSION and 0 <= col < DIMENSION:
            if self.selected_piece:
                move = (row, col)
                if move in self.valid_moves:
                    self.make_move(move)
                    if not Move.get_valid_moves(self.gs):  # Check if the other player has valid moves
                        print("Game Over")
                        self.running = False
                else:
                    print("Move is invalid")
                self.selected_piece = None
                self.valid_moves = []
            else:
                self.select_piece(row, col)

    def select_piece(self, row, col):
        piece = self.gs.board[row][col]
        if piece == self.gs.current_player:
            self.selected_piece = (row, col)
            self.valid_moves = Move.get_valid_moves(self.gs)
            print(f"Valid moves: {self.valid_moves}")

    def make_move(self, move):
        Move.make_move(self.gs, move)
        self.selected_piece = None
        self.valid_moves = []


    def run_game(self, screen):
        self.running = True        
        while self.running:
            self.handle_events()
            self.draw_board(screen)
            self.highlight_valid_moves(screen)  # Highlight valid moves
            pygame.display.flip()
            if self.gs.is_game_over():
                print("Game over")
                self.running = False  # End the game loop when the game is over


    def highlight_valid_moves(self, screen):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.rect(screen, pygame.Color("light green"),
                             pygame.Rect((col * SQ_SIZE) + ((WIDTH - B_WIDTH) // 2) - 64,
                                         (row * SQ_SIZE) + (HEIGHT - B_HEIGHT) // 2, SQ_SIZE, SQ_SIZE))
            
    def draw_board(self, screen):
        # Call the draw method of ChessboardScene
        self.chessboard_scene.draw(screen)

class ChessHuman(ChessGUI):
    def human_handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    print("Mouse Clicked")
                    x, y = pygame.mouse.get_pos()
                    row = (y - (HEIGHT - B_HEIGHT) // 2) // SQ_SIZE
                    col = (x - ((WIDTH - B_WIDTH) // 2) + 64) // SQ_SIZE
                    print(f"Click position: ({x}, {y}), Board position: ({row}, {col})")
                    if 0 <= row < DIMENSION and 0 <= col < DIMENSION:
                        if self.selected_piece:
                            move = (row, col)
                            print(f"Selected piece at: {self.selected_piece}, Attempt move: {move}")
                            if move in self.valid_moves:
                                print("Move is valid")
                                Move.make_move(self.gs, move)
                                self.selected_piece = None
                                self.valid_moves = []

                                if not Move.get_valid_moves(self.gs):  # Check if the other player has valid moves
                                    print("Game Over")
                                    self.running = False

                            else:
                                print("Move is invalid")
                                self.selected_piece = None
                                self.valid_moves = []
                        else:
                            piece = self.gs.board[row][col]
                            print(f"Piece selected: {piece} at ({row}, {col})")
                            if piece == self.gs.current_player:  # If the clicked piece belongs to the current player
                                self.selected_piece = (row, col)
                                self.valid_moves = Move.get_valid_moves(self.gs)
                                print(f"Valid moves: {self.valid_moves}")
    


class GameOver:
    def __init__(self, game_state):
        self.game_state = game_state

    def draw(self, screen):
        winner = self.game_state.get_winner()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        winner = self.game_state.get_winner()
        if winner != 'Tie':
            text = font.render("Game over. Winner: " + winner, True, (255, 255, 255))
        else:
            text = font.render("Game over. It's a Tie!", True, (255, 255, 255))
        screen.blit(text, (10, 10))
