from game.actors import Enemy

enemies = {
    'moron': lambda: Enemy(hp=10, xp=10, name='A Moron',
                          classification='A == "x"', weakness=['Fool']),
    'asshole': lambda: Enemy(hp=10, xp=10, name='Giant Asshole',
                    classification='B == "x"',  weakness=['Alcoholic']),
    'satan': lambda: Enemy(hp=20, xp=100, name='Satan', 
                    classification='idiot == "x"', weakness=['Disingenuous']),
}