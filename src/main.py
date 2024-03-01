import pygame
import math
import random
from render import *
from conf import *
import asyncio

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Billiards")


screen.fill(BACKGROUND)
pygame.display.update()



c = pygame.time.Clock()
running = True


async def main():

    global running
    global c
    global screen
    global pygame

    init()

    while running:

        
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    launch()
        
        pressed_keys = pygame.key.get_pressed()
        if  pressed_keys[pygame.K_a]:
            turn_tracer()
        if pressed_keys[pygame.K_d]:
            turn_tracer(invert=True)
        if  pressed_keys[pygame.K_q]:
            turn_tracer(fine=True)
        if pressed_keys[pygame.K_e]:
            turn_tracer(fine=True,invert=True)
        if pressed_keys[pygame.K_s]:
            decrease_power()
        if pressed_keys[pygame.K_w]:
            increase_power()
                    

        dt = c.tick(max_frame_rate)
        evolve(dt)

        screen.blit(render(),(0,0))
        
        await asyncio.sleep(0)
        pygame.display.flip()
        # render 
        

asyncio.run(main())