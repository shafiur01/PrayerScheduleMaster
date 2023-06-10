# This is a python program that fetches all the prayer timings from api.aladhan based on the location provided
# and gives us the connected scatterplot graph of different prayer times which will help the muslim community with
# a great advantage to find free time to schedule different meetings without conflictics of time
# Besides another functionality of the program is it takes care of the daylight savings.

import csv
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from date_handler import *

# I don't remember what this is for but it breaks if I delete it
timings = []


def formatted_print(item):
    for obj in item:
        date = datetime.fromtimestamp(
            int(obj["date"]["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        temp = [date, get_time(obj, "Fajr"), get_time(obj, "Dhuhr"), get_time(
            obj, "Asr"), get_time(obj, "Maghrib"), get_time(obj, "Isha")]
        timings.append(temp)
        print(temp)


def get_time(item, prayer):
    return item["timings"][prayer].split(" ")[0]


def get_prayer_data(year, month, address):
    response = requests.get(
        f"http://api.aladhan.com/v1/calendarByAddress/{year}/{month}?address={address}")
    if response.status_code == 200:
        print(f"successfully fetched the data for {year}/{month}")
        formatted_print(response.json()["data"])
    else:
        print(
            f"Hello person, there's a {response.status_code} error with your request")
        

def generate_prayer_times_graph(start_month, start_year, end_month, end_year, address):

    month_year_list = get_month_year_range(start_month, start_year, end_month, end_year)

    for month, year in month_year_list:
        get_prayer_data(year, month, address)

    # Writing data to a csv file
    with open("prayer_timings.csv", mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])
        writer.writerows(timings)

    with open('prayer_timings.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        # Append the new column names to the header
        header.extend(['FajrMinutes', 'DhuhrMinutes', 'AsrMinutes',
                       'MaghribMinutes', 'IshaMinutes'])

        # Opening a new csv file to write the converted minutes in seperate row
        with open('prayerMinutes.csv', 'w', newline='') as new_csvfile:
            csvwriter = csv.writer(new_csvfile)
            csvwriter.writerow(header)

            # Looping over each row in the original csv file that we made after fetching the Json data
            for row in csvreader:
                # Converting the times to minutes
                fajr_minutes = (datetime.strptime(
                    row[1], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
                duhr_minutes = (datetime.strptime(
                    row[2], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
                asr_minutes = (datetime.strptime(
                    row[3], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
                maghrib_minutes = (datetime.strptime(
                    row[4], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
                isha_minutes = (datetime.strptime(
                    row[5], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0

                # Appending the new columns to the row
                row.extend([fajr_minutes, duhr_minutes, asr_minutes,
                            maghrib_minutes, isha_minutes])

                # Writing the row to the new csv file
                csvwriter.writerow(row)

    # reading the csv file and parse the date and times into a pandas dataframe
    df = pd.read_csv('prayerMinutes.csv', parse_dates=['Date'],
                     date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S', errors='coerce'))

    # converting minutes to timedata and add to date using pandas dataframe
    df['Fajr'] = pd.to_datetime(df['Date'].dt.date) + \
        pd.to_timedelta(df['FajrMinutes'], unit='m')
    df['Dhuhr'] = pd.to_datetime(df['Date'].dt.date) + \
        pd.to_timedelta(df['DhuhrMinutes'], unit='m')
    df['Asr'] = pd.to_datetime(df['Date'].dt.date) + \
        pd.to_timedelta(df['AsrMinutes'], unit='m')
    df['Maghrib'] = pd.to_datetime(
        df['Date'].dt.date) + pd.to_timedelta(df['MaghribMinutes'], unit='m')
    df['Isha'] = pd.to_datetime(df['Date'].dt.date) + \
        pd.to_timedelta(df['IshaMinutes'], unit='m')

    # plotting the data using matplotlib and showing it
    yticklocs = [60 * i for i in range(25)]
    yticklabels = ["12:00 AM"]
    yticklabels.extend(["{}:00 AM".format(t) for t in range(1, 12)])
    yticklabels.append("12:00 PM")
    yticklabels.extend(["{}:00 PM".format(t) for t in range(1, 12)])
    yticklabels.append("12:00 AM")


    plt.yticks(yticklocs, yticklabels)
    plt.plot(df['Date'], df['FajrMinutes'], label='Fajr')
    plt.plot(df['Date'], df['DhuhrMinutes'], label='Dhuhr')
    plt.plot(df['Date'], df['AsrMinutes'], label='Asr')
    plt.plot(df['Date'], df['MaghribMinutes'], label='Maghrib')
    plt.plot(df['Date'], df['IshaMinutes'], label='Isha')
    plt.legend()
    plt.grid()
    plt.show()


start_month = 8
start_year = 2023
end_month = 12
end_year = 2023
address = "Dhaka"

generate_prayer_times_graph(start_month, start_year,
                            end_month, end_year, address)