#! /usr/bin/env python3
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import re
import sys

# ORDINE ELEMENTI (in tutte le liste seguenti): w, f, sf, qf [, of]
rd_points = []
results = []
predict = []

def get_tourn_round_points():
    tourn_img =  browser.find_element_by_css_selector('.tourney-badge-wrapper > img')
    tourn_category = re.findall(r'\d+', tourn_img.get_attribute('src').split('/')[-1])[0]
    points_distribution = {'250': [250, 150, 90, 45], '500': [500, 300, 180, 90], '1000': [1000, 600, 360, 180, 90]}
    rd_points.extend(points_distribution[tourn_category])


def get_tourn_results():
    results.append( [x.text for x in browser.find_elements_by_css_selector('.day-table > tbody:nth-of-type(1) > tr > td:nth-child(3) > a')] )
    results.append( [x.text for x in browser.find_elements_by_css_selector('.day-table > tbody:nth-of-type(1) > tr > td:nth-child(7) > a')] )
    results.append( [x.text for x in browser.find_elements_by_css_selector('.day-table > tbody:nth-of-type(2) > tr > td:nth-child(7) > a')] )
    results.append( [x.text for x in browser.find_elements_by_css_selector('.day-table > tbody:nth-of-type(3) > tr > td:nth-child(7) > a')] )
    results.append( [x.text for x in browser.find_elements_by_css_selector('.day-table > tbody:nth-of-type(4) > tr > td:nth-child(7) > a')] )


def get_prediction(filename):
    with open(filename, 'r') as f:
        players = [line.strip() for line in f if line]
        predict.append([players[0]])
        predict.append([players[2]])
        predict.append(players[4:6])
        predict.append(players[7:11])
        predict.append(players[12:20])


def sparami_il_risultato():
    global rd_points
    score = 0
    # 0,1,2,3,4 = w,f,sf,qf,of
    for rd_i in range(len(rd_points)):
        print(rd_i)
        for name in predict[rd_i]:
            print(f'\t{name}')
            # se il giocatore ha raggiunto/superato il round pronosticato
            if any([name in player for t in results[:rd_i+1] for player in t]):
                score += rd_points[rd_i]
            # altrimenti, puo' comunque guadagnare i punti del turno a cui e' arrivato
            else:
                for ofst, t in enumerate(results[rd_i+1: len(rd_points)]):
                    if any([name in player for player in t]):
                        score += rd_points[rd_i + (ofst+1)]
                        break
    print(score)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: ./fantatennis.py <FILE_PRONOSTICO> <LINK_TORNEO>')
        exit()

    __, filename, page = sys.argv
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # che palle non va, quindi si apre chrome ma dai non voglio che mi spari una finestrona in faccia
    # options.add_argument('window-size=1920x1080')
    browser = webdriver.Chrome()#options=options)
    browser.get(page)

    get_tourn_round_points()
    get_tourn_results()
    get_prediction(filename)
    sparami_il_risultato()
