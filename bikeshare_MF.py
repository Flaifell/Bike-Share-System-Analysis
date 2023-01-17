import time
import pandas as pd
import datetime

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
Months = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april',
          'apr', 'may', 'june', 'jun', 'all']
Days = ['friday', 'fri', 'saturday', 'sat', 'sunday', 'sun', 'monday', 'mon',
        'tuesday', 'tue', 'wednesday', 'wed', 'thursday', 'thu', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington) and handling typos
    while True:
        city = input('please chose a city from our available list, '
                     '(Chicago, New York City adn Washington): ').lower().strip()
        if city in CITY_DATA:
            break
        else:
            print('Oops! this might be a typo or your desired city is not available in our database yet. '
                  'please try again')

    # get user input for month (all, january, ... , june) also accepting abbreviations (jan,feb..etc)
    while True:     # handling typos and out of scoop
        month = input('please specify a month (Jan to June) to filter or type all for no filters: ').lower().strip()
        if month in Months:
            break
        else:
            print('Oops! this might be a typo or month is not available, please try again!..... (use Jan to Jun)')

    # get user input for day of week (all, monday, ... sunday) also accepting day name abbreviations (fri, sun, etc.)
    while True:     # handling typos
        day = input('please specify the day name to filter or type all for no filters: ').lower().strip()
        if day in Days:
            break
        else:
            print('oops! this might be a typo, please try again. ')

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
    # reading csv file by name
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting (Months, Days and Hours) into separate columns
    df['Month'] = df['Start Time'].dt.month
    df['Day Name'] = df['Start Time'].dt.day_name()
    df['Hours'] = df['Start Time'].dt.hour

    # applying filters if chosen
    if month != 'all':
        # getting the corresponding index of a chosen month
        month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = month[0:3]      # handling abbreviation cases in raw input (eg: 'jan' or 'feb')
        month = month_list.index(month) + 1

        # applying the month filter
        df = df[df['Month'] == month]

    if day != 'all':
        # getting full day name in cases of abbreviations in input. (eg: 'fri'...etc)
        day_list = {'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday', 'mon': 'monday',
                    'tue': 'tuesday', 'wed': 'wednesday', 'thu': 'thursday'}
        day = day[0:3]
        day = day_list.get(day).title()

        # applying the day filter
        df = df[df['Day Name'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nGetting Times of Travel statistics...\n')
    start_time = time.time()

    if month == 'all':  # print most common month if there was no filter, printing month name instead of month number
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
        common_month = df['Month'].mode()[0]
        total_count = df['Month'].value_counts()[common_month]
        print('The most busiest month was: {}, with a total of {} trips done'
              .format(month_dict.get(common_month), total_count))

    if day == 'all':        # display the most common day of week if there was no filter
        common_day = df['Day Name'].mode()[0]
        print('The most busiest day was: {}'.format(common_day))

    # display the most common start hour
    common_hours = df['Hours'].mode()[0]
    print('The most busiest hour was: {}:00'.format(common_hours))

    print("\nThis process took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nGetting Stations and Routes statistics...\n')
    start_time = time.time()

    # display most commonly used start station
    print('[ {} ] is the most Start Station used by users'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('[ {} ] is the most End Station used by users'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Combined Trip'] = df['Start Station'] + ' ---> ' + df['End Station']
    print('the most frequent combination of stations is: {}'.format(df['Combined Trip'].mode()[0]))

    print("\nThis process took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nGetting Trip Duration statistics...\n')
    start_time = time.time()

    # printing total travel time
    total = df['Trip Duration'].sum()

    sec = int(total)    # converting total seconds to days, hours, mins and seconds
    str_tm = str(datetime.timedelta(seconds=sec))
    day = str_tm.split(',')[0]
    hour, minute, second = str_tm.split(',')[1].split(':')
    print(f'The total travel time is: {day}{hour} hours {minute} mins and {second} seconds')

    # printing mean travel time
    mean = df['Trip Duration'].mean()
    print('the average trip duration take about: {} minutes'.format(int(mean/60)))

    print("\nThis process took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nGetting User Statistics...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts().to_string()
    print('Summary of user types: \n{}'.format(user_count))

    # Display counts of gender and excluding Washington
    if city != 'washington':
        gender_count = df['Gender'].value_counts().to_string()
        print('\nSummary of Gender types: \n{}'.format(gender_count))

    # Display earliest, most recent, and most common year of birth
        old = df['Birth Year'].min()
        year_old = 2023 - int(old)
        young = df['Birth Year'].max()
        year_young = 2023 - int(young)
        avr = df['Birth Year'].mode()[0]
        year_avr = 2023 - int(avr)
        print('\nAge Summary:\nOldest user is {} years old. (Birth year: {})\nYoungest user is {} years old. (Birth '
              'year: {}\nAverage user age is {} years old.'
              .format(year_old, int(old), year_young, int(young), year_avr))
    print("\nThis process took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        look = input('Finally, would you like to have a look at the database? [y/n]')
        x = 0
        n = 5
        while x+n < df.shape[0]:

            if look == 'n':
                break
            else:
                n = int(input('how many rows would you like to see'))
                print(df.iloc[x:x+n])
                x += n
                a = input('please press "y" if you want to load more rows or "n" to exit.').lower().strip()
                if a == 'y':
                    continue
                else:
                    break

        restart = input('\nThis is the end of our statistics, Would you like to restart again? [y/n].\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
