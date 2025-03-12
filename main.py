import pygame
import time
import math
from util import scale_images, blit_rotate_center

#Define and append to required scale the 2D racing game images
grass = scale_images(pygame.image.load("game_images/grass.jpg"), 2.5)
track = scale_images(pygame.image.load("game_images/track.png"), 0.9)

track_border = scale_images(pygame.image.load("game_images/track-border.png"), 0.9)
track_border_mask = pygame.mask.from_surface(track_border)
#variable track_border_mask for identifying area covered by track border

finish_line = pygame.image.load("game_images/finish.png")
finish_line_mask = pygame.mask.from_surface(finish_line)
finish_position = (130, 250)

purple_car = scale_images(pygame.image.load("game_images/purple-car.png"), 0.55)
green_car = scale_images(pygame.image.load("game_images/green-car.png"), 0.55)
red_car = scale_images(pygame.image.load("game_images/red-car.png"), 0.55)
grey_car = scale_images(pygame.image.load("game_images/grey-car.png"), 0.55)
white_car = scale_images(pygame.image.load("game_images/white-car.png"), 0.55)

# Define game window dimensions
window_width, window_height = track.get_width(), track.get_height()

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("2D Racing Game!")

#Define the car object which will be used for the player car instances.
class Car:
    def __init__(self, max_velocity, rotation_velocity):
        self.img = self.IMG
        self.max_velocity = max_velocity
        self.velocity = 0
        self.rotation_velocity = rotation_velocity
        self.angle = 0
        self.x, self.y = self.starting_position
        self.acceleration = 0.1
    
    # Allow user to change direction either left or right.
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity
    
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
    
    def forward_movement(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.move()


    def backward_movement(self):
        self.velocity = max(self.velocity - self.acceleration, -self.max_velocity/2) # the negative velocity is divided by two to ensure maximum backwards velocity cannot be more than half of the frontwards acceleration
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        #The vertical and horizontal move according to the hypotenous (cos(radians) and sin(radians))

        self.x -= horizontal
        self.y -= vertical

    def collision(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        #offset is the distance from the car's mask to the mask being passed as a parameter/argument(track border mask).
        collision_point = mask.overlap(car_mask, offset)
        return collision_point
    
    def restart(self):
        self.x, self.y = self.starting_position
        self.velocity = 0
        self.angle = 0
    

class PlayerCar(Car):
    IMG = purple_car
    starting_position = (180, 200)

    #Function to reduce the car's speed when user stops moving. 
    def reduce_speed(self):
        self.velocity = max(self.velocity - self.acceleration/2, 0)
        self.move()
    
    def track_border_collision(self):
        self.velocity = -self.velocity
        self.move()

#Append and draw the images
def draw(win, images, player_car):
    for image, position in images:
        win.blit(image, position)

    player_car.draw(win)
    pygame.display.update()

def player_movement(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    #Variable move is set to identify whether the user is pressing the move button

    if keys[pygame.K_LEFT]: 
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.forward_movement()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.backward_movement()
    
    if not moved:
        player_car.reduce_speed()
    #When car stops being pressed forwards, its speed starts decelerating
    
    
run = True
clock = pygame.time.Clock()
frames_per_second = 60
images = [(grass, (0, 0)), (track, (0, 0)), (finish_line, finish_position), (track_border, (0, 0))]
player_car = PlayerCar(6, 6) #Passing max velocity and rotation velocity


while run:
    #Manage game's speed for each computer to 60 frames per second
    clock.tick(frames_per_second)

    # draw the game's images and objects
    draw(window, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    player_movement(player_car)

    if player_car.collision(track_border_mask) != None:
        player_car.track_border_collision()
    
    # Check if player car collides with finish line before finishing race(by moving backwards) and reverse its direction if it does.
    finish_collision = player_car.collision(finish_line_mask, *finish_position)
    if finish_collision != None:
        if finish_collision[1] == 0:
            player_car.track_border_collision()
        elif finish_collision[1] <= 1:
            print("Congratulations, you finished the race.")
            player_car.restart()
       
pygame.quit()