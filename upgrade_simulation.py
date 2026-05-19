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
        continue
    name = file.stem
    players[name] = {}
    #print(name, ":\n")
    #curr_round = 0
    with open(file, 'r') as f:
        for line in f:
            entry = json.loads(line)
            round_num = entry['round']
            players[name][round_num] = entry['upgrade_stats']
            players[name][round_num]['food'] = entry['game_state']['player_info']['food']

            #if the round changes, print the stats for that round (console print version)
            # if entry['round'] != curr_round:
            #     curr_round += 1
            #     print("Round ", curr_round, ":")
            #     for stat in entry['upgrade_stats']:
            #         print(stat, ":", entry['upgrade_stats'][stat], " ")
            #     print()

#plot
player_names = list(players.keys())
n_players = len(player_names)
all_rounds = sorted(set(r for p in players.values() for r in p.keys()))
x = np.arange(len(all_rounds))
width = 0.8 / len(stats_keys)

fig, axes = plt.subplots(1, len(player_names), figsize=(12, 5), sharey=True)
fig.suptitle('Player Upgrade Stats by Round')

for ax, name in zip(axes, player_names):
    for i, stat in enumerate(stats_keys):
        values = [players[name].get(r, {}).get(stat, 0) for r in all_rounds]
        offset = (i - len(stats_keys) / 2) * width + width / 2
        ax.bar(x + offset, values, width=width, label=stat)
    ax.set_title(name)
    ax.set_xlabel('Round')
    ax.set_ylabel('Value')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Round {r}' for r in all_rounds])
    ax.legend()

plt.tight_layout()
plt.show()

#display_stats()
