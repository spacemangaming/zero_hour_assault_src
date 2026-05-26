import pygame
from pygame.locals import *

pygame.joystick.init()

class joystick:
    def __init__(self, joystick_index=0):
        self.joystick = pygame.joystick.Joystick(joystick_index)
        self.joystick.init()
        self.current_button_pressed = -2
        self.current_button_released = -2
        self.buttons_held = []
        self.axes_values = [0] * self.joystick.get_numaxes()
        self.hats_values = [(0, 0)] * self.joystick.get_numhats()
        self.balls_values = [(0, 0)] * self.joystick.get_numballs()

    def update(self, events=None):
        self.current_button_pressed = -2
        self.current_button_released = -2
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                self.buttons_held.append(event.button)
                self.current_button_pressed = event.button
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in self.buttons_held:
                    self.buttons_held.remove(event.button)
                self.current_button_released = event.button
            elif event.type == pygame.JOYAXISMOTION:
                try: self.axes_values[event.axis] = round(event.value, 2)
                except: pass
            elif event.type == pygame.JOYHATMOTION:
                try: self.hats_values[event.hat] = event.value
                except: pass
            elif event.type == pygame.JOYBALLMOTION:
                try: self.balls_values[event.ball] = round(event.rel[0], 2), round(event.rel[1], 2)
                except: pass
    def button_pressed(self, button):
        return self.current_button_pressed == button

    def button_released(self, button):
        return self.current_button_released == button

    def button_down(self, button):
        return button in self.buttons_held

    def button_up(self, button):
        return button not in self.buttons_held

    def get_axis(self, axis):
        if 0 <= axis < len(self.axes_values):
            return self.axes_values[axis]
        else:
            return 0

    def get_hat(self, hat):
        if 0 <= hat < len(self.hats_values):
            return self.hats_values[hat]
        else:
            return (0, 0)

    def get_ball(self, ball):
        if 0 <= ball < len(self.balls_values):
            return self.balls_values[ball]
        else:
            return (0, 0)


import globals as g

class joystick_wrapper:
    def button_pressed(self, button):
        for j in g.sticks:
            if j.current_button_pressed == button:
                return True
        return False

    def button_released(self, button):
        for j in g.sticks:
            if j.current_button_released == button:
                return True
        return False

    def button_down(self, button):
        for j in g.sticks:
            if button in j.buttons_held:
                return True
        return False

    def button_up(self, button):
        return not self.button_down(button)
        for j in g.sticks:
            if button not in j.buttons_held:
                return True
        return False

    def get_axis(self, axis):
        for j in g.sticks:
            if j.get_axis(axis) != 0:
                return j.get_axis(axis)
        return 0

    def get_hat(self, hat):
        for j in g.sticks:
            if j.get_hat(hat) != (0, 0):
                return j.get_hat(hat)
        return (0, 0)

    def get_ball(self, ball):
        for j in g.sticks:
            if j.get_ball(ball) != (0, 0):
                return j.get_ball(ball)
        return (0, 0)
