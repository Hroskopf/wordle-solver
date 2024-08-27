import pygame
from logic import WordLogic

interval = 10
length = 65
    
class Button:
    def __init__(self, pos_x, pos_y, width, height, on_click, text = "Button"):
        self.on_click = on_click
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        pygame.draw.rect(game_window, (220, 220, 220), self.rect)
        pygame.draw.rect(game_window, (150,150,150), self.rect, 2)
        font = pygame.font.Font(None, 25)
        text_surface = font.render(text, True, (0,0,0))
        game_window.blit(text_surface, (pos_x + 15, pos_y + 5))
    
    
    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.on_click()
            return True
        return False

class Label:
    def __init__(self, pos_x = 4 * interval + 5 * length, pos_y = 50, width = 500, height = 100):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    def show(self, text = "Label"):
        pygame.draw.rect(game_window, (255, 255, 255), self.rect)
        word_position = (self.pos_x + 75, self.pos_y)
        font = pygame.font.Font(None, 36) 
        word_surface = font.render(text, True, (0,0,0)) 
        game_window.blit(word_surface, word_position)
        
def show_next_word():
    next_word.show(logic.best_suggestions()[0] + f"({len(logic.candidates)})")

class Row:
    def __init__(self, pos_x, pos_y):
        self.block_colors = [(215, 215, 215), (255, 165, 0), (0, 255, 0)]
        self.current_colors = [0, 0, 0, 0, 0]
        self.text_color = (50, 50, 50)
        self.rects = []
        self.letters = ["", "", "", "", ""]
        self.current_letter = 0
        self.font = pygame.font.Font(None, 75)
        
        for i in range(5):
            self.rects.append(pygame.Rect(pos_x + (length + interval)*i, pos_y, length, length))
    
    def update(self):
        for i in range(len(self.rects)):
            rect = self.rects[i]
            pygame.draw.rect(game_window, self.block_colors[self.current_colors[i]], rect)
            pygame.draw.rect(game_window, (150,150,150), rect, 2)
            
            text_surface = self.font.render(self.letters[i], True, self.text_color)

            text_rect = text_surface.get_rect(center = (rect.x + rect.width/2, rect.y + rect.height//2))
            
            game_window.blit(text_surface, text_rect)
            
    def add_letter(self, c):
        if self.current_letter == len(self.letters):
            return
        self.letters[self.current_letter] = c
        self.current_letter += 1
        
    def erase_letter(self):
        if self.current_letter == 0:
            return
        self.current_letter -= 1
        self.letters[self.current_letter] = ''
        
    def submit_word(self):
        if self.current_letter < len(self.letters):
            return False
        else:
            logic.decrease_candidates(''.join(self.letters),tuple(self.current_colors))
            return True
    
    def click(self, mouse_pos):
        for i in range(len(self.rects)):
            if self.rects[i].collidepoint(mouse_pos):
                self.current_colors[i] = (self.current_colors[i] + 1) % 3

class Grid:
    def __init__(self, pos_x = 50, pos_y = 50):
        self.reset(pos_x, pos_y)
    
    def update(self):
        for i in self.rows:
            i.update()
    
    def add_letter(self, c):
        if self.current_row == len(self.rows):
            return
        self.rows[self.current_row].add_letter(c)
    
    def erase_letter(self):
        if self.current_row == len(self.rows):
            return
        self.rows[self.current_row].erase_letter()
        
    def submit_word(self):
        if self.current_row == len(self.rows):
            return
        if self.rows[self.current_row].submit_word():
            self.current_row += 1
            show_next_word()
            
    def click(self, mouse_pos):
        if self.current_row == len(self.rows):
            return
        self.rows[self.current_row].click(mouse_pos)
        
    def reset(self, pos_x = 50, pos_y = 50):
        self.rows = []
        self.current_row = 0
        show_next_word()
        for i in range(6):
            self.rows.append(Row(pos_x, pos_y + (length + interval)*i))
    
    def __repr__(self):
        r = ""
        for i in self.rows:
            r += str(i.letters)+ '\n'
        r += '\n'
        return r
    
def reset():
    logic.reset()
    grid.reset()
                   
    
pygame.init()

WINDOW_WIDTH = 300 + 4 * interval + 5*length
WINDOW_HEIGHT = 200 + 4 * interval + 5*length 

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Wordle solver')

game_window.fill((255, 255, 255))  

next_word = Label()
logic = WordLogic()
grid = Grid()


reset_button = Button(450, 465, 70, 25, reset, "reset")

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
                grid.submit_word()
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
            grid.click(mouse_pos)
                    
    
    grid.update()
    pygame.display.update()
    
    

pygame.quit()
