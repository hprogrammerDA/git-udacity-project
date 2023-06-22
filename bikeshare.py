import time
import os
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 24)
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyse.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('To end this program, type ctrl+C on Windows or ctrl+Z on Unix shell systems followed by any input.')
    done = False
    while not done:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington? ").lower()
        for i in CITY_DATA:
            if city == i:
                done = True
                break
        else:
            print("Invalid input, try again please. Please confirm spelling is matching the requested input exactly.")

    while True:
        filterinput = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter. ").lower()
        if filterinput == 'month' or filterinput == 'day' or filterinput == 'both' or filterinput == 'none':
            break
        else:
            print("Only valid inputs are 'month', 'day', 'both' or 'none'")
    month = 'all'
    if filterinput == 'month' or filterinput == 'both':
        done = False
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while not done:
            month = input("Which month? January, February, March, April, May, or June? ").lower()
            for i in months:
                if month == i:
                    done = True
                    break
            else:
                print("Invalid input, try again please. Please confirm spelling is matching the requested input exactly")

    day = 'all'
    if filterinput == 'day' or filterinput == 'both':
        done = False
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while not done:
            day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
            for i in days:
                if day == i:
                    done = True
                    break
            else:
                print("Invalid input, try again please. Please confirm spelling is matching the requested input exactly")

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
    # Load file into environment with transformations #
    absolute_path = os.path.dirname(__file__)
    relative_path = "data_files"
    full_path = os.path.join(absolute_path,relative_path)
    df = pd.read_csv("{}/{}".format(full_path, CITY_DATA[city]))
        
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] =df['Start Time'].dt.hour
    df['monthname'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all': # month filter
        df = df.where(df["monthname"] == month.title())
        df = df[df['monthname'].notnull()]

    if day != 'all': # day filter
        df = df.where(df["day_of_week"] == day.title())
        df = df[df['day_of_week'].notnull()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df.monthname.mode()[0]
    print("Most popular month: {}".format(popular_month))
    popular_day = df.day_of_week.mode()[0]
    popular_hour = int(df.hour.mode()[0])
    print("Most popular hour: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most common stations and trip combinations."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: {}".format(common_start_station))

    common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station: {}".format(common_end_station))

    common_trip_combination = df[['Start Station', 'End Station']].value_counts().head(n=1).to_string()
    print("Most common combination of start station and end station trip consists of:\n{}".format(common_trip_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()
    print("The total trip duration is: {} seconds".format(total_travel))

    mean_travel = df['Trip Duration'].mean()
    print("The mean trip duration is: {} seconds".format(round(mean_travel,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts().to_string()
    print("User type statistics (count):\n{}".format(user_types))

    try:
        gender_statistics = df['Gender'].value_counts().to_string()
        print("\nGender statistics (count):\n{}".format(gender_statistics))
    except:
        print("No Gender statistics unfortunately")

    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nBirth Statistics: \nEarliest birth year is: {}. \nMost recent birth year is: {}\nmost common year of birth is: {}".format(earliest, most_recent, most_common))
    except:
        print("No Birth Year Statistics unfortunately")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rawdata(df):
    """Asks user whether they want to display 5 rows of data or not """
    while True:
        rawdata = input("Would you like to see 5 rows of raw data?(for yes write 'yes', for no write 'no') ").lower()
        if rawdata == 'yes':
            print(df.sample(n=5))
        elif rawdata.lower() == 'no':
            break
        else:
            print("Invalid input, try again please. Only valid inputs are yes or no!")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata(df)
        
        done = False
        while not done:
            restart = input('\nWould you like to restart? Enter yes or no. \n') 
            if restart.lower() == 'yes':
                print("restarting...")
                break
            elif restart.lower() == 'no': 
                done = True
                break
            else:
                print("Invalid input, try again please. Only valid inputs are yes or no!")
        if done == True: 
            break

if __name__ == "__main__":
	main()