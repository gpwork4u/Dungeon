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
        return max(random.randint(0, 4), 1)

class Block:
    def __init__(self):
        self.builded = False
        self.direction = [[Wall_type.DOOR for i in range(4)]]
        self.objects = []
    def build(self, from_=None, walls=[]):
        self.builded = True
        self.random_monster = random.randint(0,100)
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
            block_str += o.name + ':' + str(o.hp) + '\n'

        return block_str

class State:
    NORMAL = 0

class Player:
    def __init__(self, coor_x=0, coor_y=0, name='player'):
        self.state = State.NORMAL
        self.name = name
        self.coor_x = coor_x
        self.coor_y = coor_y
        self.position = None
        self.hp = 100
        self.str = 10
        self.agi = 10
        self.luc = 10
        self.int = 10
    def attack(self, target):
        target.hp -= self.str

    def action(self, action):
        if action < 4:
            if not self.position.direction[action]:
                return
            x_move = 0
            y_move = 0
            direction = 1
            if action % 2 == 0:
                x_move = 1
            else:
                y_move = -1
            if action < 2:
                direction = -1
            self.coor_x += direction * x_move
            self.coor_y += direction * y_move
            current_coor = (self.coor_x, self.coor_y)
            self.position.objects.remove(player)
            self.position = dugeon[current_coor]
            self.position.objects.append(player)
            if not self.position.builded:
                walls = []
                if self.coor_x == X_BORDER - 1 \
                   or dugeon[self.coor_x+1][self.coor_y] == Wall_type.WALL:
                    walls.append(Direction.RIGHT)
                if self.coor_x == 0 \
                   or dugeon[self.coor_x-1][self.coor_y] == Wall_type.WALL:
                    walls.append(Direction.LEFT)
                if self.coor_y == Y_BORDER - 1 \
                   or dugeon[self.coor_x-1][self.coor_y] == Wall_type.WALL:
                    walls.append(Direction.FRONT)
                if self.coor_y == 0 \
                   or dugeon[self.coor_x-1][self.coor_y] == Wall_type.WALL:
                    walls.append(Direction.BACK)
                self.position.build(from_=action, walls=walls)
        else:
            print('<%d>%s,'%(0, 'cancel'),end='')
            for i,target in enumerate(self.position.objects):
                print('<%d>%s,'%(i+1, target.name),end='')
            print()
            print('choose target:')
            action = int(input())
            if not action:
                return
            else:
                self.attack(self.position.objects[action-1])
            if self.position.objects[action-1].hp <= 0:
                del self.position.objects[action-1]

    def __str__(self):
        return self.name

if __name__ == '__main__':
    move_actions = ['left', 'front', 'right', 'back', 'attack']
    X_BORDER = 10
    Y_BORDER = 10
    dugeon = [[Block() for j in range(Y_BORDER)] for i in range(X_BORDER)]
    dugeon = np.array(dugeon)
    coor_x = 1
    coor_y = 1
    start_block = dugeon[coor_x, coor_y]
    players = [Player(coor_x=coor_x, coor_y=coor_y, name='gp%d'%i) for i in range(2)]
    for p in players:
        p.position = start_block
        start_block.add_object(p)
    start_block.build()
    turn = 1
    while True:
        turn = (turn + 1)%2
        player = players[turn]
        current_coor = (player.coor_x, player.coor_y)
        os.system('clear')
        print('turn:%s'%player.name)
        print(current_coor)
        print(player.position)
        for i, act in enumerate(move_actions):
            print('<%d>%s,'%(i, act),end='')
        print()
        print('enter action:')
        action = int(input())
        player.action(action)