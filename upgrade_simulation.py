import json
from pathlib import Path

folder = Path("SaveData")

# load data
def display_stats():
    all_stats = []
    # go through each file in folder, then print stats for each round for that player
    for file in folder.glob('*.jsonl'):
        name = file.stem
        #name = []
        print(name, ":\n")
        #file.player_name
        curr_round = 0
        with open(file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                #name.append(json.loads(line))

                # if the round changes, print the stats for that round
                if entry['round'] != curr_round:
                    curr_round += 1
                    print("Round ", curr_round, ":")
                    for stat in entry['upgrade_stats']:
                        print(stat, ":", entry['upgrade_stats'][stat], " ")
                    print()

        #all_stats.append(name)
    return
    

# go through dictionary of save data for each player
# list each of that player's stats for each round

# def display_stats(stats_dic):
#     for player in stats_dic:
#         print(player, " ")
#     print('\n')
#     # for num of rounds, print each player's stats?

display_stats()
