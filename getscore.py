import statsapi
from collections import defaultdict
import re

def getScores(gamePk, team):
    gamedata = statsapi.boxscore_data(gamePk)
    teambatters = str(team+'Batters')
    teamname = gamedata['teamInfo'][team]['teamName']
    boxscore = gamedata[teambatters][1:]
    # print(boxscore)
    order = 0
    scores = defaultdict(dict)
    for batter in boxscore:
        name = batter['name']
        score = int(batter['h']) + \
                int(batter['doubles']) + \
                int(batter['triples'])*2 + \
                int(batter['hr'])*3 + \
                int(batter['r']) + \
                int(batter['rbi']) + \
                int(batter['sb']) + \
                int(batter['bb']) - \
                int(batter['k'])
        lob = int(batter['lob'])
        if batter['substitution'] == True:
            scores[order]['name'].append(name)
            scores[order]['score'] += score
            scores[order]['lob'] += lob
            # print(f'-- {name}')
        else:
            order += 1
            scores[order]['name'] = [name]
            scores[order]['score'] = score
            scores[order]['lob'] = lob
            # print(f'{order}. {name}')
    
    # print(scores)
    info = gamedata[team]['info']
    # print(info)

    result = {}
    for i in range(len(info)):
        for j in range(len(info[i]['fieldList'])):
            if info[i]['fieldList'][j]['label'] in ('E','CS','GIDP'):
                text = info[i]['fieldList'][j]['value']
                text = text.rstrip('.')
                entries = [entry.strip() for entry in text.split(';')]
                # Initialize dictionary
                
                for entry in entries:
                    entry_clean = re.sub(r'\([^)]*\)', '', entry).strip()
                    # Match name and optional number
                    match = re.match(r'^(.+?)(?:\s+(\d+))?$', entry_clean)
                    if match:
                        name = match.group(1).strip()
                        number = int(match.group(2)) if match.group(2) else 1
                        # print(entry_clean, match)
                        if name in result.keys():
                            result[name] -= number
                        else:
                            result[name] = number
    # print(result)
    for player in result:
        # print(player)
        for b in scores:
            if player in scores[b]['name']:
                scores[b]['score'] -= result[player]
    # print(scores)               
        
    return teamname, scores

# game = statsapi.last_game(145)
# hometeam, homescores = getScores(game,'home')
# print(hometeam)
# print(homescores)

def showScores(team, scores):
    print('-'*39)
    print(f"{'':2}| {team:25} | {'':5} |")
    print('-'*39)
    print(f"{'':2}| {'Player':25} | {'Score':3} |")
    print('-'*39)
    for s in scores:
        print(f"{s:2}| {'; '.join(scores[s]['name']):25} | {scores[s]['score']:5} |")
        print('-'*39)