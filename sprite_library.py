"""A library of many different Sprite subclasses to use"""

import numpy as np
import pygame

from utils import segment_intersects, WINDOW_SIZE


def collide_mask(mask1, mask2):
    """Checks if two masks collide"""
    return pygame.sprite.collide_mask(mask1, mask2) is not None


class VectorSprite(pygame.sprite.Sprite):
    """A sprite that is centered and can be moved based on that center"""
    def __init__(self, containers, image, start):
        """Creates the VectorSprite"""
        super().__init__(containers)
        self.image = None
        self.rect = None
        self.vec = start
        self.set_image(image)

    def set_image(self, image):
        """Sets the image for the vector sprite"""
        self.image = image
        self.rect = self.image.get_rect()
        self.move_to(self.vec)

    def move_to(self, vec):
        """Moves the sprite to a new location"""
        cursor_x, cursor_y = self.rect.center
        self.rect.move_ip(int(vec[0]-cursor_x), int(vec[1]-cursor_y))
        self.vec = vec

    def move_by(self, vec):
        """Moves the sprite given a displacement vector"""
        self.move_to(vec+self.vec)

    def point_inside_rect(self, point):
        """Check if a particular point is inside the rectangle that bounds this sprite"""
        horizontal = self.rect.left <= point[0] <= self.rect.right
        vertical = self.rect.top <= point[1] <= self.rect.bottom
        return horizontal and vertical

    def is_on_screen(self):
        """Checks if this sprite is on screen"""
        horizontal = segment_intersects(self.rect.left, self.rect.right, 0, WINDOW_SIZE[0])
        vertical = segment_intersects(self.rect.bottom, self.rect.top, 0, WINDOW_SIZE[1])
        return vertical and horizontal

    def hitting_screen_boundary(self):
        """Checks if this sprite is hitting the boundary of the screen"""
        ans = np.array([0, 0])
        if self.rect.left < 0:
            ans[0] = -1
        if self.rect.right >= WINDOW_SIZE[0]:
            ans[0] = 1
        if self.rect.top < 0:
            ans[1] = -1
        if self.rect.bottom >= WINDOW_SIZE[1]:
            ans[1] = 1
        return ans

    def center_off_screen(self):
        ans = np.array([0, 0])
        for dimension in range(2):
            if self.vec[dimension] < 0:
                ans[dimension] = -1
            if self.vec[dimension] >= WINDOW_SIZE[dimension]:
                ans[dimension] = 1
        return ans


class TextSprite(VectorSprite):
    """A sprite that contains text"""
    def __init__(self, containers, text, start, font_size=24, color=(255, 255, 255)):
        """Creates the TextSprite"""
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
        """Updates the image used for this sprite"""
        font = pygame.font.SysFont('mono', self.font_size)
        img = font.render(self.text, True, self.color)
        self.set_image(img)

    def set_text(self, text):
        """Sets the text"""
        if text != self.text:
            self.text = text
            self.update_image()

    def set_color(self, color):
        """Sets the color"""
        if color != self.color:
            self.color = color
            self.update_image()

    def set_font_size(self, font_size):
        """Sets the font size"""
        if font_size != self.font_size:
            self.font_size = font_size
            self.update_image()


class RectangleSprite(VectorSprite):
    """A sprite that displays a rectangle"""
    def __init__(self, containers, color, size, border_size, start, fill=False):
        """Creates the RectangleSprite"""
        super().__init__(
            containers=containers,
            image=pygame.Surface(size),
            start=start
        )
        self.color = color
        self.size = size
        self.border_size = border_size
        self.inner_size = self.size-2*self.border_size
        self.fill = fill

    def update(self):
        """Draws the image for the sprite"""
        self.image.fill(self.color)
        if not self.fill:
            self.image.fill((0, 0, 0), pygame.Rect(
                self.border_size,
                self.border_size,
                self.inner_size[0],
                self.inner_size[1]
            ))


class Button(RectangleSprite):
    """A button that can be pressed"""
    def __init__(self, containers, text, start, size, onclick=lambda: None,
                 font_size=24, color=(200, 200, 200),
                 hover_color=(255, 255, 255), border_size=2):
        """Creates the button"""
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
        """Sets the button color"""
        self.color = color
        self.text.set_color(color)

    def update(self):
        """Updates the button"""
        pressed = pygame.mouse.get_pressed(3)[0]  # check if mouse button is clicked
        if self.point_inside_rect(pygame.mouse.get_pos()):  # mouse is inside button
            self.set_color(self.hover_color)
            if pressed:
                self.being_pressed = True
            else:
                if self.being_pressed:
                    self.onclick()  # register a click
                self.being_pressed = False
        else:  # mouse is not inside button
            self.set_color(self.normal_color)
            self.being_pressed = False

        super().update()


class Collider(VectorSprite):
    """A sprite that collides using a mesh with other sprites"""
    def __init__(self, containers, image, start, health, damage, hitbox=None):
        """Creates the Collider"""
        super().__init__(containers, image, start)
        self.health = health
        if hitbox is not None:
            self.mask = pygame.mask.from_surface(hitbox)
        else:
            self.mask = pygame.mask.from_surface(self.image)
        self.damage = damage

    def get_hit(self, other):
        """Gets hit by another Collider"""
        self.health.take_damage(other.damage)
        if self.health.dead():
            self.kill()

    @staticmethod
    def collide(collider1, collider2):
        """Causes two Colliders to damage each other"""
        collider1.get_hit(collider2)
        collider2.get_hit(collider1)

    @staticmethod
    def collide_all(collider1, collider2s):
        """Checks for collisions between many colliders"""
        sprite_list = pygame.sprite.spritecollide(collider1, collider2s, False, collide_mask)
        for collider2 in sprite_list:
            Collider.collide(collider1, collider2)
