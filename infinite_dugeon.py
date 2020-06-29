import os
import random
import monsters
class Direction:
    LEFT = 0
    FRONT = 1
    RIGHT = 2
    BACK = 3
class Wall_type:
    WALL = 0
    DOOR = 1
    @staticmethod
    def random():
        return random.randint(0, 1)

class Block:
    def __init__(self, block=None, from_=None):
        self.boss_room = not bool(random.randint(0,100))
        if self.boss_room:
            self.objects = [monsters.Slime(hp=100)]
        else:
            self.objects = [monsters.Slime()]
        self._direction = [Wall_type.random() for i in range(4)]
        if block:
            self._direction[from_-2] = block
    
    def move_to(self, direction):
        if self._direction[direction]:
            if self._direction[direction] == Wall_type.DOOR:
                self._direction[direction] = Block(block=self, from_=direction)
            return self._direction[direction]
        return self

    def add_object(self, object_):
        self.objects.append(object_)

    def __str__(self):
        walls = ['|', '--', '|', '--']
        for i, wall in enumerate(self._direction):
            if wall:
                if i % 2:
                    walls[i] = '  '
                else:
                    walls[i] = ' '
        block_str = '+---%s---+\n'%walls[1] + \
                    '|        |\n' + \
                    '%s        %s\n'%(walls[0], walls[2]) + \
                    '|        |\n' + \
                    '+---%s---+\n'%walls[3]
        if self.boss_room:
            print('!!!!BOSS!!!!')
        for o in self.objects:
            block_str += 'slime_hp:%d'%o.hp

        return block_str

class State:
    NORMAL = 0

class Player:
    def __init__(self):
        self.state = State.NORMAL
        self.hp = 100
        self.exp = 0
        self.lv = 1
        self.str = 10
    def attack(self, target):
        target.hp -= self.str

    def action(self, target):
        self.attack(target)

if __name__ == '__main__':
    current_block = Block()
    player = Player()
    move_actions = ['left', 'front', 'right', 'back', 'attack']
    while True:
        print(current_block)
        for i, act in enumerate(move_actions):
            print('<%d>%s,'%(i, act),end='')
        print()
        print('enter action:')
        action = int(input())
        if action < 4:
            current_block = current_block.move_to(action)
        else:
            print('<%d>%s,'%(0, 'cancel'),end='')
            for i,target in enumerate(current_block.objects):
                print('<%d>%s,'%(i+1, target.name),end='')
            print()
            print('choose target:')
            action = int(input())
            if not action:
                continue
            else:
                player.attack(current_block.objects[action-1])
            if current_block.objects[action-1].hp <= 0:
                del current_block.objects[action-1]
            else:
                current_block.objects[action-1].attack(player)
                print('attacked hp:%d'%player.hp)

        os.system('clear')