import os
import random
import numpy as np
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
    def __init__(self):
        self.builded = False

    def build(self, from_=None, walls=[]):
        self.builded = True
        self.boss_room = not bool(random.randint(0,100))
        if self.boss_room:
            self.objects = [monsters.Slime(hp=100)]
        else:
            self.objects = [monsters.Slime()]
        self.direction = [Wall_type.random() for i in range(4)]
        if from_ != None:
            self.direction[from_-2] = Wall_type.DOOR
        for wall in walls:
            self.direction[wall] = Wall_type.WALL
    def add_object(self, object_):
        self.objects.append(object_)

    def __str__(self):
        walls = ['|', '--', '|', '--']
        for i, wall in enumerate(self.direction):
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
    player = Player()
    move_actions = ['left', 'front', 'right', 'back', 'attack']
    dugeon = [[Block() for j in range(3)] for i in range(3)]
    dugeon = np.array(dugeon)
    coor_x = 1
    coor_y = 1
    current_coor = (coor_x, coor_y)
    current_block = dugeon[current_coor]
    current_block.build()
    while True:
        print(current_coor)
        print(current_block)
        for i, act in enumerate(move_actions):
            print('<%d>%s,'%(i, act),end='')
        print()
        print('enter action:')
        action = int(input())
        if action < 4:
            if not current_block.direction[action]:
                continue
            x_move = 0
            y_move = 0
            direction = 1
            if action%2 == 0:
                x_move = 1
            else:
                y_move = -1
            if action < 2:
                direction = -1
            coor_x += direction*x_move
            coor_y += direction*y_move
            current_coor = (coor_x, coor_y)
            current_block = dugeon[current_coor]
            if not current_block.builded:
                walls = []
                if coor_x == dugeon.shape[0]-1:
                    walls.append(Direction.RIGHT)
                if coor_x == 0:
                    walls.append(Direction.LEFT)
                if coor_y == dugeon.shape[1]-1:
                    walls.append(Direction.FRONT)
                if coor_y == 0:
                    walls.append(Direction.BACK)
                current_block.build(from_=action, walls=walls)
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