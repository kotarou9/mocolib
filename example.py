import mocolib
import random

config = mocolib.config

class Example(mocolib.RoomManager):

    def onInit(self):
        rooms = ['20', 'trivia']
        for room in rooms:
            self.joinRoom(room)
        self.setColor("FF0000")

    def onMessage(self, room, user, msg):
        print(room.name, user.name, msg.body)
        data = msg.body.split(" ", 1)
        if len(data) > 1:
            cmd, args = data[0], data[1]
        else:
            cmd, args = data[0], ""
        if cmd == "-say":
            room.message("%s told me to say, \"%s\"" % (user.name, args))
        elif cmd == "-dice":
            n = random.randint(1, 12)
            room.message("%s rolled, %i" % (user.name, n))
        elif cmd == "bot":
            choices = ['Hi', 'Hey', 'Sup?', 'What do you want? :|']
            msg = random.choice(choices)
            room.message(msg)

        elif cmd == "-credit":
            msg = "The library that I use is called mocolib, it was created by Kotarou. But, I am made by %s" % (config.botowner)
            room.message(msg)
            
    def onEnter(self, room, user):
        print(user.name.title() + " has entered " + room.name.title())

if __name__=="__main__":
    bot = Example()
    bot.run()