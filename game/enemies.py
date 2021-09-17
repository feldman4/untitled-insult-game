from game.actors import Enemy

enemies = {
    'moron': lambda: Enemy(hp=10, xp=10, name='A Moron',
                           classification='A == "x"', weakness=['Fool']),
    'asshole': lambda: Enemy(hp=10, xp=10, name='Giant Asshole',
                             classification='B == "x"', weakness=['Alcoholic']),
    'satan': lambda: Enemy(hp=20, xp=100, name='Satan',
                           classification='idiot == "x"', weakness=['Disingenuous']),


    'cell': lambda: Enemy(hp=25, xp=35, name='cell',
                          classification='cell == "x"', weakness=['Dirty', 'Creature', 'Invertebrate']),
    'colleague': lambda: Enemy(hp=45, xp=90, name='Colleague Jerry',
                               classification='colleague == "x"', weakness=['Human', 'Luckless', 'Weasel', 'Lonely']),
    'computer': lambda: Enemy(hp=75, xp=180, name='Windoof XP Laptop',
                              classification='computer == "x"', weakness=['Common', 'Careless', 'Misinformed']),
    'postman': lambda: Enemy(hp=60, xp=500, name='Postman Dan',
                             classification='postman == "x"', weakness=['Loser', 'Human', 'Luckless', 'Disorganized']),
    'reviewer': lambda: Enemy(hp=150, xp=1030, name='Mrs. Licky',
                              classification='reviewer == "x"', weakness=['Traditionalist', 'Intellectual', 'Hairless',
                                                                          'Careless']),

    'beach_greg': lambda: Enemy(hp=45, xp=90, name='Beach Greg',
                               classification='beach_greg == "x"', weakness=['Human', 'Luckless', 'Weasel', 'Lonely']),
    'mall_greg': lambda: Enemy(hp=45, xp=90, name='Mall Greg',
                               classification='mall_greg == "x"', weakness=['Human', 'Luckless', 'Weasel', 'Lonely']),
    'store_greg': lambda: Enemy(hp=45, xp=90, name='Store Greg',
                               classification='store_greg == "x"', weakness=['Human', 'Luckless', 'Weasel', 'Lonely']),

}
