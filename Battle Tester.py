

#Elemental battle simulator


class fighter:

    def __init__(self):
        self.title = "Unassigned"
        self.hp = 100
        self.sp = 100
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.magic = 0
        self.lvl = 1
        self.xp = 0
        self.element = "none"
        self.moves = []

    def choose_fighters(self):

        print("Welcome to this battle simulator!")
        print("First lets choose our fighters, press enter to continue...")
        print("The first 3 classes are 1.The Mage, 2.The Knight, 3.The Swordsman")
        choice = input("Enter the number of your choice.. 1,2,or 3?")
        player1 = choice
        player2 = input("Enter the number of your choice.. 1,2,or 3?")

        return (player1,player2)




