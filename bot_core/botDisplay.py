import sys
import time
from botMethods.playerInfo import playerInfo as PI

class botDisplay:
    """
    Basic terminal GUI used to display the bot stats. It contains the functionality to display a single of multiple bots by simply adding player info
    """
    def __init__(self, width=50, leading_whitespace=7, args=6, messageFeed = []):
        self.width = width
        self.inside = width-2
        self.whitespace = leading_whitespace
        self.args = args

        self.firstUpdate = True

        self.botList: list[PI] = []

        self.messageFeed = messageFeed
        self.queueFeed = ['','','','']

    def addBot(self, PI):
        self.botList.append(PI)
        

    
    def update(self):
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
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Food:{i.food}/{i.foodCapacity}', ' '*(self.inside - len(' '*self.whitespace + f'Food:{i.food}/{i.foodCapacity}'))))
            #sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Food:{i.food}', ' '*(self.inside - len(' '*self.whitespace + f'Food:{i.food}'))))
            #mothersname
            sys.stdout.write('│%s%s│\n' % (' '*self.whitespace + f'Mother:{i.mothersName}', ' '*(self.inside - len(' '*self.whitespace + f'Mother:{i.mothersName}'))))            
            
            index += 1

        while self.messageFeed:
            self.queueFeed.pop(0)
            self.queueFeed.append(f'{time.strftime("%H:%M:%S")}: {self.messageFeed.pop(0)}')
        
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
    bot1.botID, bot1.name, bot1.food, bot1.foodCapacity, bot1.mothersName = 'Bot1', 'thomas', 6, 20, 'chelsea'
    bot2 = PI()
    bot2.botID, bot2.name, bot2.food, bot2.foodCapacity, bot2.mothersName, bot2.status = 'Bot2', 'clarence', 12, 20, 'chelsea', 'GHOST'
    progress = botDisplay()
    progress.addBot(bot1)
    progress.addBot(bot2)
    while True:
        progress.update()
        time.sleep(0.05)