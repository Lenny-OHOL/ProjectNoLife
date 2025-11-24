from bot_core.botActions import botActions

import time

open_second_tutorial_door = [
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'right'),
        ('move', 'down'),
        ('use', 'down'),
        ('move', 'down'),
        ('move', 'down'),
]


def main():
    email = ''
    accountKey = ''
    try:
         with open('email.ini', 'r') as file:
             email = file.read()
    except FileNotFoundError:
        print('missing email.ini')
        return

    try:
         with open('accountKey.ini', 'r') as file:
             accountKey = file.read()
    except FileNotFoundError:
        print('missing email.ini')
        return


    player = botActions(email, accountKey, tutorial_number=1, show_display=True)
    #player = botActions(email, accountKey, host='bigserver2.onehouronelife.com', tutorial_number)

    for action in open_second_tutorial_door:
        time.sleep(1)
        player(*action)

    #Random actions

    time.sleep(2)
    player('say', 'i am perfect')

    time.sleep(2)
    player('use')
    time.sleep(2)
    player('drop')
    time.sleep(2)
    player('move', 'down')
    time.sleep(2)
    player('move', 'down')
    time.sleep(2)
    player('move', 'up')
    time.sleep(2)
    player('move', 'up')
    time.sleep(2)
    player('move', 'left')
    time.sleep(2)
    player('move', 'right')

    return


if __name__ == "__main__":
    main()