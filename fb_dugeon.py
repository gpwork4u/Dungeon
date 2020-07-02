from Facebooker import facebook
from dungeon import *
players = {}
fb = facebook.API()
commands = {
            'left':0,
            'front':1,
            'right':2,
            'back':3,
            'attack':4,
            'say':5,
           }
X_BORDER = 10
Y_BORDER = 10
dugeon = [[Block() for j in range(Y_BORDER)] for i in range(X_BORDER)]
dugeon = np.array(dugeon)
coor_x = 1
coor_y = 1
start_block = dugeon[coor_x, coor_y]
start_block.build()
email = 'email'
password = 'pass'
fb.login(email, password)
while True:
    unread_chats = fb.get_unread_chat()
    for chat in unread_chats:
        msg = fb.get_msg(chat, 1)
        msg = msg[0][1]
        send_from = list(fb.get_msg(chat))[0][0]
        print('get chat id:%s, message:%s'%(chat, msg))
        if len(msg) == 0:
            continue
        if msg == '/start':
            fb.send_msg(chat, 'game start')
            players[chat] =Player(coor_x=coor_x, coor_y=coor_y, name=send_from)
            start_block.add_object(players[chat])
            players[chat].position = start_block
            coor = '(%d,%d)\n'%(coor_x, coor_y)
            fb.send_msg(chat, coor + players[chat].position.fb_format())
            print(coor)
            print(players[chat].position)
        elif msg == '/help':
            help_mdg = '/start : game start\n' + \
                       '/left : go left\n' + \
                       '/front : go front\n' + \
                       '/right : go right\n' + \
                       '/back : go back\n' + \
                       '/attack {target number} : attack target\n'

        elif msg[0] == '/':
            msg = msg[1:]
            if chat in players:
                player = players[chat]
                split = msg.find(' ')
                if split > 0:
                    cmd = [msg[:split], msg[split:]]
                else:
                    cmd = [msg]
                try:
                    action = commands[cmd[0]]
                    target = None
                    if len(cmd) >= 2:
                        target = cmd[1]
                    if action == 4:
                        try:
                            target = int(target)
                        except:
                            target = 0
                    player.action(action, target)
                    player.position = dugeon[player.coor_x,player.coor_y]
                except:
                    fb.send_msg(chat, 'command error')
                if not players[chat].position.builded:
                    walls = []
                    if player.coor_x == X_BORDER - 1 \
                        or dugeon[player.coor_x+1][player.coor_y] == Wall_type.WALL:
                        walls.append(Direction.RIGHT)
                    if player.coor_x == 0 \
                        or dugeon[player.coor_x-1][player.coor_y] == Wall_type.WALL:
                        walls.append(Direction.LEFT)
                    if player.coor_y == Y_BORDER - 1 \
                        or dugeon[player.coor_x-1][player.coor_y] == Wall_type.WALL:
                        walls.append(Direction.FRONT)
                    if player.coor_y == 0 \
                        or dugeon[player.coor_x-1][player.coor_y] == Wall_type.WALL:
                        walls.append(Direction.BACK)
                    players[chat].position.build(from_=action, walls=walls)
                if action < 4:
                    players[chat].position.add_object(player)
                coor = '(%d,%d)\n'%(player.coor_x, player.coor_y)
                fb.send_msg(chat, coor + players[chat].position.fb_format())
                print(coor)
                print(player.position) 