class Monster:
    def __init__(self):
        self.str = 10
    def attack(self, target):
        for t in target:
            t.hp -= self.str


class Slime(Monster):
    def __init__(self, hp=30):
        self.hp = hp
        self.say = ''
        self.name = 'slime'
        self.str = hp / 10
    def attack(self, target):
        self.str = self.hp / 10
        target.hp -= self.str

    def action(self, target):
        self.attack(target)