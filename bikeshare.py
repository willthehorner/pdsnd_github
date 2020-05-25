import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    city = ''
    while city not in CITY_DATA:
        city = str(input('Which city would you like to analyze? Please enter Chicago, New York City, or Washington: ')).lower()

    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    i = input('Please enter the number of the month to analyze (1 for January, etc.) or enter 0 to analyze all months: ')
    while not i.isdecimal():
        print('Entry should be a number less than {}.'.format(len(months)))
        i = input('Please enter the number of the month to analyze (1 for January, etc.) or enter 0 to analyze all months: ')
    i = int(i)
    if i >= len(months) or i < 0:
        print('Not available - returning data for all months')
        i = 0

    month = months[i]

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    daynames = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    j = input('Please enter the number of the day of the week to analyze (1 for Monday, etc.) or enter 0 to analyze all days: ')
    while not j.isdecimal():
        print('Entry should be a number less than {}.'.format(len(daynames)))
        j = input('Please enter the number of the day of the week to analyze (1 for Monday, etc.) or enter 0 to analyze all days: ')
    j = int(j)
    if j >= len(daynames) or j < 0:
        print('Not available - returning data for all weekdays')
        j = 0

    day = daynames[j]

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['Month'] == month.title()]

    if day != 'all':
        df = df[df['Weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # Display the most common month, day of week, and start hour
    statcol = ['Month', 'Weekday', 'Start Hour']
    for col in statcol:
        if len(df[col].unique()) == 1:
            print('We are only searching data for the {} of {}.'.format(col.lower(), str(df[col].unique()[0])))
        else:
            print('The most common {} for rentals is {}.'.format(col.lower(), str(df[col].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station, end station, and combination of start station and end station
    df['Station Combo'] = df['Start Station'] + ' to ' + df['End Station']
    statcol = ['Start Station', 'End Station', 'Station Combo']
    for col in statcol:
        print('The most common {} is {}.'.format(col.lower(), str(df[col].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tottime = df['Trip Duration'].sum() / 60
    print('Total travel time was {} minutes'.format(int(tottime)))

    # display mean travel time
    avgtime = df['Trip Duration'].mean() / 60
    print('Average travel time was {} minutes'.format(int(avgtime)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types and gender
    user_types = df['User Type'].value_counts()
    for i in user_types.index:
        print('The count of {} users is {}.'.format(i.lower(),user_types[i]))

    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        for j in gender_count.index:
            print('The count of {} users is {}.'.format(j.lower(),gender_count[j]))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest, recent, common = int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])
        print('The oldest customer was born in {}, the youngest was born in {}, and the highest number were born in {}'.format(earliest, recent, common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        choice = input('\nWould you like to see some raw data? Enter yes or no. \n')
        if choice.lower() == 'yes':
            print(df[0:5])
            for r in range(5,df.shape[0],5):
                choice = input('\nWould you like to see more raw data? Enter yes or no. \n')
                if choice.lower() == 'yes':
                    print(df[r:r + 5])
                else:
                    break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
