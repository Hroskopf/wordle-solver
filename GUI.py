import pygame
from logic import WordLogic

class Button:
    
    """
    A button class.
    
    Attributes:
    -----------
    on_click : function
        Function that is done when button clicked.
    rect : pygame.Rect
        A rectangle of a button.
    """
    
    def __init__(self, pos_x, pos_y, width, height, on_click, text = "Button"):#pos_x and pos_y are coordinates of the top left corner.
        self.on_click = on_click
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        pygame.draw.rect(game_window, (220, 220, 220), self.rect)
        pygame.draw.rect(game_window, (150,150,150), self.rect, 2)
        font = pygame.font.Font(None, 25)
        text_surface = font.render(text, True, (0,0,0))
        game_window.blit(text_surface, (pos_x + 15, pos_y + 5))
    
    
    def click(self, mouse_pos):
        
        """
        Checks whether the button is clicked and performs the on_click action.

        Parameters:
        -----------
        mouse_pos :  
            Position, where mouse clicks

        Returns:
        --------
        boolean
            True if action is done.
        """
        
        if self.rect.collidepoint(mouse_pos):
            self.on_click()
            return True
        return False

class Label:
    
    """
    A label class.
    
    Attributes:
    -----------
    rect : pygame.Rect
        A rectangle of a label.
    pos_x: int
        A x-coordinate of top left corner.
    pos_y: int
        A y-coordinate of top left corner.
    """
    
    def __init__(self, pos_x, pos_y, width, height):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.pos_x = pos_x
        self.pos_y = pos_y
            
    def show(self, text = "Label"):
        
        """
        Changes text on label to a given.

        Parameters:
        -----------
        text : string
            New text of a label.

        """
        
        pygame.draw.rect(game_window, WHITE, self.rect)
        word_position = (self.pos_x, self.pos_y)
        font = pygame.font.Font(None, 32) 
        word_surface = font.render(text, True, (0,0,0)) 
        game_window.blit(word_surface, word_position)

class Row:
    
    """
    Class which implements a row of squares for showing entered words.
    
    Attributes:
    -----------
    colors : list of tuples.
        Colors, corresponding to different types of letters.
    current_colors: list of ints
        A color numbers for each cell.
    rects: list of pygame.Rect
        A array of rectangles.
    letters: list of chars
        Letters, written on each cell.
    current_letter: int
        Number of first non-entered letter
    """
    
    def __init__(self, pos_x, pos_y):
        self.colors = [LIGHT_GREY, ORANGE, GREEN]
        self.current_colors = [0, 0, 0, 0, 0]
        self.rects = []
        self.letters = ["", "", "", "", ""]
        self.current_letter = 0
        self.current_row = False
        
        
        for i in range(5):
            self.rects.append(pygame.Rect(pos_x + (SIDE + INTERVAL)*i, pos_y, SIDE, SIDE))
    
    def update(self):
        
        """
        Shows an actual state of a row on screen.

        """
        for i in range(len(self.rects)):
            rect = self.rects[i]
            pygame.draw.rect(game_window, self.colors[self.current_colors[i]], rect)
            
            line_color = (150,150,150)
            if i == self.current_letter and self.current_row:
                line_color = DARK_GREY
            pygame.draw.rect(game_window, line_color, rect, 2)
            
            font = pygame.font.Font(None, 75)
            
            text_surface = font.render(self.letters[i], True, GREY)

            text_rect = text_surface.get_rect(center = (rect.x + rect.width/2, rect.y + rect.height//2))
            
            game_window.blit(text_surface, text_rect)
            
    def add_letter(self, c):
        
        """
        Enters a new letter.
        """
        
        if self.current_letter == len(self.letters):
            return
        self.letters[self.current_letter] = c
        self.current_letter += 1
        
    def erase_letter(self):
        
        """
        Erase the last letter.
        """
        
        if self.current_letter == 0:
            return
        self.current_letter -= 1
        self.letters[self.current_letter] = ''
        
    def submit_word(self):
        
        """
        Sumbits the entered word into a WordleLogic.

        Returns:
        --------
        boolean
            True if action is done.
        """
        
        if self.current_letter < len(self.letters):
            return False
        else:
            logic.update_candidates(''.join(self.letters), tuple(self.current_colors))
            return True
    
    def click(self, mouse_pos):
        
        """
        Checks whether mouse clicks on some cell and changes its color if so.

        Attributes:
        -----------
        mouse_pos :
            Position of a mouse when clicked.
        """
        
        for i in range(len(self.rects)):
            if self.rects[i].collidepoint(mouse_pos):
                self.current_colors[i] = (self.current_colors[i] + 1) % 3

    def change_current_row(self):
        self.current_row = not self.current_row
    
class Grid:
    
    """
    Class for a full grid. Consists of rows.
    
    Attributes:
    -----------
    rows : list of Rows
        All Rows shown on screen.
    current_row : int
        Number of a active row.
    """
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        pos_x = 50
        pos_y = 50
        self.rows = []
        self.current_row = 0
        change_suggestions_list()
        for i in range(6):
            self.rows.append(Row(pos_x, pos_y + (SIDE + INTERVAL)*i))
        self.rows[0].change_current_row()
    
    def update(self):
        """
        Updates each row.
        """
        for i in self.rows:
            i.update()
    
    def add_letter(self, c):
        """
        Adds letter to the current row.

        Attributes:
        -----------
        c : char
            A added letter.
        """
        if self.current_row == len(self.rows):
            return
        self.rows[self.current_row].add_letter(c)
    
    def erase_letter(self):
        """
        Erases last letter from the current row.
        
        """
        if self.current_row == len(self.rows):
            return
        self.rows[self.current_row].erase_letter()
        
    def submit_word(self):
        """
        Submits the word in current row and goes to next row.
        
        """
        if self.current_row == len(self.rows):
            return
        if self.rows[self.current_row].submit_word():
            self.rows[self.current_row].change_current_row()
            self.current_row += 1
            self.rows[self.current_row].change_current_row()
            change_suggestions_list()
            
    def click(self, mouse_pos):
        """
        Click on current row.
        Attributes:
        -----------
        mouse_pos : 
            A position of a click.
        """
        
        if self.current_row == len(self.rows):
            return
        self.rows[self.current_row].click(mouse_pos)
    
    
def change_suggestions_list():
    
    """
    Changes the text of labels with suggestions.
    """
    
    title.show(f"{logic.words_left()} words are left.")
    second_title.show("Best suggestions are:")
    
    if logic.words_left() == 0:
        second_title.show("Oops, smth went wrong:(")
    elif logic.words_left() == 1:
        title.show(f"1 word is left.")
        second_title.show("The unknown word is:")
        
    words = logic.best_suggestions()
    for i in range(len(suggestions_list)):
        suggestions_list[i].show(words[i] if i < len(words) else '')
        
def reset():
    logic.reset()
    grid.reset()

def submit():
    grid.submit_word()
           
                   
SIDE = 65 # Side of the squares
INTERVAL = 10 # distance between squares


WHITE = (255, 255, 255)
GREY = (50, 50, 50)
DARK_GREY = (10, 10, 10)
LIGHT_GREY = (215, 215, 215)
ORANGE = (255, 155, 41)
GREEN = (92, 255, 30)


WINDOW_WIDTH = 400 + 4 * INTERVAL + 5*SIDE
WINDOW_HEIGHT = 250 + 4 * INTERVAL + 5*SIDE 
    

pygame.init()

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wordle solver')

game_window.fill(WHITE)  


suggestions_list = [] # List of labels for suggested words
for i in range(10):
    suggestions_list.append(Label(4 * INTERVAL + 5 * SIDE + 100, 120 + 32 * i, 500, 50))
    
title = Label(4 * INTERVAL + 5 * SIDE + 100, 50, 500, 25)
second_title = Label(4 * INTERVAL + 5 * SIDE + 100, 75, 500, 50)

logic = WordLogic()
grid = Grid()


reset_button = Button(450, 500, 70, 27, reset, "reset")
submit_button = Button(450, 460, 127, 27, submit, "submit word")

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                reset()
            elif event.key == pygame.K_BACKSPACE:
                grid.erase_letter()
            elif event.key == pygame.K_RETURN:
                submit()
            else:
                try:
                    c = chr(event.key)
                    if c.isalpha():
                        c = c.upper()
                        grid.add_letter(c)
                except:
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            reset_button.click(mouse_pos)
            submit_button.click(mouse_pos)
            grid.click(mouse_pos)
                    
    
    grid.update()
    pygame.display.update()
    
    
pygame.quit()

