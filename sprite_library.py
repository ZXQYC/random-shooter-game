
import pygame

from utils import *


def collide_mask(c1, c2):
    return pygame.sprite.collide_mask(c1, c2) is not None


class VectorSprite(pygame.sprite.Sprite):
    def __init__(self, containers, image, start):
        super().__init__(containers)
        self.image = None
        self.rect = None
        self.vec = start
        self.set_image(image)

    def set_image(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.move_to(self.vec)

    def move_to(self, vec):
        cx, cy = self.rect.center
        self.rect.move_ip(int(vec[0]-cx), int(vec[1]-cy))
        self.vec = vec

    def move_by(self, vec):
        self.move_to(vec+self.vec)

    def point_inside_rect(self, pt):
        horizontal = self.rect.left <= pt[0] <= self.rect.right
        vertical = self.rect.top <= pt[1] <= self.rect.bottom
        return horizontal and vertical

    def is_on_screen(self):
        horizontal = segment_intersects(self.rect.left, self.rect.right, 0, WINDOW_SIZE[0])
        vertical = segment_intersects(self.rect.bottom, self.rect.top, 0, WINDOW_SIZE[1])
        return vertical and horizontal


def image_from_text(text, font_size, color):
    font = pygame.font.SysFont('mono', font_size)
    return font.render(text, True, color)


class TextSprite(VectorSprite):
    def __init__(self, containers, text, start, font_size=24, color=(255, 255, 255)):
        super().__init__(
            containers=containers,
            image=pygame.Surface((1, 1)),
            start=start
        )
        self.font_size = font_size
        self.color = color
        self.text = text
        self.update_image()

    def update_image(self):
        self.set_image(image_from_text(self.text, self.font_size, self.color))

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.update_image()

    def set_color(self, color):
        if color != self.color:
            self.color = color
            self.update_image()

    def set_font_size(self, font_size):
        if font_size != self.font_size:
            self.font_size = font_size
            self.update_image()


class RectangleSprite(VectorSprite):
    def __init__(self, containers, color, size, border_size, start):
        super().__init__(
            containers=containers,
            image=pygame.Surface(size),
            start=start
        )
        self.color = color
        self.size = size
        self.border_size = border_size
        self.inner_size = self.size-2*self.border_size

    def update(self):
        self.image.fill(self.color)
        self.image.fill((0, 0, 0), pygame.Rect(
            self.border_size,
            self.border_size,
            self.inner_size[0],
            self.inner_size[1]
        ))


class Button(RectangleSprite):
    def __init__(self, containers, text, start, size, onclick=lambda: None,
                 font_size=24, color=(200, 200, 200),
                 hover_color=(255, 255, 255), border_size=2):
        super().__init__(
            containers=containers,
            color=color,
            size=size,
            border_size=border_size,
            start=start
        )
        self.text = TextSprite(containers, text, start, font_size, color)
        self.onclick = onclick
        self.normal_color = color
        self.hover_color = hover_color
        self.being_pressed = False

    def set_color(self, color):
        self.color = color
        self.text.set_color(color)

    def update(self):
        pressed = pygame.mouse.get_pressed(3)[0]
        if self.point_inside_rect(pygame.mouse.get_pos()):
            self.set_color(self.hover_color)
            if pressed:
                self.being_pressed = True
            else:
                if self.being_pressed:
                    self.onclick()
                self.being_pressed = False
        else:
            self.set_color(self.normal_color)
            self.being_pressed = False

        super().update()


class Collider(VectorSprite):
    def __init__(self, containers, image, start, health, damage):
        super().__init__(containers, image, start)
        self.health = health
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = damage

    def get_hit(self, other):
        self.health.take_damage(other.damage)
        if self.health.dead():
            self.kill()

    @staticmethod
    def collide(c1, c2):
        c1.get_hit(c2)
        c2.get_hit(c1)

    @staticmethod
    def collide_all(c1, c2s):
        sprite_list = pygame.sprite.spritecollide(c1, c2s, False, collide_mask)
        for c2 in sprite_list:
            Collider.collide(c1, c2)
