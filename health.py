
class Health:
    def __init__(self, hp=1, regen=0):
        self.hp = hp
        self.regen = regen

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def dead(self):
        return self.hp == 0

    def die(self):
        self.hp = 0

    def update(self):
        if not self.dead():
            self.hp += self.regen


class InfiniteHealth(Health):
    def take_damage(self, dmg):
        pass


class OneHealth(Health):
    def take_damage(self, dmg):
        if dmg > 0:
            self.die()
