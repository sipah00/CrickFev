import requests
import sys
import click
from bs4 import BeautifulSoup as BS


url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
r = requests.get(url)
soup = BS(r.text, "html.parser")
tableHeads = soup.find_all('div', {'class' : 'match-section-head'})
tableData = soup.find_all('section', {'class' : 'matches-day-block'})
team_matches = []
team = ''


def getScore(ch):
        try:
            temp = tableData[ch - 1]
        except (IndexError, ValueError):
            click.secho("Please choose right choice.", fg='red')
            exit()

        if ch > 0:
            global matches
            matches = tableData[ch-1].find_all('section', {'class' : 'default-match-block'})
        else:
            matches = tableData[0].find_all('section', {'class' : 'default-match-block'})
            for ix in range(1, len(tableData)):
                matches = matches + tableData[ix].find_all('section', {'class':'default-match-block'})

        for ix in range(0,len(matches)):

                matchDetails = matches[ix].find_all('div')

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

                headerline = "Match " + str(ix+1) + ": " + team1 + " vs " + team2
                headerline += (" " * (75 - len(headerline)))

                if team in ['', team1.lower(), team2.lower()]:
                    team_matches.append(ix+1)
                    click.secho(headerline + "\t\t(" + str(matchDetails[0].find('span', {'class':'bold'}).text) +")", fg='red')
                    click.secho(str(matchDetails[0].find('span', class_='match-no').a.text.split('     ',1)[1]), fg='green')
                    click.secho("\t" + team1 + " "*(20-len(team1)) +"| " + score1 + "\n\t" + team2 + " "*(20-len(team2)) +"| " + score2, fg='blue')
                    click.secho("\t" + matchDetails[3].text.split('\n')[1], fg='blue')

                click.echo("\n")



@click.command()
@click.option('--ch', default=0, type=int, help='choose any event')

def main(ch):
    click.clear()
    getScore(ch)



