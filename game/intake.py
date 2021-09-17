import pandas as pd
def split_pairs(txt):
    txt = txt.strip()
    first, second = [], []
    for phrase in txt.split(','):
        for x in compound_adjectives + compound_nouns:
            if x in phrase:
                phrase = phrase.replace(x, x.replace(' ', '_'))

        words = phrase.split()
        words = [x.strip().replace('_', ' ') for x in phrase.split()]
        if len(words) == 2:
            first += [words[0]]
            second += [words[1]]
        elif len(words) == 1:
            second += [words[0]]
        else:
            print('Not 1 or 2 words:', phrase.strip())
    return first, second
        
    
def process_raw_pairs(raw):
    lines = raw.split('\n')[::-1]
    arr = []
    while lines:
        x = lines.pop()
        if not x:
            continue
        if x.startswith('###'):
            tag = ' '.join(x.split()[1:])
            # print('Loading', tag)
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


def is_plural(word):
    return (word.endswith('men') or word.endswith('s') 
           or word in plural_exceptions)

def singularize(word):
    if word in plural_exceptions:
        return plural_exceptions[word]
    if word.endswith('ies'):
        return word[:-3] + 'y'
    if word.endswith('men'):
        return word[:-3] + 'man'
    else:
        return word[:-1]

plural_exceptions = {
    'Lice': 'Louse', 
    'Horse Thieves': 'Horse Thief',
    'Witches': 'Witch',
    'Wolves': 'Wolf',

}
compound_nouns = [
    'Errand Boys',
    'Tin Soldiers',
    'Dog Catchers',
    'Horse Thieves',
    'Political Scientists',
    'Money Changers',
    'Running Dogs',
    'Whipping Boys',
    'Street Toughs',
    'IB Coordinator',
]

compound_adjectives = [
    'Politically Illiterate',
    'Heavily Armed',
]

raw_pairs = """
### Criminal Professions
Disingenuous Hitmen, Common Thugs, Preposterous Highwaymen, Alcoholic Criminals, Jackbooted Accomplices, Ineffectual Mercenaries, Small-Time Assassins, Discount Executioners, Careless Arsonists, Malignant Squatters, Reckless Lawbreakers, Obsequious Pimps, Indiscreet Murderers, Retired Slave-Traders, Well-Fed Scoundrels, Bucktoothed Swindlers, Flesh-Eating Goons, Craven Warlords, Clumsy Villains, Embarrassing Backstabbers, Unwashed Kidnappers, Launderers, Politically Illiterate Gangsters, Crooks, Sidekicks, Henchmen, Stooges, Extortionists, Inarticulate Hoodlums, Street Toughs, Delinquents, Marauders, Blackamoors, Vandals, Carpetbaggers, Killers, Racketeers

### Lowly Professions
Incontinent Meat-Packers, Sniveling Ratcatchers,  Breastfed Academics, Kowtowing Swineherds, Apprentice Spooks, Hoity-Toity Intellectuals, Insufferable Clerks, Spineless Middle-Managers, Backwoods Trappers, Impotent Fish-Cleaners, Unwitting Peasants, Insignificant Garbagemen, Self-Satisfied Undertakers, Bearded Mystics, Dishonest Morticians, Simpering Priests, Pallid Functionaries, Melancholy Organ-Grinders, Deranged Pornographers, Ill-Tempered Philanthropists, Misinformed Yes-Men, Hairless Dignitaries, Medicated Stenographers, Orthodox Gravediggers, Dimwitted Philosophers, Dog Catchers, Shoeshiners, IB Coordinator, Comedians, Psychoanalysts, Errand Boys, Colonists, Journalists, Tin Soldiers, Hecklers, Moribund Horse Thieves, Reluctant Whipping Boys, Cold-Blooded Money Changers, Clowns

### Sexual
Disgraced Pederasts, Listless Masturbators, Limp-wristed Onanists, Daft Cuckolds, Gilded Concubines, Self-Appointed Harlots, Inept Jezebels, Reanimated Harpies, Unannounced Molestors, Armchair Philanderers, Witches, Insolent Tarts, Tufted Eunuchs, Money-Grubbing Whores

### Political
Unprincipled Marxists, Political Insects, Mistaken Demagogues, Communists, Garden-Variety Reactionaries, Diseased Collaborators, Jilted Counter-Revolutionaries, Drugstore Fascists, Dirty Trotskyites, Crass Individualists, Feather-Brained Idealists, Diabetic Maoists, Mealy-Mouthed Political Scientists, Kulaks, Capitalists, Jingoists, Baathists, Libertarians, Ultra-Rightists, Traditionalists, Centrists, Running Dogs

### Southern
Overfunded Mouth-Breathers, Backwater Racists, Ill-Bred Yokels, Oxygen-Deprived Rednecks, Prejudiced Swamp-Dwellers, Officious Transients, Fear-Mongering Cowards, Mean Turncoats, Odious Riffraff, Meddlesome Fanatics, Atrophied Sponges, Free-Range Morons, Unemployed Fetishists, Variegated Cretins, Vindictive Abusers, Synthetic Ape-Men, Asthmatic Geldings, Intellectual Centipedes, Nauseating Hypocrites, Irrelevant Bigmouths, Underqualified Drunks, Déclassé Losers, Insincere Hucksters, Unregenerate Philistines, Antediluvian Trash, Pompous Narcissists, Disorganized Pushovers, Tendentious Boobs, Scheming Crackpots, Drug-Addled Parasites, Egg-Sucking Cavemen, Low-Rent Scum

### Religious
Fraudulent Monks, Bigoted Soothsayers, Defrocked Witchdoctors, Luckless Zealots, Forsaken Apostates, Morose Cultists, White-Collar Simonists, Discredited Fakirs

### Animal
Garish Reptiles, Overpaid Invertebrates, Loathsome Creatures, Heavily Armed Baboons, Inbred Hyenas, Ill-Mannered Rats, Dyspeptic Weasels, Syphilitic Chimps, Hellhounds, Wolves, Lice, Locusts, Chickens, Dogs, Jackals, Sharks, Vultures, Loons, Snakes

### Uncategorized I
Irreligious Latecomers, Jaded Miscreants, Predatory Liars, Lonely Regurgitators, Disguised Carrion, Candy-Assed Filth, Unsuccessful Looters, Talentless Hacks, Floundering Engimas, Licentious Turds, Renegade Dwarfs, Underhanded Sinners, Deceased Tyrants, Celebrated Nincompoops, Avaricious Poltergeists, Constipated Moochers, Low-ranking Sycophants, Inveterate Plagiarizers, Cantankerous Poltroons, Impoverished Lunatics, Clamorous Weaklings, Unelected Yahoos, Despicable Bastards, Sweaty Pygmies, Gutless Traitors, Defenceless Neophytes, Sinister Halfwits, Poisonous Fools, Self-Promoting Judases, Treacherous Failures, Subservient Wimps, Botched Experiments, Powdered Fops, Monied Aristocrats, Litigious Upstarts, Ignorant Amateurs, Worm-Eaten Pilferers, Querulous Ne’er-do-wells, Solicitous Bunglers, Bankrupt Nitwits, Self-Righteous Bottom-Feeders

"""