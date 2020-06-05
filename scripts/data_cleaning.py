# !/usr/bin/python
import sys
import pandas
from datetime import datetime


def lookup_value_in_df(flights, x, df, value):
    return df.loc[df["IATA_CODE"] == x, value].iloc[0]


def lookup_coordinates_in_df(flights, x, df):
    return [lookup_value_in_df(flights, x, df, "LONGITUDE"), lookup_value_in_df(flights, x, df, "LATITUDE")]


def airports_data(flights, df, tuples, pairs):
    for t0, t1, t2 in tuples:
        flights[t0] = flights[t1].map(lambda x: lookup_value_in_df(flights, x, df, t2))
    for p0, p1 in pairs:
        flights[p0] = flights[p1].map(lambda x: lookup_coordinates_in_df(flights, x, df))


def time_to_HHSS(number):
    number = str(int(number))
    while len(number) < 4:
        number = '0' + number
    return number[:2] + ":" + number[2:]


def columns_time_to_HHSS(flights, cols):
    for col in cols:
        flights[col] = flights[col].map(lambda x: time_to_HHSS(x))


def main():
    path = "./" if len(sys.argv) < 2 else sys.argv[1]

    flights = pandas.read_csv(path + 'flights.csv', error_bad_lines=False, nrows=100000)
    airports = pandas.read_csv(path + 'airports.csv', error_bad_lines=False)
    airlines = pandas.read_csv(path + 'airlines.csv', error_bad_lines=False)

    flights.dropna(
        subset=['YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
                'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT',
                'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
                'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'ARRIVAL_DELAY', 'DIVERTED', 'CANCELLED'],
        inplace=True)

    flights['DATE'] = flights.apply(lambda row: str(datetime(row['YEAR'], row['MONTH'], row['DAY']))[:10], axis=1)
    flights.drop(columns=['YEAR', 'MONTH', 'DAY'], inplace=True)

    flights["AIRLINE_NAME"] = flights["AIRLINE"].map(lambda x: lookup_value_in_df(flights, x, airlines, 'AIRLINE'))
    flights.rename(columns={"AIRLINE": "AIRLINE_CODE"}, inplace=True)

    tuples = [("ORIGIN_AIRPORT_NAME", "ORIGIN_AIRPORT", "AIRPORT"), ("ORIGIN_AIRPORT_CITY", "ORIGIN_AIRPORT", "CITY"),
              ("ORIGIN_AIRPORT_STATE", "ORIGIN_AIRPORT", "STATE"),
              ("ORIGIN_AIRPORT_COUNTRY", "ORIGIN_AIRPORT", "COUNTRY"),
              ("DESTINATION_AIRPORT_NAME", "DESTINATION_AIRPORT", "AIRPORT"),
              ("DESTINATION_AIRPORT_CITY", "DESTINATION_AIRPORT", "CITY"),
              ("DESTINATION_AIRPORT_STATE", "DESTINATION_AIRPORT", "STATE"),
              ("DESTINATION_AIRPORT_COUNTRY", "DESTINATION_AIRPORT", "COUNTRY")]
    pairs = [("ORIGIN_AIRPORT_COORDINATES", "ORIGIN_AIRPORT"),
             ("DESTINATION_AIRPORT_COORDINATES", "DESTINATION_AIRPORT")]

    airports_data(flights, airports, tuples, pairs)
    del tuples, pairs

    columns_time_to_HHSS(flights, ["SCHEDULED_DEPARTURE", "DEPARTURE_TIME", "WHEELS_OFF", "WHEELS_ON"])

    flights.to_json(path + 'dataset.json', orient='records', lines=True)


main()
