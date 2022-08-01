import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from scipy import stats


class Match:
    def __init__(self, game, maps, player_scores):
        self.game = game
        self.maps = maps
        self.player_scores = player_scores


class Map:
    def __init__(self, name, players):
        self.name = name
        self.players = players


class Player:
    def __init__(self, name, statistic, score):
        self.name = name
        self.statistic = statistic
        self.score = score


class Statistic:
    def __init__(self, name, value, score):
        self.name = name
        self.value = value
        self.score = score


def calc():
    statsOfInterest = ["Final Blows", "Eliminations", "Hero Damage Done", "Healing Done", "Deaths"]
    multipliers = [1, 0.5, 0.001, 0.001, -0.5]
    df = pd.read_csv('/content/drive/MyDrive/phs_2021_final.csv', low_memory=False)
    
    df.drop(['start_time', 'tournament_title', 'map_type', 'team_name'], axis=1, inplace=True)
    games = []
    for index, row in df.iterrows():
        newGame = Match(row[0], [], [])
        gameFound = 0
        for eachGame in games:
            if eachGame.game == newGame.game:
                gameFound = 1
                break
            else:
                continue
        if gameFound == 0:
            games.append(newGame)
    for index, row in df.iterrows():
        newMap = Map(row[1], [])
        for eachGame in games:
            if eachGame.game == row[0]:
                mapFound = 0
                for eachMap in eachGame.maps:
                    if eachMap.name == newMap.name:
                        mapFound = 1
                        break
                    else:
                        continue
                if mapFound == 0:
                    eachGame.maps.append(newMap)
                break

    for index, row in df.iterrows():
        newPlayer = Player(row[2], [], 0)
        for eachGame in games:
            if eachGame.game == row[0]:
                for eachMap in eachGame.maps:
                    if eachMap.name == row[1]:
                        playerFound = 0
                        for eachPlayer in eachMap.players:
                            if eachPlayer.name == newPlayer.name:
                                playerFound = 1
                                break
                            else:
                                continue
                        if playerFound == 0:
                            eachMap.players.append(newPlayer)
                        break
                break

    for index, row in df.iterrows():
        newStat = Statistic(row[3], row[5], [])
        newPlayerScore = Player(row[2], None, [0, 0, 0])
        index = 0
        score = 0
        for eachStatOfInterest in statsOfInterest:
            if row[3] == eachStatOfInterest:
                score = multipliers[index]*row[5];
            index += 1
        newStat.score = score
        for eachGame in games:
            if eachGame.game == row[0]:
                for eachMap in eachGame.maps:
                    if eachMap.name == row[1]:
                        for eachPlayer in eachMap.players:
                            playerScoreFound = 0
                            if eachPlayer.name == row[2]:
                                eachPlayer.statistic.append(newStat)
                        break
                break

    for eachGame in games:
        #print(eachGame.game)
        for eachMap in eachGame.maps:
            #print(f"  {eachMap.name}")
            for eachPlayer in eachMap.players:
                score = 0
                for eachStat in eachPlayer.statistic:
                    score += eachStat.score
                eachPlayer.score = score
                #print(f"    {eachPlayer.name} {eachPlayer.score}")

    for eachGame in games:
        for eachMap in eachGame.maps:
            for eachPlayer in eachMap.players:
                newPlayerScore = Player(eachPlayer.name, None, [eachPlayer.score, 0, 0])
                playerFound = 0
                playerScoreIndex = 0
                for eachPlayerScore in eachGame.player_scores:
                    if eachPlayer.name == eachPlayerScore.name:
                        playerFound = 1
                        minIndex = 0
                        minValue = 999999999999999
                        index = 0
                        for eachScore in eachGame.player_scores[playerScoreIndex].score:
                            if eachScore < minValue:
                                minValue = eachScore
                                minIndex = index
                            if index == 2:
                                break
                            index += 1
                        if eachPlayer.score > eachGame.player_scores[playerScoreIndex].score[minIndex]:
                            eachGame.player_scores[playerScoreIndex].score[minIndex] = eachPlayer.score
                    else:
                        playerScoreIndex += 1
                if playerFound == 0:
                    eachGame.player_scores.append(newPlayerScore)
    """
    for eachGame in games:
        for eachPlayerScore in eachGame.player_scores:
            for eachScore in eachPlayerScore.score:
                print(f"{eachPlayerScore.name} {eachScore}")
    """

    all_players = df['player_name'].unique()

    summed_scores = []
    for eachGame in games:
        for eachPlayerScore in eachGame.player_scores:
            summed_scores.append(Player(eachPlayerScore.name, None, sum(eachPlayerScore.score)))

    final_scores = []
    for player in all_players:
        maxScore = 0
        for eachScore in summed_scores:
            if eachScore.name == player:
                if eachScore.score > maxScore:
                    maxScore = eachScore.score
        final_scores.append(Player(player, None, maxScore))

    for value in final_scores:
        print(f"{value.name} {value.score}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    calc()
