import pandas as pd
def split_pairs(txt):
    txt = txt.strip()
    first, second = [], []
    for phrase in txt.split(','):            
        words = [x.strip() for x in phrase.split()]
#         print(len(words))
        if len(words) == 2:
            first += [words[0]]
            second += [words[1]]
        elif len(words) == 1:
            second += [words[0]]
        else:
            print('Not 1 or 2 words:', phrase.strip())
    return first, second
        
    
def process_raw(raw):
    lines = raw.split('\n')[::-1]
    arr = []
    while lines:
        x = lines.pop()
        if not x:
            continue
        if x.startswith('###'):
            tag = ' '.join(x.split()[1:])
            print('Loading', tag)
        adjectives, nouns = split_pairs(lines.pop())
        for a in adjectives:
            arr += [{'rule': 'vocabulary', 'input': 'A', 'output': a, 'source': tag}]

        for n in nouns:
            if is_plural(n):
                symbol = 'NP'
                arr += [{'rule': 'vocabulary', 'input': symbol, 'output': n, 'source': tag}]
                symbol = 'N'
                arr += [{'rule': 'vocabulary', 'input': symbol, 'output': singularize(n), 'source': tag}]
            else:
                symbol = 'N'
                arr += [{'rule': 'vocabulary', 'input': symbol, 'output': n, 'source': tag}]
    return pd.DataFrame(arr)

exceptions = {'Lice': 'Louse'}

def is_plural(word):
    return word.endswith('men') or word.endswith('s') or word in exceptions

def singularize(word):
    if word in exceptions:
        return exceptions[word]
    if word.endswith('ies'):
        return word[:-3] + 'y'
    if word.endswith('men'):
        return word[:-3] + 'man'
    else:
        return word[:-1]

raw = """
### Criminal Professions
Disingenuous Hitmen, Common Thugs, Preposterous Highwaymen, Alcoholic Criminals, Jackbooted Accomplices, Ineffectual Mercenaries, Small-Time Assassins, Rented Executioners, Careless Arsonists, Malignant Squatters, Reckless Lawbreakers, Obsequious Pimps, Indiscreet Murderers, Retired Slave-Traders, Well-Fed Scoundrels, Bucktoothed Swindlers, Flesh-Eating Goons, Craven Warlords, Clumsy Villains, Embarrassing Backstabbers, Unwashed Kidnappers, Cabal Of Man-Hunters, Launderers, Politically Illiterate Gangsters, Crooks, Sidekicks, Henchmen, Stooges, Extortionists, Hoodlums, Street Toughs, Delinquents, Marauders, Blackamoors, Vandals, Carpetbaggers, Killers, Racketeers

### Lowly Professions
Incontinent Meat-Packers, Sniveling Ratcatchers,  Breastfed Academics, Kowtowing Swineherds, Apprentice Spooks, Hoity-Toity Intellectuals, Insufferable Clerks, Spineless Middle-Managers, Backwoods Trappers, Impotent Fish-Cleaners, Unwitting Peasants, Insignificant Garbagemen, Self-Satisfied Undertakers, Bearded Mystics, Dishonest Morticians, Simpering Priests, Pallid Functionaries, Melancholy Organ-Grinders, Deranged Pornographers, Ill-Tempered Philanthropists, Misinformed Yes-Men, Hairless Dignitaries, Medicated Stenographers, Orthodox Gravediggers, Dimwitted Philosophers, Dog Catchers, A Circle Of Coke-Sniffing Adulterers, Shoeshiners, IB Coordinator, Comedians, Psychoanalysts, Errand Boys, Colonists, Journalists, Tin Soldiers, Hecklers, Moribund Horse Thieves,  Reluctant Whipping Boys, Cold-Blooded Money Changers, Sniggering Wine Merchants, 

### Sexual
Disgraced Pederasts, Listless Masturbators, Limp-wristed Onanists, Daft Cuckolds, Gilded Concubines, Self-Appointed Rapists, Harlots, Witches, Tarts, Jezebels, Harpies, Molestors, Philanderers, Syndicate Of Rapists, 

### Political
Unprincipled Marxists, Political Insects, Mistaken Demagogues, Closet Communists, Garden-Variety Reactionaries, Diseased Collaborators, Jilted Counter-Revolutionaries, Drugstore Fascists, Dirty Trotskyites, Crass Individualists, Feather-Brained Idealists, Kulaks, Peddlers Of Ideological Mildew, Capitalists, Jingoists, Baathists, Libertarians, Maoists, Sympathizers, Ultra-Rightists, Traditionalists, Centrists, Running Dogs, Mealy-Mouthed Political Scientists

### Southern
Overfunded Mouth-Breathers, Backwater Racists, Ill-Bred Yokels, Oxygen-Deprived Rednecks, Prejudiced Swamp-Dwellers, Officious Transients, Fear-Mongering Cowards, Mean Turncoats, Odious Riffraff, Meddlesome Fanatics, Armchair Rapists, Atrophied Sponges, Free-Range Morons, Unemployed Fetishists, Variegated Cretins, Vindictive Abusers, Synthetic Ape-Men, Asthmatic Geldings, Intellectual Centipedes, Nauseating Hypocrites, Irrelevant Bigmouths, Underqualified Drunks, Bankrupt Losers, Insincere Hucksters, Unregenerate Philistines, Antediluvian Trash, Pompous Narcissists, Disorganized Pushovers, Tendentious Boobs, Scheming Crackpots, Drug-Addled Parasites, Egg-Sucking Cavemen, Human Scum, Infrequent Bathers, 

### Religious
Fraudulent Monks, Bigoted Soothsayers, Defrocked Witchdoctors, Luckless Zealots, Forsaken Apostates, Morose Cultists, White-Collar Simonists, Fakirs

### Animal
Garish Reptiles, Overpaid Invertebrates, Loathsome Creatures, Heavily Armed Baboons, Simian, Porcine, Snakes, Dogs, Rats, Hyenas, Jackals, Sharks, Vultures, Loons, Weasels, Hellhounds, Wolves, Chimps, Lice, Locusts

"""