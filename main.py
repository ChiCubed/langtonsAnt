import pygame, sys


WINDOW_SIZE = (500,500)
FPS         = 60.0


pygame.init()

# Icon must be set before screen
# has been initialised
icon = pygame.image.load("icons/icon.png")
pygame.display.set_icon(icon)

screen = pygame.display.set_mode(WINDOW_SIZE)
clock  = pygame.time.Clock()

pygame.display.set_caption('Langton\'s Ant', 'Langton\'s Ant')


# The ui module requires pygame to be initialised,
# and the video mode to be set, since it calls
# convert_alpha on some surfaces to improve speed.
import ui


# A function to get the FPS
def _temp_get_fps():
    if clock.get_fps():
        return clock.get_fps()
    # Prevent get_fps from
    # ever returning 0.
    return FPS
    ui.get_fps = clock.get_fps


ui.get_fps = _temp_get_fps


screenContainer = ui.UnboundedContainer((0,0))


while 1:
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and
            event.key == pygame.K_ESCAPE) or \
           event.type == pygame.QUIT:
            pygame.quit() # IDLE friendly :)
            sys.exit(0)
        
        screenContainer.handle_event(
            event, pygame.mouse.get_pos()
        )
                
    screen.fill(pygame.colordict.THECOLORS['white'])

    
    screenContainer.update()
    screenContainer.draw(screen)
    
    pygame.display.flip()
    
    clock.tick(FPS)
