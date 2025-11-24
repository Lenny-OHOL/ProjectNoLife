import sys
import time
from bot_core.player_info import PlayerInfo as PI

class BotDisplay:
    """
    Basic terminal GUI used to display the bot stats. It contains the functionality to display a single of multiple bots by simply adding player info
    """
    def __init__(self, width=50, leading_whitespace=7, args=6, message_feed = []):
        self.width = width
        self.inside = width-2
        self.whitespace = leading_whitespace
        self.args = args

        self.firstUpdate = True

        self.botList: list[PI] = []

        self.message_feed = message_feed
        self.queueFeed = ['','','','']

    def addBot(self, PI):
        self.botList.append(PI)
        

    
    def update_display(self):
        # Move cursor up 2 lines
        if self.firstUpdate:
            self.firstUpdate = False
        else:
            cursor = 1 + len(self.botList)*self.args + len(self.botList) + 7

            sys.stdout.write(f'\033[{cursor}A')


        sys.stdout.write('┌%s┐\n' % ('─'*self.inside))
        # Print updated bars

        index = 0
        for i in self.botList:
            if index > 0:
                sys.stdout.write('├%s┤\n' % ('─'*self.inside))
            #botID
            sys.stdout.write('│%s%s│\n' % (i.LifeID, ' '*(self.inside - len(str(i.LifeID)))))
            #bot Name in game
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Name:{i.name}', ' '*(self.inside - len(' '*self.whitespace + f'Name:{i.name}'))))
            #bot poition from birth
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'{i.x, i.y}', ' '*(self.inside - len(' '*self.whitespace + f'{i.x, i.y}'))))
            #bot Status
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Status:{i.status}', ' '*(self.inside - len(' '*self.whitespace + f'Status:{i.status}')))) 
            #food
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Food:{i.food}/{i.food_capacity}', ' '*(self.inside - len(' '*self.whitespace + f'Food:{i.food}/{i.food_capacity}'))))
            #sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Food:{i.food}', ' '*(self.inside - len(' '*self.whitespace + f'Food:{i.food}'))))
            #mothersname
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Mother:{i.mothers_name}', ' '*(self.inside - len(' '*self.whitespace + f'Mother:{i.mothers_name}'))))            
            
            index += 1

        while self.message_feed:
            self.queueFeed.pop(0)
            self.queueFeed.append(f'{time.strftime("%H:%M:%S")}: {self.message_feed.pop(0)}')
        
        sys.stdout.write('├%s┤\n' % ('─'*self.inside))
        sys.stdout.write('│%s%s│\n' % ('Message Feed:', ' '*(self.inside - len('Message Feed:'))))
        sys.stdout.write('├%s┤\n' % (' '*self.inside))
        sys.stdout.write('│%s%s│\n' % (self.queueFeed[0], ' '*(self.inside - len(self.queueFeed[0]))))
        sys.stdout.write('│%s%s│\n' % (self.queueFeed[1], ' '*(self.inside - len(self.queueFeed[1]))))
        sys.stdout.write('│%s%s│\n' % (self.queueFeed[2], ' '*(self.inside - len(self.queueFeed[2]))))
        sys.stdout.write('│%s%s│\n' % (self.queueFeed[3], ' '*(self.inside - len(self.queueFeed[3]))))
        sys.stdout.write('└%s┘\n' % ('─'*self.inside))


        sys.stdout.flush()


if __name__ == "__main__":
# Example
    bot1 = PI()
    bot1.botID, bot1.name, bot1.food, bot1.food_capacity, bot1.mothers_name = 'Bot1', 'thomas', 6, 20, 'chelsea'
    bot2 = PI()
    bot2.botID, bot2.name, bot2.food, bot2.food_capacity, bot2.mothers_name, bot2.status = 'Bot2', 'clarence', 12, 20, 'chelsea', 'GHOST'
    progress = BotDisplay()
    progress.addBot(bot1)
    progress.addBot(bot2)
    while True:
        progress.update_display()
        time.sleep(0.05)