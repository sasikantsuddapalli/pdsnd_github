#Python program to analyze data and provide descriptive statistics
import time
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pandas import *


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all','january', 'february', 'march', 'april', 'may', 'june']
dow= ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city= str(input('\nWhich of the following city data do you wish to see: Chicago,New York City,Washignton\n')).lower()
            if city not in CITY_DATA:
                print('Are you blind? Please select from the three cities')
                False
            else:
                break
        except:
            print('\nTry again!\n')
        finally:
            print('\nYou selected {}\n'.format(city))

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month= str(input('\nWhich month data do you wish to see? Input months (january,february,march,april,may,june or all)\n')).lower()
            if month not in months:
                print('Are you blind? Please provide selection from the first six months')
                False
            else:
                break
        except:
            print('\nTry again!\n')
        finally:
            print('\nYou selected {}\n'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day= str(input('\nWhich day do you wish to see? Input days (Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday or All)\n')).lower()
            if day not in dow:
                print('Are you blind? Please provide selection from actual days')
                False
            else:
                break
        except:
            print('\nTry again!\n')
        finally:
            print('\nYou selected {}\n'.format(day))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
        # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


        # extract month and day of week from Start Time to create new columns
    df['month'] =df['Start Time'].dt.month
    df['day_of_week'] =df['Start Time'].dt.weekday_name
        # filter by month if applicable
    if month != 'all':
            # use the index of the months list to get the corresponding int
        month = months.index(month)

            # filter by month to create the new dataframe
        df = df[df['month']==month]

            # filter by day of week if applicable
    if day != 'all':
                # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost common month is:\n {}'.format(popular_month))
    # display the most common day of week
    popular_dayofweek = df['day_of_week'].mode()[0]
    print('\nMost common day of week is:\n {}'.format(popular_dayofweek))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost common start hour is:\n {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_ss = df['Start Station'].mode()[0]
    print('\nMost common Start Station:\n {}'.format(popular_ss))

    # display most commonly used end station
    popular_es = df['End Station'].mode()[0]
    print('\nMost common End Station:\n {}'.format(popular_es))

    # display most frequent combination of start station and end station trip
    df['start-stop']=df['Start Station']+'-'+df['End Station']
    popular_sses = df['start-stop'].mode()
    print('\nMost common Start Station-End Station combinations:\n {}'.format(popular_sses))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    totalduration=df['Trip Duration'].sum(skipna=True)
    print('\nTotal travel time (minutes):\n',totalduration)

    # display mean travel time
    meantime=df['Trip Duration'].mean(skipna=True)
    print('\nMean Travel Time (minutes):\n',meantime)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print('\nUser Types:\n',df['User Type'].value_counts())

    # Display counts of gender
    if (city=='chicago' or city=='new york city'):
        print('\nUser Types:\n',df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if (city=='chicago' or city=='new york city'):
        print('\nEarliest birth year:\n',df['Birth Year'].min(skipna=True))
        print('\nRecent birth year:\n',df['Birth Year'].max(skipna=True))
        print('\nCommon Year of birth:\n',df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data"""
    while True:
        try:
            yn= str(input('\nDo you wish to see raw data: Y or N\n')).lower()
            if yn=='n':
                break
            elif yn=='y':
                while True:
                    try:
                        r=int(input('\nHow many rows of data do you wish to see.Choose between 1 and {}'.format(df.shape[0])))
                        if (r>=1 and r<=df.shape[0]) is False:
                            print('Try a number between the acceptable range')
                            False
                        else:
                            print(df.head(r))
                            break
                    except:
                        print('\nTry again!\n')
        except:
            print('\nTry again!\n')

def plot_data(df,city):
    """"Plot data trends"""
    plt.figure();
    if (city=='chicago' or city=='new york city'):
        print('\nYour plot named "SamplePlot1.png" is saved in the same folder as your script')
        table = pivot_table(df, values='Trip Duration', index=['Birth Year'],columns=['Gender'], aggfunc=np.sum)
        plt.rcParams["figure.figsize"] = [16,9]
        a=table.plot.bar()
        a.set_ylabel("Trip Duration")
        plt.savefig('SamplePlot1.png')
    else:
        print('\nYour plot named "SamplePlot2.png" is saved in the same folder as your script')
        table = pivot_table(df, values='Trip Duration', index=['User Type'], aggfunc=np.sum)
        plt.rcParams["figure.figsize"] = [16,9]
        table.plot.pie(subplots=True)
        plt.savefig('SamplePlot2.png')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        #plot_data(df,city)
        #raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
