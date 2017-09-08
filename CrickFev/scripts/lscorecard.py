import requests
import sys
import click
from bs4 import BeautifulSoup as BS

url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
r = requests.get(url)
soup = BS(r.text, "html.parser")
tableHeads = soup.find_all('div', {'class' : 'match-section-head'})
tableData = soup.find_all('section', {'class' : 'matches-day-block'})

def getBowlingTables(text):
    text = text.split('\n')
    all_bowlers = []

    for line_number in range(0, len(text)):
        if '<table width="100%" class="bowling-table">' in text[line_number]:
            newTable = []
            while '</table>' not in text[line_number]:
                line_number += 1
                if '<td class="bowler-name">' in text[line_number]:
                    newBowler = []
                    newBowler.append(text[line_number].split('>')[-3].split('<')[0])		#playerName
                    for ix in range(1, 6):
                        newBowler.append(text[line_number+ix].split('<td>')[1].split('</td>')[0])
                    newTable.append(newBowler)
            all_bowlers.append(newTable)

    return all_bowlers


def getScoreCard(url, meta):

        print("\n" + "*"*100)

        r=requests.get(url)
        soup=BS(r.text, "html.parser")

        summary = soup.find('div', {'class' : 'match-information-strip'}).text.split(',')
        summary[-2] = summary[-2] + ',' + summary[-1]

        for ix in range(0, len(summary)-1):
            summary[ix] = summary[ix].strip()
            print summary[ix]
        print('\n' + meta)

        inningsBat = soup.find_all('table', {'class':'batting-table innings'})
        inningsBowl = getBowlingTables(r.text)

        for ix in range(0, len(inningsBat)):
            print("\n" + "-" * 100)

            rows = inningsBat[ix].find_all('tr')

            try:
                playerData = rows[len(rows) - 2].find_all('td')
                playerName = playerData[1].text
            except:
                continue

            inningHead = rows[0].find_all('th')[1].text.split('innings', 1)[0] + 'Innings'
            if len(inningHead) < 60:
                inningHead += " " * (60 - len(inningHead))
            print("\n" + inningHead + "\t" + "Runs" + "\t"+ "Balls" + "\t" + "Strike Rate" + "\n")

            for px in range(1, len(rows)-2, 2):
                playerData = rows[px].find_all('td')
                playerName = playerData[1].text
                if len(playerName)<25:
                    playerName += " " * (25 - len(playerName))
                dismissalMode = playerData[2].text
                if len(dismissalMode) < 35:
                    dismissalMode += " " * (35 - len(dismissalMode))
                runs = playerData[3].text
                if len(runs) < 4:
                    runs += " " * (4 - len(runs))
                balls = playerData[len(playerData) - 4].text
                if len(balls) < 5:
                    balls += " " * (5 - len(balls))
                print(playerName + dismissalMode + "\t" + runs + "\t" + balls + "\t" + playerData[len(playerData)-1].text)

            playerData = rows[len(rows) - 2].find_all('td')
            playerName = playerData[1].text
            playerName += " "*(25 - len(playerName))
            dismissalMode = playerData[2].text
            if len(dismissalMode) < 35:
                dismissalMode += " "*(35 - len(dismissalMode))
            runs = playerData[3].text
            if len(runs)<4:
                runs += " "*(4-len(runs))
            print("\n" + playerName + dismissalMode + "\t" + runs)

            playerData = rows[len(rows) - 1].find_all('td')
            playerName = playerData[1].text
            playerName += " "*(25 - len(playerName))
            dismissalMode = playerData[2].text
            if len(dismissalMode) < 35:
                dismissalMode += " "*(35 - len(dismissalMode))
            runs = playerData[3].text
            if len(runs) < 4:
                runs += " " * (4 - len(runs))
            print(playerName + dismissalMode + "\t" + runs + "\t" + playerData[4].text)

            print "_" * 20

            inningHead = 'Bowling'
            inningHead += " " * (30 - len(inningHead))
            print("\n" + inningHead + "\t" + "Overs" + "\t" "Maidens" + "\t" + "Runs" + "\t" + "Wickets" + "\t" + "Economy" + "\n")

            for row in range(len(inningsBowl[ix])):
                playerName = str(inningsBowl[ix][row][0])
                if len(playerName)<30:
                    playerName += " "*(30-len(playerName))
                overs = str(inningsBowl[ix][row][1])
                if len(overs)<5:
                    overs += " "*(5-len(overs))
                maidens = str(inningsBowl[ix][row][2])
                if len(maidens)<7:
                    maidens += " "*(7-len(maidens))
                runs = str(inningsBowl[ix][row][3])
                if len(runs)<4:
                    runs += " "*(4-len(runs))
                wickets = str(inningsBowl[ix][row][4])
                if len(wickets)<7:
                    wickets += " "*(7-len(wickets))
                economy = str(inningsBowl[ix][row][5])
                print(playerName + "\t" + overs + "\t" + maidens + "\t" + runs + "\t" + wickets + "\t" + economy)





@click.command()
@click.option('--em', nargs=2, type=int, help='first arg for event number and second for match')

def main(em):

        ch = em[0]

        if ch > 0:
            global matches
            matches = tableData[ch-1].find_all('section', {'class' : 'default-match-block'})

        else:
            matches = tableData[0].find_all('section', {'class' : 'default-match-block'})
            for ix in range(1, len(tableData)):
                matches = matches + tableData[ix].find_all('section', {'class':'default-match-block'})

        ch = em[1]

        try:
            temp = matches[ch-1]
        except (IndexError, ValueError):
            print("Invalid choice\n")
            exit()


        url2 = "http://www.espncricinfo.com" + matches[ch-1].find_all('div')[4].find_all('a')[0]['href'] + "?view=scorecard"
        matchDetails = matches[ch-1].find_all('div')
        team1 = str(matchDetails[1].text.split('\n',1)[1].split(' ')[0])
        if len(str(matchDetails[1].text.split('\n',1)[1].split(' ')[1]))>0:
            team1 = team1 + " " + str(matchDetails[1].text.split('\n',1)[1].split(' ')[1])
        score1 = str(matchDetails[1].find('span').text)
        if len(str(matchDetails[1].text.split('\n',1)[1].split(' ')[2]))>0:
            team1 = team1 + " " + str(matchDetails[1].text.split('\n',1)[1].split(' ')[2])
        score2 = str(matchDetails[2].find('span').text)

        team2 = str(matchDetails[2].text.split('\n',1)[1].split(' ')[0])
        if len(str(matchDetails[2].text.split('\n',1)[1].split(' ')[1]))>0:
            team2 = team2 + " " + str(matchDetails[2].text.split('\n',1)[1].split(' ')[1])
        if len(str(matchDetails[2].text.split('\n',1)[1].split(' ')[2]))>0:
            team2 = team2 + " " + str(matchDetails[2].text.split('\n',1)[1].split(' ')[2])

        meta = "\t" + team1 + ": " + score1 + "\n\t" + team2 + ": " + score2
        meta += "\n\n" + matchDetails[3].text.split('\n')[1]


        getScoreCard(url2, meta)
