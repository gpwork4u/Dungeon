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
        self.direction = [[Wall_type.DOOR for i in range(4)]]
    def build(self, from_=None, walls=[]):
        self.builded = True
        self.random_monster = random.randint(0,100)
        self.objects = []
        if self.random_monster == 0:
            self.objects.append(monsters.Slime(hp=100))
        elif self.random_monster < 20:
            self.objects.append(monsters.Slime())
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
        if self.random_monster == 0:
            print('!!!!BOSS!!!!')
        for o in self.objects:
            block_str += 'slime_hp:%d'%o.hp

        return block_str

class State:
    NORMAL = 0

class Player:
    def __init__(self, name='player'):
        self.state = State.NORMAL
        self.name = name
        self.hp = 100
        self.str = 10
        self.agi = 10
        self.luc = 10
        self.int = 10
    def attack(self, target):
        target.hp -= self.str

    def action(self, target):
        self.attack(target)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    player = Player()
    move_actions = ['left', 'front', 'right', 'back', 'attack']
    X_BORDER = 3
    Y_BORDER = 3
    dugeon = [[Block() for j in range(Y_BORDER)] for i in range(X_BORDER)]
    dugeon = np.array(dugeon)
    coor_x = 1
    coor_y = 1
    current_coor = (coor_x, coor_y)
    current_block = dugeon[current_coor]
    current_block.build()
    while True:
        os.system('clear')
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
            current_block.remove(player)
            current_block = dugeon[current_coor]
            current_block.append(player)
            if not current_block.builded:
                walls = []
                if coor_x == X_BORDER - 1 \
                   or dugeon[coor_x+1][coor_y] == Wall_type.WALL:
                    walls.append(Direction.RIGHT)
                if coor_x == 0 \
                   or dugeon[coor_x-1][coor_y] == Wall_type.WALL:
                    walls.append(Direction.LEFT)
                if coor_y == Y_BORDER - 1 \
                   or dugeon[coor_x-1][coor_y] == Wall_type.WALL:
                    walls.append(Direction.FRONT)
                if coor_y == 0 \
                   or dugeon[coor_x-1][coor_y] == Wall_type.WALL:
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