import pygame
import time
import math
from util import scale_images, blit_rotate_center
pygame.font.init()

#Define and append to required scale the 2D racing game images
grass = scale_images(pygame.image.load("game_images/grass.jpg"), 2.5)
track = scale_images(pygame.image.load("game_images/track.png"), 0.8)

track_border = scale_images(pygame.image.load("game_images/track-border.png"), 0.8)
track_border_mask = pygame.mask.from_surface(track_border)
#variable track_border_mask for identifying area covered by track border

finish_line = pygame.image.load("game_images/finish.png")
finish_line_mask = pygame.mask.from_surface(finish_line)
finish_position = (110, 230)

purple_car = scale_images(pygame.image.load("game_images/purple-car.png"), 0.40)
# green_car = scale_images(pygame.image.load("game_images/green-car.png"), 0.50)
red_car = scale_images(pygame.image.load("game_images/red-car.png"), 0.40)
# grey_car = scale_images(pygame.image.load("game_images/grey-car.png"), 0.50)
# white_car = scale_images(pygame.image.load("game_images/white-car.png"), 0.50)

# Define game window dimensions
window_width, window_height = track.get_width(), track.get_height()

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("2D Racing Game!")

font = pygame.font.SysFont("arial", 35, bold=True)

ai_car_path = [(154, 89), (53, 81), (50, 407), (290, 653), (378, 592), (369, 456), (510, 448), (535, 613), (633, 642), (649, 343), (375, 318), (375, 232), (625, 236), (654, 82), (266, 69), (236, 379), (134, 327), (152, 234)]
class Gameinfo:
    levels = 10
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.start_time = 0
        self.highest_score = None

    def next_level(self):
        self.level += 1
        self.started = False
    
    def reset(self):
        self.level = 1
        self.started = False
        self.start_time = 0
    
    def game_ended(self):
        return self.level > self.levels

    def start(self):
        if not self.started:
            self.started = True
            self.start_time = time.time()
    
    def get_time(self):
        if self.started:
            return round(time.time() - self.start_time)
        else:
            return 0
        
    def update_high_score(self):
        time_taken = self.get_time()
        if self.highest_score is None or time_taken < self.highest_score:
            self.highest_score = time_taken
    

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

        #The vertical and horizontal move according to the hypotenous and adjacent or opposite lines from the car's x and y pixel coordinates (cos(radians) and sin(radians)) - (SOH-CAH-TOA (sin(radians) = opposite/hypotenous and cos(radians) = adjacent/hypotenous)

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
    starting_position = (170, 190)

    #Function to reduce the car's speed when user stops moving. 
    def reduce_speed(self):
        self.velocity = max(self.velocity - self.acceleration/2, 0)
        self.move()
    
    def track_border_collision(self):
        self.velocity = -self.velocity
        self.move()

class AICar(Car):
    IMG = red_car
    starting_position = (150, 200)

    def __init__(self, max_velocity, rotation_velocity, path = []):
        super().__init__(max_velocity, rotation_velocity)
        self.path = path
        self.current_point = 0
        self.velocity = max_velocity
    
    #The draw_points function is needed to draw points on path
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)
    
    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point] 
        x_difference = target_x - self.x
        y_difference = target_y - self.y

        if y_difference == 0:
            angle = math.pi/2
        else:
            angle = math.atan(x_difference / y_difference)

        if target_y > self.y:
            angle += math.pi
        
        angle_difference = self.angle - math.degrees(angle)
        if angle_difference >= 180:
            angle_difference -= 360
        
        if angle_difference > 0:
            self.angle -= min(self.rotation_velocity, abs(angle_difference))
        else:
            self.angle += min(self.rotation_velocity, abs(angle_difference))
    
    def move_to_next_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        #Ensure movement to existing points

        self.calculate_angle()
        self.move_to_next_path_point() 
        super().move()

    def next_level(self, level):
        self.restart()
        self.velocity = self.max_velocity + (level - 1) * 0.2 #velocity of ai car increases by one after each level, but divided by two to lower its speed to make it beatable.
        self.current_point = 0


#Append and draw the images and texts
def draw(win, images, player_car, ai_car, game_info):
    for image, position in images:
        win.blit(image, position)
    
    level_text = font.render(f"Level: {game_info.level}", 1, (0, 0, 0))
    win.blit(level_text, (10, window_height - level_text.get_height() - 80))

    time_ellapsed = font.render(f"Time: {game_info.get_time()}s", 1, (0, 0, 0))
    win.blit(time_ellapsed, (10, window_height - time_ellapsed.get_height() - 50))

    highest_score_text =  "Best Time: --" if game_info.highest_score is None else f"Best Time: {game_info.highest_score}s"
    best_time = font.render(highest_score_text, 1, (0, 0, 0)) #Render text color and content
    win.blit(best_time, (10, window_height - best_time.get_height() - 20)) #Render text position on window

    player_car.draw(win)
    ai_car.draw(win)
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
        game_info.start()
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
player_car = PlayerCar(15, 9) #Passing max velocity and rotation velocity
ai_car = AICar(2, 9, ai_car_path) #Passing max velocity, rotation velocity, and the path the car will follow, which has been pre-selected
game_info = Gameinfo()

while run:
    #Manage game's speed for each computer to 60 frames per second
    clock.tick(frames_per_second)

    # draw the game's images and objects
    draw(window, images, player_car, ai_car, game_info)

    while not game_info.started:
        window.fill((200, 200, 200))  # Light grey background for better visibility
        
        start_message = font.render(f"Press any key to start Level {game_info.level}", True, (0, 0, 0))
        text_x = (window_width - start_message.get_width()) // 2
        text_y = (window_height - start_message.get_height()) // 2

        window.blit(start_message, (text_x, text_y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                #Introduce countdown before the game starts
                for count in range(3, 0, -1):
                    window.fill((200,200,200))
                    countdown_message = pygame.font.SysFont("arial", 80, bold=True).render(str(count), True, (255, 0, 0))    
                    countdown_x = (window_width - countdown_message.get_width()) // 2
                    countdown_y = (window_height - countdown_message.get_height()) // 2

                    window.blit(countdown_message, (countdown_x, countdown_y))
                    pygame.display.update()
                    pygame.time.delay(1000)
                
                game_info.start()
                break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            ai_car.path.append(pos)
    
    player_movement(player_car)
    ai_car.move()

    if player_car.collision(track_border_mask) != None:
        player_car.track_border_collision()
    
    # Check if player and ai car collides with finish line before finishing race(by moving backwards) and reverse its direction if it does.
    ai_car_collision = ai_car.collision(finish_line_mask, *finish_position)
    if ai_car_collision != None:
        if ai_car_collision[1] <= 1:
            losing_message = font.render(f"You Lost! Try again.", True, (0, 0, 0))
            text_x = (window_width - losing_message.get_width()) // 2
            text_y = (window_height - losing_message.get_height()) // 2

            window.blit(losing_message, (text_x, text_y))
            pygame.display.update()
            pygame.time.wait(3000)

            game_info.reset()
            player_car.restart()
            ai_car.restart() # Handle game end when ai_car wins
            

    finish_collision = player_car.collision(finish_line_mask, *finish_position)
    if finish_collision != None:
        if finish_collision[1] == 0:
            player_car.track_border_collision()
        elif finish_collision[1] <= 1:
            game_info.update_high_score()
            win_message = font.render(f"You Won! Next Level.", True, (0, 0, 0))
            text_x = (window_width - win_message.get_width()) // 2
            text_y = (window_height - win_message.get_height()) // 2

            window.blit(win_message, (text_x, text_y))
            pygame.display.update()
            pygame.time.wait(3000)

            # Handle game end when player wins a level
            
            game_info.next_level()
            player_car.restart() 
            ai_car.next_level(game_info.level)
    if game_info.game_ended():
        window.fill((200, 200, 200))

        end_message = font.render(f"Congratulations, You the Game!!", True, (0, 0, 0))
        text_x = (window_width - end_message.get_width()) // 2
        text_y = (window_height - end_message.get_height()) // 2

        window.blit(end_message, (text_x, text_y))
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.restart()
        ai_car.restart()
    


# print(ai_car.path)       
pygame.quit()