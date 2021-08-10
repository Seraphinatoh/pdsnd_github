#import time for checking code runtime
#import pandas to store data

import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter Chicago, Washington or New York City for your analysis: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please input first 6 months or all for filtering: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please input day of the week or all: ').lower()

#    print('-'*40)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # only run this calculation if there are no filter for month
    if month == 'all':
        #try to check for error for month
        try:
            # display the most common month
            popular_month = df['month'].mode()[0]
            print('Most Popular Month:', popular_month)
        
        except Exception as e:
            print('Error:{}, Skip calculation, please check data'.format(e))    

    # only run this calculation if there are no filter for day
    if day == 'all':
        #try to check for error for day of week
        try:
            # display the most common day of week
            popular_day = df['day_of_week'].mode()[0]
            print('Most Popular Day of Week:', popular_day)
        
        except Exception as e:
            print('Error:{}, Skip calculation, please check data'.format(e))
    
    #try to check for error with start time
    try:
        # display the most common start hour
        # extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour
        # find the most popular hour
        popular_hour = df['hour'].mode()[0]
        print('Most Popular Start Hour:', popular_hour)
    
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))    
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    #try to check error for start station
    try:
        # display most commonly used start station
        popular_start = df['Start Station'].mode()[0]
        
        print('Most Popular Start Station:', popular_start)
    
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))
    
    #Try to check error for end station
    try:
        # display most commonly used end station
        popular_end = df['End Station'].mode()[0]        
        print('Most Popular End Station:', popular_end)

        # display most frequent combination of start station and end station trip
        df['Combi Station']  = df['Start Station'] + ' to ' + df['End Station']
        popular_combi = df['Combi Station'].mode()[0]      
        print('Most Popular Start to End Station:', popular_combi)
    
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    
    start_time = time.time()
    
    #try to check error for trip duration
    try:
        # display total travel time
        total_time = df['Trip Duration'].sum()
        print(total_time)
        #split into hours minutes seconds
        hrs=(total_time//3600)
        mins=(total_time%3600)//60
        sec=(total_time%3600)%60
        print('Total travel time: {} hours {} mins {} seconds'.format(int(hrs), int(mins), round(sec)))
        
        # display mean travel time
        mean_time = df['Trip Duration'].mean()
        #split into minutes seconds
        mins=(mean_time//60)
        sec = mean_time%60
        print('Average travel time: {} mins {} seconds'.format(int(mins), round(sec)))
     
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #try to check for error for user types
    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print(user_types)
    
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))
        
    
    #try to check for error for gender
    try:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)
        
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))
        
    #try to check for error for birth year
    try:
        # Display earliest, most recent, and most common year of birth
        df_filter = df[df['Birth Year'].notnull()]
        df_birthyear = df_filter['Birth Year'].astype(int)
        by_earliest = df_birthyear.min()
        by_mostrecent = df_birthyear.max()
        by_mostcommon = df_birthyear.mode()[0]

        print('Birth Year - Earliest: {}, Most Recent: {}, Most Common: {}'.format(by_earliest,by_mostrecent,by_mostcommon))
        
    except Exception as e:
        print('Error:{}, Skip calculation, please check data'.format(e))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df,index):
    #allow all column to be displayed. Print first 5 rows of the df
    pd.set_option('display.max_columns',200)
    print(df[index:index+5])



def main():
    while True: 
        max_retries = 3
        for n in range(max_retries):
            try:
                city, month, day = get_filters()
                df = load_data(city, month, day)
                time_stats(df, month, day)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                break
            except Exception as e:
                if n < max_retries-1:
                    print('Exception occurred:{}, please retype inputs'.format(e))
                    print('Tries remaining:{}'.format(max_retries-n-1))
                else:
                    print('Exception occurred:{}, Max retries. Code will exit'.format(e))
                    break
        index = 0
        while True:
            display = input('\nWould you like to display more raw data (5 rows each time only)? Enter yes or no.\n').lower()
            if display == 'yes':   
                display_raw_data(df,index) 
                index = index + 5
            elif display == 'no':
                break
            else:
                print('Invalid input, try again')            
                
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'no' or restart == 'yes':
                break
            else:
                print('Invalid input, try again')               
        if restart == 'no':
           break

if __name__ == "__main__":
	main()
