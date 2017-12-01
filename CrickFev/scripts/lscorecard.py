import requests
import sys
import click
from bs4 import BeautifulSoup as BS

url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
r = requests.get(url)
soup = BS(r.text, "html.parser")
tableHeads = soup.find_all('div', {'class' : 'match-section-head'})
tableData = soup.find_all('section', {'class' : 'matches-day-block'})


def getScoreCard(url,meta):
    print(("\n" + "*"*100))
    
    r1 = requests.get(url)
    soup = BS(r1.text,'html.parser')

    details = soup.find_all("tbody")
    
    batsman_data = [["Batsman","Runs","Balls","Fours","Six","S/R"]]
    bowler_data = [["Bowler","Over","Maiden","Runs","Wkts","Economy"]]

    for rows in details[0]:
        tds = rows.find_all("td")
        batsman_data.append(tds)

    for rows in details[1]:
        tds = rows.find_all("td")
        bowler_data.append(tds)

    if len((batsman_data[0])[0])<25:
    		(batsman_data[0])[0] +=" "*(25-len((batsman_data[0])[0]))
    (batsman_data[0])[1] +=" "*(4-len((batsman_data[0])[1]))
    (batsman_data[0])[2] +=" "*(5-len((batsman_data[0])[2]))
    (batsman_data[0])[3] +=" "*(4-len((batsman_data[0])[3]))
    (batsman_data[0])[4] +=" "*(4-len((batsman_data[0])[4]))
    (batsman_data[0])[5] +=" "*(4-len((batsman_data[0])[5]))

    print(((batsman_data[0])[0]+"\t"+(batsman_data[0])[1]+"\t"+(batsman_data[0])[2]+"\t"+(batsman_data[0])[3]+"\t"+(batsman_data[0])[4]+"\t"+(batsman_data[0])[5]))

#Print the Values of the Batsmen Playing
    for j in range(1,3):
        playerName = (batsman_data[j])[0].a.string
        playerScore = (batsman_data[j])[1].string
        ballsFaced = (batsman_data[j])[2].string
        fours = (batsman_data[j])[3].string
        six = (batsman_data[j])[4].string
        sr = (batsman_data[j])[5].string

        if len(playerName)<25:
            playerName +=" "*(25-len(playerName))

        if len(playerScore)<4:
            playerScore +=" "*(4-len(playerScore))
        if len(ballsFaced)<5:
            ballsFaced +=" "*(5-len(ballsFaced))
        if len(fours)<4:
            fours +=" "*(4-len(fours))
        if len(six)<4:
            six +=" "*(4-len(six))
        if len(sr)<4:
            sr +=" "*(4-len(sr))

        print((playerName + "\t"+playerScore+"\t"+ballsFaced+"\t"+fours+"\t"+six+"\t"+sr))

    print(("\n"+"*"*70))

    if len((bowler_data[0])[0])<25:
    		(bowler_data[0])[0] +=" "*(25-len((bowler_data[0])[0]))
    (bowler_data[0])[1] +=" "*(4-len((bowler_data[0])[1]))
    (bowler_data[0])[2] +=" "*(5-len((bowler_data[0])[2]))
    (bowler_data[0])[3] +=" "*(4-len((bowler_data[0])[3]))
    (bowler_data[0])[4] +=" "*(4-len((bowler_data[0])[4]))
    (bowler_data[0])[5] +=" "*(4-len((bowler_data[0])[5]))

    print(((bowler_data[0])[0]+"\t"+(bowler_data[0])[1]+"\t"+(bowler_data[0])[2]+"\t"+(bowler_data[0])[3]+"\t"+(bowler_data[0])[4]+"\t"+(bowler_data[0])[5]))

#Print the values of Bowlers data
    for j in range(1,3):
        name = (bowler_data[j])[0].a.string
        over = (bowler_data[j])[1].string
        maid = (bowler_data[j])[2].string
        runs = (bowler_data[j])[3].string
        wkt = (bowler_data[j])[4].string
        eco = (bowler_data[j])[5].string

        if len(name)<25:
            name +=" "*(25-len(name))

        over +=" "*(5-len(over))
        maid +=" "*(4-len(maid))
        runs +=" "*(4-len(runs))
        wkt  +=" "*(4-len(wkt))
        eco +=" "*(4-len(eco))

        print((name +"\t"+over+"\t"+maid+"\t"+runs+"\t"+wkt+"\t"+eco))
       
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


        url2 =  matches[ch-1].find_all('div')[4].find_all('a')[0]['href'] + "?view=scorecard"
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

        
        print (meta)
        getScoreCard(url2, meta)
