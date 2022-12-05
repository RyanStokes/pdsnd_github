import time
import pandas as pd

RAW_DATA_SIZE = 5

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Valid months is a dictionary of months (1-6) in different formats
VALID_MONTHS = {'all':0,
                'january':1,'jan':1,'1':1,
                'february':2,'feb':2,'2':2,
                'march':3,'mar':3,'3':3,
                'april':4,'apr':4,'4':4,
                'may':5,'may':5,'5':5,
                'june':6,'jun':6,'6':6}

#Valid days is a dictionary of all days in different formats
VALID_DAYS = {'all':-1,
              'monday':0,'mon':0,'0':0,
              'tuesday':1,'tue':1,'1':1,
              'wednesday':2,'wed':2,'2':2,
              'thursday':3,'thu':3,'3':3,
              'friday':4,'fri':4,'4':4,
              'saturday':5,'sat':5,'5':5,
              'sunday':6,'sun':6,'6':6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - int of the month to filter by, or "0" to apply no month filter
        (int) day - int of the day of week to filter by, or "-1" to apply no day filter
    """
    print('Welcome! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while(city.lower() not in CITY_DATA):
        city = input("\nWhich city would you like to analyze? chicago, new york city, washington: ")

        if (city.lower() not in CITY_DATA):
            print("I don't understand, please try again. Enter the full name of the city.")
        else:
            print("Great, we are using the data for {}.".format(city.lower()))

    # Get user input for month (all, january, february, ... , june)
    month = ""
    while(month.lower() not in VALID_MONTHS):
        month = input("\nWhich month would you like to filter by? all, january, february, march, april, may, or june: ")
        if (month.lower()  not in VALID_MONTHS):
            print("I don't understand, please try again. Enter the full name, short name, or the month number.")
        else:
            print("Great, we are filtering by {}.".format(month.lower()))
            
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while(day.lower() not in VALID_DAYS):
        day = input("\nWhich day would you like to filter by? all, monday, tuesday, etc.: ")
        if (day.lower()  not in VALID_DAYS):
            print("I don't understand, please try again. Enter the full name or the short name.")
        else:
            print("Great, we are filtering by {}.".format(day.lower()))

    print('-'*40)
    
    return city.lower(), VALID_MONTHS[month], VALID_DAYS[day]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - int of the month to filter by, or "0" to apply no month filter
        (int) day - int of the day of week to filter by, or "-1" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Load in the data from appropriate city
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the start time column to a date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create a new column for month, day and hour of the start time
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    
    # Check if month/day filter was set to "all" coded as 0, -1 respectively
    if (month > 0):
        df = df[df['month'] == month]
    if (day >= 0):
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    months = df['month'].value_counts()
    
    # The below takes advantage of the dictionary keys being ordered (as of Python 3.7) to get the name of the month
    print("The most common month is {} with {} records".format(list(VALID_MONTHS)[list(VALID_MONTHS).index(str(months.idxmax()))-2],months.max()))
        
    # Display the most common day of week
    days = df.groupby(['day'])['day'].count()
    print("The most common day is {} with {} records".format(list(VALID_DAYS)[list(VALID_DAYS).index(str(days.idxmax()))-2],days.max()))

    # Display the most common start hour
    hours = df.groupby(['hour'])['hour'].count()
    print("The most common starting hour is {}:00 with {} records".format(hours.idxmax(),hours.max()))

    print("\nThis took %s milliseconds." % round((time.time() - start_time)*1000,2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    stations = df.groupby(['Start Station'])['Start Station'].count()
    print("The most common start station is: {} with {} records".format(stations.idxmax(),stations.max()))
    
    # Display most commonly used end station
    stations = df.groupby(['End Station'])['End Station'].count()
    print("The most common end station is: {} with {} records".format(stations.idxmax(),stations.max()))

    # Display most frequent combination of start station and end station trip
    stations = df.groupby(['Start Station','End Station'])['Start Station'].count()
    print("The most common combination of stations are start: {} and end: {} with {} records".format(stations.idxmax()[0],stations.idxmax()[1],stations.max()))

    print("\nThis took %s milliseconds." % round((time.time() - start_time)*1000,2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    # Convert the seconds to days to make this more readable (60s * 60m * 24h)
    sum_days = round(df['Trip Duration'].sum()/86400,2)
    print("The total travel time was {} days".format(sum_days))

    # Display mean travel time in minutes
    mean_minutes = round(df['Trip Duration'].mean()/60,2)
    print("The mean travel time was {} minutes".format(mean_minutes))

    print("\nThis took %s milliseconds." % round((time.time() - start_time)*1000,2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The following users were found:")
    print(df['User Type'].value_counts())
    
    # Display counts of gender
    if set(['Gender']).issubset(df.columns):
        print("\nThe following genders were found:")
        print(df['Gender'].value_counts())
    else:
        print("\nUnfortunately, this dataset does not have information about gender.")

    # Display earliest, most recent, and most common year of birth
    if set(['Birth Year']).issubset(df.columns):
        print("\nThe earliest year of birth is {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is {}".format( int(df['Birth Year'].max())))
        print("The most common year of birth is {}".format( int(df['Birth Year'].mode())))
    else:
        print("\nUnfortunately, this dataset does not have information about birth year.")
        
    print("\nThis took %s milliseconds." % round((time.time() - start_time)*1000,2))
    print('-'*40)
    
    
def raw_data(df):
    """Asks users if they want to see the raw data."""
    
    # If applicable show all columns of the data frame
    pd.set_option('display.max_columns', None)
    
    answer = input("Would you like to see the raw data? yes or no: ")
    
    index_count = 0
    
    if(answer.lower() == "yes"):
        
        while (answer.lower() != "no"):   
            
            if(answer.lower() == "yes"):
                
                #If we reach the end of the raw data we want to cap the report and end the loop
                #otherwise report RAW_DATA_SIZE rows of raw data and ask if they want more.
                if(index_count + RAW_DATA_SIZE <= len(df)):
                    print(df[index_count:index_count+RAW_DATA_SIZE])
                else:
                    print(df[index_count:])
                    print("End of raw data")
                    break
                
            elif (answer.lower() != "no"):
                print("I don't understand, please try again.")
            
            answer = input("Would you like to see an additional 5 rows? yes or no: ")
            
            index_count += RAW_DATA_SIZE
                
    elif (answer.lower() != "no"):
        print("I don't understand, please try again.")
        
        #recursively ask question until it receives valid input
        raw_data(df)
        


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
