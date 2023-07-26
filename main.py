from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import csv
import datetime

matchDate = None


def scrape():
    matchupDate = input("Enter date (YYYY-MM-DD or blank for today's date):")
    print("Matchup date is: " + matchupDate)

    dateValues = matchupDate.split("-")

    try:
        newDate = datetime.datetime(int(dateValues[0]), int(dateValues[1]), int(dateValues[2]))
        correctDate = True
    except ValueError:
        print("Unrecognized date. Check format (YYYY-MM-DD) - " + matchupDate)
        correctDate = False
        sys.exit()

    # Add loop to loop through last 10 games
    # Previous_Date = datetime. datetime. today() – datetime. timedelta(days=1)
    count = 0
    attempedCount = 0
    dateToProcess = newDate
    while (count < 10 and attempedCount < 50):
        Previous_Date = dateToProcess - datetime.timedelta(days=1)
        dateToProcessFormatted = str(Previous_Date.year) + "-" + str(Previous_Date.month) + "-" + str(Previous_Date.day)

        # add working code below here and change url to use dateToProcessFormatted
        # change any reference to matchupdate in working code to dateToProcessFormatted
        # / html / body / div[4] / div[1] / div[1] / div / a[1]
        dateToProcess = Previous_Date
        print(dateToProcess)



        # if url found
        # add 1 to count
        # process date
        count += 1
        attempedCount += 1

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://www.covers.com/sports/mlb/matchups?selectedDate=" + matchupDate)

    navigationDate = driver.find_element(By.CLASS_NAME, 'cmg_active_navigation_item')

    pageDate = navigationDate.get_attribute("data-date")

    if pageDate != matchupDate:
        print("Matchup date not found.) - " + matchupDate)
        sys.exit()

    matchup_print = ""
    matchup_games = driver.find_elements(By.XPATH, '//div[contains(@class, "cmg_postgame")]')
    matchup_print = matchupDate + "\n" + "\t"

    with open('MLB_ScrapedData.txt', 'w') as f:
        for matchup_game in matchup_games:
            # Date              -   matchupDate
            # Home Team         -   homeTeam
            # Away Team         -   awayTeam
            # Home Score        -   homeScore
            # Away Score        -   awayScore
            # ATS
            # Winning Team      -
            # Losing Team       -
            # Results
            # OU
            # W / L
            # Results
            # ML
            # W / L
            # Results

            matchupLineScore = ""
            matchupLineScore = matchup_game.find_element(By.CLASS_NAME, 'cmg_matchup_line_score')

            table = ""
            table = matchupLineScore.find_elements(By.TAG_NAME, "tr")
            awayTeamRow = table[1].text.split()
            homeTeamRow = table[2].text.split()

            matchup_print = matchup_print + homeTeamRow[0] + " " + homeTeamRow[10] + " " + "ML:" + homeTeamRow[
                11] + " OU:" + homeTeamRow[12] + " (h)" + "\n" + "\t"
            matchup_print = matchup_print + awayTeamRow[0] + " " + awayTeamRow[10] + " " + "ML:" + awayTeamRow[
                11] + " OU:" + awayTeamRow[12] + "\n" + "\n" + "\t"

        f.write(matchup_print)

    input("Scrape complete. Press enter to exit.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape()
