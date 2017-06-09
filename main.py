import pygame, sys


WINDOW_SIZE = (640,480)


pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
clock  = pygame.time.Clock()


import ui # some of this requires pygame to be initialised


def _temp_get_fps():
    if clock.get_fps():
        return clock.get_fps()
    # Prevent get_fps from
    # ever returning 0.
    return 60.0
    ui.get_fps = clock.get_fps


ui.get_fps = _temp_get_fps

bigc = ui.Container(pos=(0,0))

for x in range(3):
    for y in range(3):
        c = ui.Container(pos=(x*90,y*90))
        for i in range(3):
            for j in range(3):
                c.children.append(ui.Checkbox((i*20,j*20),size=(20,20)))
        bigc.children.append(c)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # IDLE friendly :)
            sys.exit(0)
        bigc.handle_event(event, pygame.mouse.get_pos())
                
    screen.fill(pygame.colordict.THECOLORS['white'])
    
    bigc.update() # Update is handled regardless of visibility
    bigc.draw(screen)
    
    bigc[2].pos[1] += 1
    
    pygame.display.flip()
    
    clock.tick(60.0)
