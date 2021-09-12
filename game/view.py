import numpy as np
from curtsies.fmtfuncs import red, blue, bold, green, on_blue, yellow, cyan, magenta
from curtsies import FSArray


def view(model, window):
    m = model
    h, w = window.height, window.width
    a = FSArray(h, w)
    with open('logs/term', 'w') as fh:
        print('model', m['view_template'], file=fh)

    blank = red(' '*w)
    horizontal_line = red('-' * w)

    front = m['view_template'].format(buffer=m['buffer'], choices=' '.join(m['candidates']))
    rows = [green(x) for x in front.split('\n')]
    rows += [blank]
    rows += [blank]
    rows += [horizontal_line]
    rows += [red(x) for x in format_history(m['history'])]
    rows += [blue('socket dead' if m['socket'] == None else 'socket alive')]

    for i, row in enumerate(rows):
        # limit width to match terminal
        row = row[:w]
        a[i, :row.width] = [row]
    window.render_to_terminal(a)



def format_history(history):
    frame, timeline = history
    if frame == -1:
        rows = [f'FRAME: {len(timeline)}']
    else:
        rows = [f'FRAME: {frame + 1}/{len(timeline)}']

    formatted = [f'[{i}] {msg}' for i, msg in enumerate(timeline)]
    past = formatted if frame == -1 else formatted[:frame]
    future = [] if frame == -1 else formatted[frame:]

    rows += ['PAST: ' +  ' '.join(past[-3:][::-1])]
    rows += ['FUTURE: ' +  ' '.join(future[:3])]

    return rows


def view_old(model, window):
    m = model
    h, w = window.height, window.width
    a = FSArray(h, w)
    with open('logs/term', 'a') as fh:
        print('model', m, file=fh)
    blank = red(' '*w)
    horizontal_line = magenta('-' * w)
    rows = [
        blank,
        blank,
        horizontal_line,
        red(m['description']),
        blank,
        green(m['buffer']),
        green('OPTIONS: ' + ' '.join(m['candidates'])),
        horizontal_line,
        green('--- your self-respect ---'),
        green('{header}'.format(**model)),
        green('-------------------------'),
        blank,
        blank,
        # red('LOG: ' + m['log']),
    ]
    rows += [red(x) for x in format_history(m['history'])]
    rows += [blue('socket dead' if m['socket'] == None else 'socket alive'),]
    for i, row in enumerate(rows):
        # limit width to match terminal
        row = row[:w]
        a[i, :row.width] = [row]
    window.render_to_terminal(a)



def make_health_bar(actor, width=23):
    health = actor.hp / actor.max_hp
    positive_health = max(int(np.ceil(health * width)), 0)
    health_bar = '█' * positive_health + ' ' * (width - positive_health)
    health_bar = '|' + health_bar + '|'
    return health_bar



def create_choice_template(player, level_name, description):
    view_string = """

{level_name}
{description}



{{buffer}}
------------------------------------------------------------
{player_name}
{player_health}

Your Choice: {{choices}}
    """
    width = max(len(x) for x in view_string.split('\n'))
    return view_string.format(
        level_name=level_name.center(width, '-'),
        description=description,
        player_name=' ' + player.name,
        player_health=make_health_bar(player),

    )


### NEXT FUNCTION


def create_battle_template(player, enemy, description):
    view_string = """
{enemy_name}
{enemy_health}
------------------------------------------------------------
{description}



{{buffer}}
------------------------------------------------------------
{player_name}
{player_health}

Words: {{choices}}
"""[1:-1]
    width = max(len(x) for x in view_string.split('\n'))
    return view_string.format(
        enemy_name=(enemy.name + ' ').rjust(width), 
        enemy_health=make_health_bar(enemy).rjust(width),
        description=description,
        player_name=' ' + player.name,
        player_health=make_health_bar(player),
    )