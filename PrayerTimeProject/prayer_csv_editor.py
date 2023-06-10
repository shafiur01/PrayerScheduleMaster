import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Open the csv file
with open('prayertimes.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)

    # Append the new column names to the header
    header.extend(['FajrMinutes', 'DhuhrMinutes', 'AsrMinutes', 'MaghribMinutes', 'IshaMinutes'])

    # Open a new csv file to write the results
    with open('prayerMinutes.csv', 'w', newline='') as new_csvfile:
        csvwriter = csv.writer(new_csvfile)
        csvwriter.writerow(header)

        # Loop over each row in the original csv file
        for row in csvreader:
            # Convert the times to minutes
            fajr_minutes = (datetime.strptime(row[1], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            duhr_minutes = (datetime.strptime(row[2], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            asr_minutes = (datetime.strptime(row[3], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            maghrib_minutes = (datetime.strptime(row[4], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            isha_minutes = (datetime.strptime(row[5], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0

            # Append the new columns to the row
            row.extend([fajr_minutes, duhr_minutes, asr_minutes, maghrib_minutes, isha_minutes])

            # Write the row to the new csv file
            csvwriter.writerow(row)

# read the csv file and parse the date and times
df = pd.read_csv('prayerMinutes.csv', parse_dates=['Date'],
                 date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S', errors='coerce'))

# add one hour for daylight saving
df[['FajrMinutes', 'DhuhrMinutes', 'AsrMinutes', 'MaghribMinutes', 'IshaMinutes']] += 60

# convert minutes to timedelta and add to date
df['Fajr'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['FajrMinutes'], unit='m')
df['Dhuhr'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['DhuhrMinutes'], unit='m')
df['Asr'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['AsrMinutes'], unit='m')
df['Maghrib'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['MaghribMinutes'], unit='m')
df['Isha'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['IshaMinutes'], unit='m')

# plot the data
plt.plot(df['Date'], df['FajrMinutes'], label='Fajr')
plt.plot(df['Date'], df['DhuhrMinutes'], label='Dhuhr')
plt.plot(df['Date'], df['AsrMinutes'], label='Asr')
plt.plot(df['Date'], df['MaghribMinutes'], label='Maghrib')
plt.plot(df['Date'], df['IshaMinutes'], label='Isha')
plt.legend()
plt.show()
