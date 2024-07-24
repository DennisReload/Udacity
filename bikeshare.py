import time
import pandas as pd
import numpy as np
import datetime

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
    city = month = day = ''

    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days   = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        city = input('\nEnter a city to analyze (Chicago, New York City, Washington): ').lower().strip()
        if city in cities:
            break
        else:
            print('This is an invalid input, try again!')

    while True:
        month = input('\nEnter a month to filter by (January, February, March, April, May, June, All): ').lower().strip()
        if month in months:
            break
        else:
            print('This is an invalid input, try again!')

    while True:
        day = input('\nEnter a day of the week to filter by: (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All): ').lower().strip()
        if day in days:
            break
        else:
            print('This is an invalid input, try again!')

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
    
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_common_month = months[df['month'].mode()[0] - 1]
    print('\nMost common month is {}'.format(most_common_month))
    
    most_common_day = df['day'].mode()[0]
    print('\nMost common day of the week is {}'.format(most_common_day))

    df['start hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['start hour'].mode()[0]
    print('\nMost common start hour is {}'.format(most_common_start_hour))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print('\nMost common start station was {}'.format(most_common_start_station))

    most_common_end_station = df['End Station'].mode()[0]
    print('\nMost common end station was {}'.format(most_common_end_station))

    most_common_start_end_station = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print('\nMost common start-end station was {}'.format(most_common_start_end_station))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time_sec = int(df['Trip Duration'].sum())
    total_travel_time = datetime.timedelta(seconds = total_travel_time_sec)
    print('The total travel time was {}'.format(total_travel_time))
    
    mean_travel_time_sec = int(df['Trip Duration'].mean())
    mean_travel_time = datetime.timedelta(seconds = mean_travel_time_sec)
    print('The mean travel time was {}'.format(mean_travel_time))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    print('\nUser Types:')
    user_types_counts = dict(df['User Type'].value_counts())
    for user_type, count in user_types_counts.items():
        print('{} count is {}'.format(user_type, count))

    if city == 'washington':
        return
        
    print('\nGenders:')
    genders_counts = dict(df['Gender'].value_counts())
    for gender, count in genders_counts.items():
        print('{} count is {}'.format(gender, count))
    
    print('\nBirth Year Stats:')
    earliest_year = df['Birth Year'].min()
    recent_year = df['Birth Year'].max()
    most_common_year = df['Birth Year'].mode()[0]
    print('Earliest year of birth is {}'.format(earliest_year))
    print('Most recent year of birth is {}'.format(recent_year))
    print('Most common year of birth is {}'.format(most_common_year))
    
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data on bikeshare users."""

    num = 0
    while True:
        check = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip()
        if check.lower() != 'yes':
            break
        try:
            print(df[num:num+5].to_dict())
        except IndexError:
            break
        num+=5
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)
                
        restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()  
    