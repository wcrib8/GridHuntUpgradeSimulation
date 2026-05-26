import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

folder = Path("SaveData")
stats_keys = ['reload', 'resistance', 'speed', 'vision', 'food']

# collect data
# go through each file in folder, then print stats for each round for that player
players = {}
for file in folder.glob('*.jsonl'):
    if file.stem == 'game_params':
        with open(file, 'r') as f:
            game_map = json.load(f)['map_name']
            continue
    name = file.stem
    players[name] = {}

    with open(file, 'r') as f:
        # iterate through each json line in file to find stat changes
        for line in f:
            entry = json.loads(line)
            round_num = entry['round']     # get stats for each round
            stats = {**entry['upgrade_stats'], 'food': entry['game_state']['player_info']['food']}  # combine upgrade stats and food into one dict
            if round_num not in players[name]:
                # if the round is not in the player's stats, add it with the current stats as both min and max
                players[name][round_num] = {
                    stat: {'min': stats[stat], 'max': stats[stat]} for stat in stats_keys
                }
            else:
                # track max and min to see the difference in stats, also show degraded stats
                for stat in stats_keys:
                    players[name][round_num][stat]['min'] = min(players[name][round_num][stat]['min'], stats[stat])
                    players[name][round_num][stat]['max'] = max(players[name][round_num][stat]['max'], stats[stat])


#plot
player_names = list(players.keys())
n_players = len(player_names)
all_rounds = sorted(set(r for p in players.values() for r in p.keys()))
x = np.arange(len(all_rounds))
width = 0.8 / len(stats_keys)

fig, axes = plt.subplots(1, len(player_names), figsize=(12, 5), sharey=True)
fig.suptitle(f'Player Upgrade Stats by Round\nGame Map: {game_map}')

for ax, name in zip(axes, player_names):
    for i, stat in enumerate(stats_keys):
        min_values = [players[name].get(r, {}).get(stat, {}).get('min', 0) for r in all_rounds]
        max_values = [players[name].get(r, {}).get(stat, {}).get('max', 0) for r in all_rounds]
        offset = (i - len(stats_keys) / 2) * width + width / 2
        ax.bar(x + offset, max_values, width=width, label=f'{stat}')
        ax.bar(x + offset, min_values, width=width, hatch='///', color='white', alpha=0.25)
    ax.set_title(name)
    ax.set_xlabel('Round')
    ax.set_ylabel('Value')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Round {r}' for r in all_rounds])
    ax.legend()

plt.tight_layout()
plt.show()
