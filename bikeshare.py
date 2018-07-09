# Libraries
import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks the user to specify a city, a month, and a day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
                      or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
                    or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Which city are you interested in?', list(CITY_DATA.keys()))

    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    print('\n')
    city = input()
    print('\n')
    while city not in CITY_DATA.keys():
        print("Sorry! This is not a valid input.")
        print("Please enter any of the following cities:", list(CITY_DATA.keys()))
        print('\n')
        city = input()
        print('\n')

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    print('Which month are you interested in (january to june)?')
    print('Type "all" if you are interested in all the months!')
    print('\n')
    month = input()
    print('\n')
    while month not in months:
        print("Sorry! This is not a valid input.")
        # print("We do not have data for " + month + '.')
        print("Please enter any of the following: ", months)
        print('\n')
        month = input()
        print('\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    print('Which day are you interested in (monday, tuesday, ...)?')
    print('Type "all" if you are interested in all the days!')
    print('\n')
    day = input()
    print('\n')
    while day not in days:
        print("Sorry! This is not a valid input.")
        # print("We do not have data for " + day + '.')
        print("Please enter any of the following:", days)
        print('\n')
        day = input()
        print('\n')

    print('You have selected city: {}, month: {}, and day: {}'\
          .format(city.upper(), month.upper(), day.upper()))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
                      or "all" to apply no month filter
        (str) day - name of the day of week to filter by,
                    or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df.month==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = df['month'].mode()[0]
    most_common_month = months[most_common_month-1]
    print('The most common month of travel is ' + most_common_month.title() + '.')

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of travel is ' + most_common_day + '.')

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour (24hrs format) of travel is ' + str(most_common_hour) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is ' + most_common_start_station + '.')

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is ' + most_common_end_station + '.')

    # display most frequent combination of start station and end station trip
    comb = df.groupby(['Start Station','End Station']).size().reset_index(name='Combination')
    max_idx = comb['Combination'].idxmax()
    print('Most frequent start and end stations combination is:')
    print('\tStart station: {} and end station: {}.'.format(comb.iloc[max_idx][0],
           comb.iloc[max_idx][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time is: ' + str(total_travel) + '.')

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean travel time is: ' + str(mean_travel) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("\nUser types with counts are summarized below:")
    print(user_type_counts)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGenders with counts are summarized below:")
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nYears of birth:")
        print('Earliest: {}, most recent: {}, most common: {}'
              .format(int(earliest), int(most_recent), int(most_common)))

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
