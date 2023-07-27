from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import csv
import datetime

def process():
    # Get date to process
    matchupDate = input("Enter date (YYYY-MM-DD or blank for today's date):")
    print("Matchup date is: " + matchupDate)

    dateValues = matchupDate.split("-")

    # Verify that the date entered is a valid date
    try:
        rawDate = datetime.datetime(int(dateValues[0]), int(dateValues[1]), int(dateValues[2]))
    except ValueError:
        print("Unrecognized date. Check format (YYYY-MM-DD) - " + matchupDate)
        sys.exit()

    process_mlb(matchupDate, rawDate)


def process_mlb(matchupDate, rawDate):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    count = 0
    rawProcessDate = rawDate

    while (count < 10):
        # ToDo: Validate rawProcessDate
        # ToDo: If date is valid, create formatted date, else error and exit
        formattedDate = str(rawProcessDate.year) + "-" + str(rawProcessDate.month) + "-" + str(
            rawProcessDate.day)

        # Get the next date to process
        rawProcessDate = rawProcessDate - datetime.timedelta(days=1)

        print(formattedDate)
        count += 1


    # ToDo: The code below will need to be inside the loop above


    driver.get("https://www.covers.com/sports/mlb/matchups?selectedDate=" + matchupDate)

    navigationDate = driver.find_element(By.CLASS_NAME, 'cmg_active_navigation_item')

    pageDate = navigationDate.get_attribute("data-date")

    if pageDate != matchupDate:
        print("Matchup date not found: " + matchupDate)
        sys.exit()

    matchup_print = ""
    matchup_games = driver.find_elements(By.XPATH, '//div[contains(@class, "cmg_postgame")]')
    matchup_print = matchupDate + "\n" + "\t"

    with open('MLB_ScrapedData.txt', 'w') as f:
        for matchup_game in matchup_games:
            # X Date                    - matchupDate
            # X Team                    - homeTeamRow[0]
            # X Opponent                - awayTeamRow[0]
            # X Rank
            # X Home Team Score
            # X Away Team Score
            # Home Team Runs            - homeTeamRow[10]
            # Away Team Runs            - awayTeamRow[10]
            # Home Team Hits            - homeTeamRow[13]
            # Away Team Hits            - awayTeamRow[13]
            # Home Team Errors
            # Away Team Errors
            # Winner                    - gameWinner

            matchupLineScore = ""
            matchupLineScore = matchup_game.find_element(By.CLASS_NAME, 'cmg_matchup_line_score')

            table = ""
            table = matchupLineScore.find_elements(By.TAG_NAME, "tr")
            awayTeamRow = table[1].text.split()
            homeTeamRow = table[2].text.split()

            # Determine winner and loser
            if homeTeamRow[10] > awayTeamRow[10]:
                gameWinner = homeTeamRow[0]
                #homeTeamRow[0] = homeTeamRow[0] + "(w)"
            else:
                gameWinner = awayTeamRow[0]
                #awayTeamRow[0] = awayTeamRow[0] + "(w)"

            if homeTeamRow.__len__() == 15:
                homeOU = homeTeamRow[12]
                homeHits = homeTeamRow[13]
                homeErrors = homeTeamRow[14]
            else:
                homeOU = ""
                homeHits = homeTeamRow[12]
                homeErrors = homeTeamRow[13]

            if awayTeamRow.__len__() == 15:
                awayOU = awayTeamRow[12]
                awayHits = awayTeamRow[13]
                awayErrors = awayTeamRow[14]
            else:
                awayOU = ""
                awayHits = awayTeamRow[12]
                awayErrors = awayTeamRow[13]

            matchup_print = matchup_print + homeTeamRow[0] + " Score:" + homeTeamRow[10] + " Runs:" + homeTeamRow[10] + " ML:" + homeTeamRow[
                11] + " OU:" + homeOU + " Hits:" + homeHits + " Errors:" + homeErrors + " (h)" + "\n" + "\t"
            matchup_print = matchup_print + awayTeamRow[0] + " Score:" + awayTeamRow[10] + " Runs:" + awayTeamRow[10] + " ML:" + awayTeamRow[
                11] + " OU:" + awayOU + " Hits:" + awayHits + " Errors:" + awayErrors + "\n" + "\n" + "\t"

        f.write(matchup_print)

    input("Scrape complete. Press enter to exit.")


# ToDo: Move date validation to a new function and return true or false


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process()
