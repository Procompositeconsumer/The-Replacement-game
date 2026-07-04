import pygame
import sys

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Monkey Puzzle")

font = pygame.font.SysFont("arial", 24)

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (180,180,180)
GREEN = (80,200,80)
RED = (220,70,70)
BLUE = (80,120,255)
YELLOW = (240,220,60)

clock = pygame.time.Clock()

# -----------------------------
# Inventory
# -----------------------------
inventory = []
selected_item = None

message = "Find a key to unlock the door."

game_finished = False

# -----------------------------
# Objects
# -----------------------------

class Item:

    def __init__(self, name, rect, color):
        self.name = name
        self.rect = pygame.Rect(rect)
        self.color = color
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
            text = font.render(self.name, True, BLACK)
            screen.blit(text, (self.rect.x, self.rect.y-25))


class Door:

    def __init__(self):
        self.rect = pygame.Rect(650,180,150,250)
        self.locked = True

    def draw(self):
        color = RED if self.locked else GREEN
        pygame.draw.rect(screen,color,self.rect)

        txt = "Locked Door" if self.locked else "Open Door"
        screen.blit(font.render(txt,True,WHITE),
                    (self.rect.x+10,self.rect.y+100))


door = Door()

# Hidden key
key = Item("Key",(180,400,40,40),YELLOW)

# Rock covering key
rock = Item("Rock",(150,370,120,80),GRAY)

# Stick
stick = Item("Stick",(80,200,100,20),BLUE)

# -----------------------------
# Drawing
# -----------------------------

def draw_inventory():

    pygame.draw.rect(screen,(50,50,50),(0,520,900,80))

    screen.blit(font.render("Inventory:",True,WHITE),(20,540))

    x = 180

    for item in inventory:

        color = GREEN if selected_item == item else WHITE

        pygame.draw.rect(screen,color,(x,535,80,40),2)

        txt = font.render(item,True,color)
        screen.blit(txt,(x+5,542))

        x += 100


def inventory_click(pos):

    global selected_item

    x = 180

    for item in inventory:

        rect = pygame.Rect(x,535,80,40)

        if rect.collidepoint(pos):

            if selected_item == item:
                selected_item = None
            else:
                selected_item = item

        x += 100


# -----------------------------
# Main Loop
# -----------------------------

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()

            if pos[1] > 520:
                inventory_click(pos)
                continue

            # Pick up stick
            if stick.visible and stick.rect.collidepoint(pos):
                stick.visible = False
                inventory.append("Stick")
                message = "You picked up a stick."

            # Rock interaction
            elif rock.visible and rock.rect.collidepoint(pos):

                if selected_item == "Stick":
                    rock.visible = False
                    message = "You moved the rock!"
                else:
                    message = "The rock is too heavy."

            # Pick up key
            elif key.visible and not rock.visible and key.rect.collidepoint(pos):
                key.visible = False
                inventory.append("Key")
                message = "You found a key!"

            # Door
            elif door.rect.collidepoint(pos):

                if selected_item == "Key":
                    door.locked = False
                    game_finished = True
                    message = "Puzzle Solved!"
                else:
                    message = "The door is locked."

    screen.fill((210,230,255))

    pygame.draw.rect(screen,(130,90,40),(0,450,900,70))

    stick.draw()

    if rock.visible:
        rock.draw()

    if not rock.visible:
        key.draw()

    door.draw()

    draw_inventory()

    txt = font.render(message,True,BLACK)
    screen.blit(txt,(20,20))

    if game_finished:
        big = pygame.font.SysFont("arial",42)

        end = big.render("YOU SOLVED THE PUZZLE!",True,GREEN)

        screen.blit(end,(180,90))

    pygame.display.flip()
    clock.tick(60)