import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pybullet as p
import pybullet_data
import time
   

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, -2.0, -10)

# Ініціалізація PyBullet
p.connect(p.DIRECT)  # або p.GUI, щоб бачити GUI фізики
p.setGravity(0, -9.8, 0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0, 5, 0]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
cubeId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)  # використовуємо модель r2d2 як куб

clock = pygame.time.Clock()

# Основний цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Крок фізики
    p.stepSimulation()
    
    # Отримуємо позицію куба
    pos, orn = p.getBasePositionAndOrientation(cubeId)
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    # Малюємо куб як простий квад (для прикладу)
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glBegin(GL_QUADS)
    glColor3f(1,0,0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    glEnd()
    glPopMatrix()
    
    pygame.display.flip()
    clock.tick(60)

p.disconnect()
pygame.quit()