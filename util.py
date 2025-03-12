import pygame

def scale_images(image, scale):
    size = round(image.get_width() * scale), round(image.get_height() * scale)
    return pygame.transform.scale(image, size)

# We need a function to rotate the cars image's rectangles
def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)
