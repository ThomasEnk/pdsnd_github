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

    # get user input for city (chicago, new york city, washington).
    cities = ['chicago', 'new york city', 'washington']
    print('\nWould you like to see data form Chicago, New York or Washington? ' )

    city = ' '
    while city not in cities:
        city = input().lower()
        #if city == 'new york' then add ' city'
        if city == 'new york':
            city += ' city'

    # get user input for month (all, january, february, ... , june)
    #Ask if you want to filter the data by month
    filter_month = ' '
    print('\nWould you like to filter the data by month (yes/no)? ')
    while filter_month != 'yes' and filter_month != 'no':
        filter_month = input().lower()

    if filter_month == 'yes':
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        #Ask which month to choose
        month = ' '
        print('Which month? January, February, March, April, May or June? ')
        while month not in months:
            month = input().lower()
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    #Ask if you want to filter the data by day
    filter_day = ' '
    print('\nWould you like to filter the data by day (yes/no)? ')
    while filter_day != 'yes' and filter_day != 'no':
        filter_day = input().lower()

    if filter_day == 'yes':
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        #Ask which day to choose
        day = ' '
        print('Which day? Monday, Tuesday, Wednesday, etc. ? ')
        while day not in days:
            day = input().title()
    else:
        day = 'all'

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # make a column of the trip between start station and end stations
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    # display the most common month
    print('The most common month is:', months[df['month'].mode()[0]-1])

    # display the most common day of week
    print('The most common day of week is:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('The most common start hour is:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most common end station is:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is:', df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is: ', df['Trip Duration'].sum())

    # display mean travel time
    print('The average travel time is: ', round(df['Trip Duration'].mean(),2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types are: ', df['User Type'].value_counts())

    #check because data not for all cities available
    if 'Gender' in df:
        # Display counts of gender
        print('The counts of gender are: ', df['Gender'].value_counts())

    #check because data not for all cities available
    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        print('The earliest year of birth is: ', int(df['Birth Year'].min()))
        print('The most recent year of birth is: ', int(df['Birth Year'].max()))
        print('The most common year of birth is: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw datas."""

    #Ask if you want raw data to be displayed
    show_data = ' '
    print('\nWould you like to see raw data (yes/no)?\n')
    while show_data != 'yes' and show_data != 'no':
        show_data = input().lower()

    if (show_data == 'yes'):
        #get the index of the filtered dataframe
        row_index = df.index
        for row in range(len(df)):
            print('\n', df.loc[row_index[row]])
            #after every 5th row, ask if more raw data's are required
            if (row+1) % 5 == 0:
                more_data = ' '
                print('\nWould you like to see more raw data? Enter any key to continue, no to exit.\n')
                more_data = input().lower()

                #break if no more raw data needed
                if more_data == 'no':
                    break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
