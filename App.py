#!/usr/bin/env python

import os
import pygame

from Neuron import Neuron
from Point import Point

class App():

    W = 900
    H = 900

    BG_COLOR = (0, 0, 0)

    def __init__(self, width=None, height=None):
        if width == None: width = App.W
        if height == None: height = App.H

        self._init_pygame(width, height)
        self._init_neuron()
        self._init_points()

    def _init_pygame(self, width, height):
        self._w = width
        self._h = height

        pygame.init()
        info = pygame.display.Info()
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % ((info.current_w - self._w) / 2, 0)
        self._screen = pygame.display.set_mode((self._w, self._h))
        pygame.display.set_caption('Neuron visualisation')

        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont("freesansbold", 25)

        print('''
=========================
Commands:

  ESCAPE or 'q' => Quit the program
  'r'           => Reset Neuron and Points
  'c'           => Remove all Points (keep Neuron's training)
  'a'           => Add some Points
  UP            => Increment training rate (equation move slower with high precision)
  DOWN          => Decrement training rate (equation move fast with low precision)
=========================
        ''')

    def _init_neuron(self):
        self._neuron = Neuron()
        self._training_rate_power = -3

    def _init_points(self):
        self._points = []

    def events(self):
        event = pygame.event.poll()
        if event != pygame.NOEVENT and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                self._running = False
            if event.key == pygame.K_r:
                self._init_neuron()
                self._init_points()
            if event.key == pygame.K_c:
                self._init_points()
            if event.key == pygame.K_a:
                for _ in range(0, 50):
                    self._points.append(Point())
            if event.key == pygame.K_UP:
                if self._training_rate_power > -20:
                    self._training_rate_power -= 1
            if event.key == pygame.K_DOWN:
                if self._training_rate_power < -1:
                    self._training_rate_power += 1

    def update(self):
        not_found = []
        for p in self._points:
            p.found(False)
            o = self._neuron.forward(p.inputs)
            if o == p.label:
                p.found()
            else:
                not_found.append(p)

        self._found_count = len(self._points) - len(not_found)

        for p in not_found:
            self._neuron.train(p.inputs, p.label, 1 * 10 ** self._training_rate_power)

    def _transpose_pos(self, pos):
        posx, posy = pos
        x = (posx + 1.) * self._w / 2
        y = self._h - ((posy + 1.) * self._h / 2)
        return (int(x), int(y))

    def _draw_line(self, pos1, pos2, color=(255, 255, 255), thickness=1):
        start_pos = self._transpose_pos((pos1[0], pos1[1]))
        end_pos   = self._transpose_pos((pos2[0], pos2[1]))
        pygame.draw.line(self._screen, color, start_pos, end_pos, thickness)

    def _draw_text(self, txt, pos, color='white'):
        surface = self._font.render(txt, True, pygame.Color(color), App.BG_COLOR)
        pos = self._transpose_pos(pos)
        self._screen.blit(surface, pos)

    def _draw_grid(self):
        self._draw_line(( 0., -1.), (0., 1.), thickness=2)
        self._draw_line((-1.,  0.), (1., 0.), thickness=2)

        self._draw_text('0',  ( .03, -.03))
        self._draw_text('-1', ( .03, -.96))
        self._draw_text('1',  ( .03,  .98))
        self._draw_text('-1', (-.98,  .05))
        self._draw_text('1',  ( .96,  .05))

        for step in range(-10, 10):         # simulate range() on float with .1 increment
            i = step / 10
            self._draw_line((  i, -1.), ( i, 1.), color=(30, 30, 30))
            self._draw_line((-1.,   i), (1.,  i), color=(30, 30, 30))

    def _draw_point(self, point):
        color = (255, 0, 255)
        if point.label == 1.: color = (0, 255, 255)

        fcolor = (255, 0, 0)
        if point.was_found: fcolor = (0, 255, 0)

        pos = self._transpose_pos((point.x, point.y))

        pygame.draw.circle(self._screen, color, pos, Point.R, 1)
        pygame.draw.circle(self._screen, fcolor, pos, Point.R // 2)

    def _draw_neuron(self):
        self._draw_line((-1., self._neuron.F(-1.)), (1., self._neuron.F(1.)), color=(0, 255, 0))
        self._draw_text('Equation approximated: %+0.4f * x %+0.4f' % (self._neuron.F_a(), self._neuron.F_b()), (-.98, .98))

    def draw(self):
        self._screen.fill(App.BG_COLOR)

        self._draw_grid()

        # Draw expected F(x)
        self._draw_line((-1., Point.F(-1.)), (1., Point.F(1.)), color=(255, 255, 0))

        for p in self._points:
            self._draw_point(p)
        self._draw_neuron()

        self._draw_text('Equation expected        : %+0.4f * x %+0.4f' % (Point.A, Point.B), (-.98, .93))
        accuracy = 'Accuracy:'
        if len(self._points) > 0:
            accuracy = 'Accuracy: %0.2f%% (%d/%d)' % (self._found_count * 100 / len(self._points), self._found_count, len(self._points))
        self._draw_text(accuracy, (-.98, .88))

        self._draw_text('Training rate: 0.%s1' % ('0' * (-self._training_rate_power - 1)), (-.98, .83))

        pygame.display.update()

    def run(self):
        self._running = True
        while self._running:
            self._clock.tick(60)

            self.events()
            self.update()
            self.draw()


if __name__ == '__main__':
    import re
    import sys

    if len(sys.argv) > 1:
        F_pattern = r'([-+]?\s*[0-9\.]+)\s*\*?\s*x\s*([-+]\s*[0-9\.]+)'
        m = re.match(F_pattern, sys.argv[1])
        if not m: raise RuntimeError('Equation argument is not valid')
        a = float(m.group(1).replace(' ', ''))
        b = float(m.group(2).replace(' ', ''))
        Point.set_equation_F(a, b)
    a = App()
    a.run()
