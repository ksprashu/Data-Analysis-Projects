import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv',
              'new york city': 'new_york_city.csv' } # added NYC just in case someone inputs this - it's not really incorrect!

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*45)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('\nFor which city would you like to see the data?')
        city = input('Please enter any one of -> Chicago, New York, or Washington (default = Chicago): ').lower() or 'chicago'
        if city in CITY_DATA.keys():
            break
        else:
            print('You seem to have entered an invalid input; please try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('\nWould you like to filter the data by month? Or enter \'all\' to see everything')
        month = input("Please enter any one of -> January, February... June, or 'All' (default = All): ").lower() or 'all'
        if month == 'all':
            break
        elif month in months:
            month = month.title()
            break
        else:
            print('You seem to have entered an invalid input; please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        print('\nWould you like to filter the data by a day of the week? Or enter \'all\' to see everything')
        day = input("Please enter any one of -> Monday, Tuesday... Saturday, Sunday, or 'All' (default = All): ").lower() or 'all'
        if day == 'all':
            break
        elif day in days:
            day = day.title()
            break
        else:
            print('You seem to have entered an invalid input; please try again.')


    print('-'*40)

    # reset all global filters before returning
    global filters, filter_day, filter_month
    filters = []
    filter_day = ''
    filter_month = ''

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
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter dataframe by selected month or don't do anything if 'all'
    global filters, filter_day, filter_month    
    if month != 'all':
        filters.append('month')
        filter_month = month
        df = df[df['month'] == month]

    # filter dataframe by selected day or don't do anything if 'all'
    if day != 'all':
        filters.append('day')
        filter_day = day
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if not 'month' in filters:
        month = df.groupby('month').size().sort_values(ascending=False)
        print('The most popular month was {} with {} trips.'.format(month.index[0], month.iloc[0]))
    else:
        print('Filtered by month - {}'.format(filter_month))

    # display the most common day of week
    if not 'day' in filters:
        day = df.groupby('day_of_week').size().sort_values(ascending=False)
        print('The most popular day was {} with {} trips.'.format(day.index[0], day.iloc[0]))
    else:
        print('Filtered by day - {}'.format(filter_day))

    # display the most common start hour
    hour = df.groupby('hour').size().sort_values(ascending=False)
    print('The most popular hour was {} with {} trips.'.format(hour.index[0], hour.iloc[0]))

    # display amount of NaN data
    report_null_data(df['Start Time'], 'There were {} records with invalid datetime data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df.groupby('Start Station').size().sort_values(ascending=False)
    print("The most popular starting station was {} with {} trips.".format(start.index[0], start.iloc[0]))

    # display amount of NaN data
    report_null_data(df['Start Station'], 'There were {} records with invalid starting station data.')

    # display most commonly used end station
    end = df.groupby('End Station').size().sort_values(ascending=False)
    print('The most popular ending station was {} with {} trips.'.format(end.index[0], end.iloc[0]))

    # display amount of NaN data
    report_null_data(df['End Station'], 'There were {} records with invalid ending station data.')

    # display most frequent combination of start station and end station trip
    grouped = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print('The most frequent combination of start station and end station was {} which saw {} trips.'.format(grouped.index[0], grouped.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration = df['Trip Duration'].sum()
    h, m = divmod(duration, 3600)
    d, h = divmod(h, 24)
    print('The total trip duration was {} seconds, or about {} days, {} hours.'.format(duration, int(d), int(h)))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    m, s = divmod(mean, 60)
    print('The average travel time was {} seconds, or about {} minutes, and {} seconds.'.format(mean, int(m), int(s)))

    # display amount of NaN data
    report_null_data(df['Trip Duration'], 'There were {} records with invalid trip duration data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df.groupby('User Type').size().sort_values(ascending=False)
    for i in range(len(user_counts)):
        print('The number of {}(s) = {}.'.format(user_counts.index[i], user_counts.iloc[i]))

    # display amount of NaN data
    report_null_data(df['User Type'], 'There were {} records with invalid user type data.')
    print('')

    # Display counts of gender
    # check if the selected dataset has the column gender, and if not show appropriate message
    if 'Gender' in df.columns:
        gender_counts = df.groupby('Gender').size().sort_values(ascending=False)
        for i in range(len(gender_counts)):
            print('The number of {}(s) = {}.'.format(gender_counts.index[i], gender_counts.iloc[i]))

        # display amount of NaN data
        report_null_data(df['Gender'], 'There were {} records with invalid gender data.')
    else:
        print('There was no gender data available for your selection.')

    print('')

    # Display earliest, most recent, and most common year of birth
    # check if the selected dataset has the column Birth Data, and if not show appropriate message
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        common = df.groupby('Birth Year').size().sort_values(ascending=False)

        print('The oldest rider was born in the year {}.'.format(int(earliest)))
        print('The youngest rider was born in the year {}.'.format(int(latest)))
        print('The most common year of birth among the riders was {} with {} trips.'.format(int(common.index[0]), common.iloc[0]))

        # display amount of NaN data
        report_null_data(df['Birth Year'], 'There were {} records with invalid birth year data.')
    else:
        print('There was no birth year data available for your selection.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Displays statistics on bikeshare users."""
    next = input('\nDo you want to see the raw data? (Y/Yes to continue, any other key for no) : ').lower()
    if not (next == 'y' or next == 'yes'):
        return

    print('\nShowing the raw data...\n')
    start = 0

    while start < df.size:
        end = start + 5
        if end > df.size:
            end = df.size
            
        print('Showing records from index {} to {}.\n'.format(start, end))
        print(df[start:end])

        start = end
        next = input('\nDo you want to see the next 5 records? (Y/Yes to continue, any other key to break) : ').lower()
        if not (next == 'y' or next == 'yes'):
            break


# in cases where there are NaN data, then let's report this to the user
def report_null_data(data, msg):
    null_count = data.isnull().sum()
    if null_count > 0:
        msg = 'NOTE: ' + msg
        print(msg.format(null_count))


# global list to keep track of the filters
filters = []
filter_month = ''
filter_day = ''


def main():
    # run the process in a loop until the user decides to quit
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
