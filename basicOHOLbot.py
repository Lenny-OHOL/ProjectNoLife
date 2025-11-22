from bot_core.botActions import botActions

import time

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


    player = botActions(email, accountKey, tutorial_number=0, show_display=True)
    #player = botActions(email, accountKey, host='bigserver2.onehouronelife.com', tutorial_number)

    time.sleep(2)
    player.BasicAction('move', 'down')
    time.sleep(2)
    player.BasicAction('move', 'down')
    time.sleep(2)
    player.BasicAction('move', 'up')
    time.sleep(2)
    player.BasicAction('move', 'up')
    time.sleep(2)
    player.BasicAction('move', 'left')
    time.sleep(2)
    player.BasicAction('move', 'right')







    time.sleep(200000)

    player.basicAction('USE')
    time.sleep(2)
    player.basicAction('SELF')
    time.sleep(2)
    player.basicAction('SELF')
    time.sleep(2)
    player.basicMovement('Left')
    player.basicMovement('Left')
    player.basicMovement('Left')
    time.sleep(2)
    player.basicMovement('Down')
    time.sleep(2)
    player.basicMovement('Down')
    time.sleep(2)
    player.basicMovement('Down')
    time.sleep(2)
    player.basicMovement('Down')
    player.basicMovement('Down')
    player.basicMovement('Down')
    player.basicMovement('Down')
    player.basicAction('USE')
    player.basicAction('SELF')
    #player.botBasicMovement('Left')
    #player.botBasicMovement('Left')
    #player.botBasicMovement('Left')
    #player.botBasicMovement('Left')


if __name__ == "__main__":
    main()