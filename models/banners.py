# - Banner is an object that contains 1 rare character, 3 semi rare characters, and common characters.
# Attributes:
#   - list of rare characters
#   - list of semi rare characters
#   - list of common characters

class Banner:
    def __init__(self, rare, semi, com):
        self.rare = rare
        self.semi = semi
        self.com = com
        self.chances = [1, 5, 94]

    def semi_guarantee(self):
        self.chances = [self.chances[0],
                        self.chances[1] + self.chances[2],
                        0]
    
    def rare_guarantee(self):
        self.chances = [1, 0, 0]
