import random
import sys

class Entity(object):
    def __init__(self):
        pass
    def tick(self):
        return

class Peasants(Entity):
    def __init__(self,quality):
        self.amount = 3
        self.quality = quality
        self.speed = 4
    def tick(self):
        return self.speed * self.quality * self.amount
    def addAmount(self,amount):
        self.amount += amount
    def getAmount(self):
        return self.amount
    def setQuality(self,quality):
        self.quality = quality

class Samurai(Entity):
    def __init__(self):
        self.amount = 2
    def tick(self):
        return
    def addAmount(self,amount):
        self.amount += amount
    def roll(self):
        total = 0
        for i in range(self.amount):
            total += random.randint(1,6)
        return total
    def getAmount(self):
        return self.amount

class Daimyo(Entity):
    def __init__(self):
        self.quality = random.randint(1,3)
        self.workers = Peasants(self.quality)
        self.warriors = Samurai()
        self.coins = 0
    def tick(self):
        if self.coins < 8:
            self.quality = random.randint(2,3)
            self.workers.setQuality(self.quality)
        if self.coins > 18:
            self.quality = random.randint(1,3)
            if self.quality == 3:
                self.quality = 1
        self.coins = self.workers.tick()
        self.coins -= self.workers.getAmount() * 2 + self.warriors.getAmount() * 3 + 5
        canBuyWarrior = True
        if self.warriors.getAmount() < 3 and self.coins > 5: # Needs more warriors, defend itself before getting more peasants
            self.warriors.addAmount(1)
            self.coins -= 3
            canBuyWarrior = False
        if self.workers.getAmount() < 5 and self.coins > 12: # Buy more peasants before adding more samurai, because samurai have costs
            self.workers.addAmount(1)
            self.coins -= 5
        if self.coins > 8 and canBuyWarrior: # Buy more samurai cuz why not
            self.warriors.addAmount(1)
            self.coins -= 3
        # Add code for attacking other estates
        print ("EOT (End of Tick) %s coins" % (self.coins))
        if self.coins <= -10:
            return False # Estate Dead
        else:
            return True # Estate still Alive
    def busted(self):
        self.coins -= 5 * self.quality
        print ("busted! -%s coins" % (str(5*self.quality))) # debug

class Shogun(Entity):
    def __init__(self,playerQuality,difficulty):
        self.daimyos = []
        for i in range(5):
            self.daimyos.append(Daimyo())
        self.daimyos.append(Player(playerQuality))
        self.difficulty = difficulty
    def tick(self):
        remainingDaimyos = []
        for daimyoIndex in range(len(self.daimyos)):
            daimyo = self.daimyos[daimyoIndex-1]
            if daimyo.tick(): # Estate Alive
                remainingDaimyos.append(daimyo)
            # Suspicion & Busting an Estate
            if random.randint(1,100) < (daimyo.quality - 1) * self.difficulty * 3:
                daimyo.busted()

class Player(Daimyo):
    def __init__(self,quality):
        self.quality = quality
        self.workers = Peasants(self.quality)
        self.warriors = Samurai()
    def tick(self):
        self.coins = self.workers.tick()
        self.coins -= self.workers.getAmount() * 2 + self.warriors.getAmount() * 3 + 5
        canBuyWarrior = True
        if self.coins > -10:
            return False # Estate Dead
        else:
            return True # Estate still Alive
    def buyPeasant(self):
        if self.coins >= 5:
            self.workers.addAmount(1)
            self.coins -= 5
            return True
        else:
            return False
    def buySamurai(self):
        if self.coins >= 2:
            self.warriors.addAmount(1)
            self.coins -=2
            return True
        else:
            return False
    def sellSamurai(self):
        self.warriors.addAmount(-1)
        self.coins += 1


# UI

print ("Welcome to Japanism!")
print ("")
print ("Select a difficulty")
print ("0) Peaceful; Cannot get busted")
print ("1) Easy; Low chance of being busted")
print ("2) Normal; Medium chance of being busted")
print ("3) Hard; High chance of being busted")
print("")
try:
    diff = int(input("Select an option: "))
except ValueError:
    print ("You must type a number!",file=sys.stderror)
    sys.exit()
if not 4 > diff > -1:
    print ("You must choose a valid number!", file=sys.stderror)
    sys.exit()

print ("")
print ("Select your inital coin quality")
print ("1) High")
print ("2) Medium")
print ("3) Low")
print ("")
print ("The lower the quality, the higher the chance to get busted")
print("")
try:
    quality = int(input("Select an option: "))
except ValueError:
    print ("You must type a number!", file=sys.stderror)
    sys.exit()
if not 4 > quality > 0:
    print ("You must choose a valid number!", file=sys.stderror)
    sys.exit()

head = Shogun(quality,diff)

while True:
    k = input("tick?")
    head.tick()
    for di in range(len(head.daimyos)):
        d = head.daimyos[di-1]
        print ("daimyo has %s coins, %s samurai, and %s peasants" % (d.coins,d.warriors.amount,d.workers.amount))