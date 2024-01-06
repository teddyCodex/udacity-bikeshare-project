import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
MONTHS = {
    "all": 0,
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
}

DAYS = [
    "all",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("\nHello! Let's explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            "\nPlease enter a city (Chicago, New York City, Washington): "
        ).lower()
        if city not in CITY_DATA:
            print(f"{city} is not an available option. Try again.\n")
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Please enter a month (all, january, february, ... , june): "
        ).lower()
        if month not in MONTHS:
            print(f"{month} is not an available option. Try again.\n")
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Please enter a weekday (all, monday, tuesday, ... sunday): "
        ).lower()
        if day not in DAYS:
            print(f"{day} is not an available option. Try again.\n")
        else:
            break

    print("-" * 40)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        month_index = MONTHS[month]
        # filter by month to create the new dataframe
        df = df[df["month"] == month_index]
    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    month_count = df["month"].value_counts()
    common_month = month_count.idxmax()
    for month, id in MONTHS.items():
        if id == common_month:
            common_month = month
            break
    print(
        "The most common travel month is {} with {} trips.".format(
            common_month.title(), month_count.max()
        )
    )

    # display the most common day of week
    day_count = df["day_of_week"].value_counts()
    common_day = day_count.idxmax()
    print(
        "The most common travel day is {} with {} trips.".format(
            common_day.title(), day_count.max()
        )
    )

    # display the most common start hour
    start_hour_count = df["Start Time"].dt.hour.value_counts()
    common_hour = start_hour_count.idxmax()
    if common_hour < 10:
        print("The most common travel hour is 0{}:00hrs".format(common_hour))
    else:
        print("The most common travel hour is {}:00hrs".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df["Start Station"].value_counts()
    common_start_station = start_station_count.idxmax()
    print(
        "The most commonly used start station is {} with {} trips".format(
            common_start_station, start_station_count.max()
        )
    )

    # display most commonly used end station
    end_station_count = df["End Station"].value_counts()
    common_end_station = end_station_count.idxmax()
    print(
        "The most commonly used end station is {} with {} trips".format(
            common_end_station, end_station_count.max()
        )
    )
    # display most frequent combination of start station and end station trip
    combined_stations = pd.Series(list(zip(df["Start Station"], df["End Station"])))
    most_freq_station = combined_stations.value_counts().idxmax()
    print(
        "The most frequent start and end station combination is {} to {} with {} trips".format(
            most_freq_station[0],
            most_freq_station[1],
            combined_stations.value_counts().max(),
        )
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(
        "Total travel time is {} seconds // {}".format(
            total_travel_time, pd.to_timedelta(total_travel_time, unit="s")
        )
    )

    # display mean travel time
    avg_trip_duration = df["Trip Duration"].mean()
    print(
        "Average travel time is {} seconds // {}".format(
            avg_trip_duration, pd.to_timedelta(avg_trip_duration, unit="s")
        )
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_type_count = df["User Type"].value_counts()
    print("User Type Counts: \n{}".format(user_type_count))
    print()

    # Display counts of gender
    if "Gender" not in df.columns:
        print("No Gender Data Available")
    else:
        gender_count = df["Gender"].value_counts()
        print("Gender Counts:\n{}".format(gender_count))
    print()

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" not in df.columns:
        print("Birth Year Data Unavailable")
    else:
        birth_year = df["Birth Year"]
        birth_year_count = birth_year.value_counts()
        print("Earliest birth year: {}".format(int(birth_year.min())))
        print("Most recent birth year: {}".format(int(birth_year.max())))
        print("Most common birth year: {}".format(int(birth_year_count.idxmax())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def get_raw_data():
    """Ask user if they want to see 5 lines of raw data

    Returns:
        bool: True or False
    """
    while True:
        choice = input(
            '\nType "yes" to view 5 lines of raw data || "no" to view other stats: '
        ).lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print("Invalid Input")


def generate_raw_data(df: pd.DataFrame):
    """_summary_

    Args:
        df (pd.DataFrame): accepts a dataframe

    Yields:
        DataFrame: Produces sequential chunks of data (5 lines)
    """
    start_index = 0

    while start_index < len(df):
        end_index = start_index + 5
        yield df.iloc[start_index:end_index]
        start_index = end_index


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # ask if user wants raw data
        if get_raw_data():
            data_chunks = generate_raw_data(df)
            while True:
                print(next(data_chunks))
                choice = input("Press Enter for 5 more lines or type 'no' to exit: ")
                if choice == "no":
                    break
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
