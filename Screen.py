import time
import os
from threading import Thread
import pygame
from render_image import render_image


class Screen(object):
    def __init__(self, min_real, max_real, min_i, max_i):
        self.min_real = min_real
        self.max_real = max_real
        self.min_i = min_i
        self.max_i = max_i
        self.nodes = []

        if not os.path.exists('images'):
            os.mkdir('images')

        print('Initializing...')
        for x in range(0, 800, 50):
            for y in range(0, 500, 50):
                print('Rendering {0}, {1}'.format(x, y))
                self.render_image(x, y)

        pygame.init()
        self.screen = pygame.display.set_mode([801, 500])
        pygame.display.set_caption('Fractal')

    def blit_image_from_location(self, location):
        image = pygame.image.load(location)
        self.screen.blit(image, (0, 0))
        pygame.display.flip()

    def blit_image(self, x, y):
        location = os.path.join('images', '{0}_{1}.png'.format(x, y))
        self.blit_image_from_location(location)

    def get_complex_from_position(self, x, y):
        real = self.min_real + (x/800)*(self.max_real - self.min_real)
        imag = self.min_i + (y/499)*(self.max_i - self.min_i)
        return complex(real, imag)

    def render_image(self, x, y):
        c = self.get_complex_from_position(x, y)
        path = os.path.join('images', '{0}_{1}.png'.format(x, y))
        if not os.path.exists(path):
            render_image(c, path)
        self.nodes.append((x, y))

    def find_nearest_node(self, pos):
        min_dist = float('inf')
        min_node = None
        for node in self.nodes:
            distance = ((node[0] - pos[0]) ** 2 + (node[1] - pos[1]) ** 2) ** 0.5
            if distance < min_dist:
                min_dist = distance
                min_node = node
        return min_node

    def run(self):
        start_time = 0
        previous_pos = None
        render_started = False
        while True:
            for _ in pygame.event.get():
                pass
            pos = pygame.mouse.get_pos()

            node = self.find_nearest_node(pos)
            if pos == previous_pos and not render_started and time.time() - start_time > 0.5:
                print('Rendering {0}, {1}'.format(*pos))
                Thread(target=self.render_image, args=pos).start()
                render_started = True
            if pos != previous_pos:
                start_time = time.time()
                render_started = False
            previous_pos = pos
            self.blit_image(*node)


Screen(-1, 1, -1, 1).run()





