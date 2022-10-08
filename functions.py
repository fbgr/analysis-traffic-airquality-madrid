import pandas as pd
import numpy as np
import datetime
import csv
import re 

def round_up(x):
    # Rounds up the number when its decimal part >0, otherwise round down
    if x%1> 0.00000000001:
        return int(x+1)
    return int(x)

def aggregate_time(data,time_column,days=7):
    # Creates a new column with the first day of its time range. Useful for time agreggating.

    # Initializing
    rango = (data[time_column].max()-data[time_column].min()).days # how many days before oldest and newest date
    interval = datetime.timedelta(days=days) # creating a interval with length days defined above
    dynamic_date = data[time_column].min() # Starting the dynamic date on the first date 

    # Iterating for each week 
    for i in range(round_up(rango/days)):
        # computing the range for that week
        week_i = pd.date_range(start=dynamic_date, end=dynamic_date+interval)
        # removing hours from the days on week_i
        week_i = list(map(lambda x: x.date(),week_i))

        # updating the column 'week' for the rows that lie within week_i
        data.loc[data[time_column].dt.date.isin(week_i),'time_range'] = dynamic_date
        # updating dynamic_date for next iteration
        dynamic_date = dynamic_date+interval
    
    return data


def get_separator(file):
    with open(file, newline='') as f:
        csv_reader = csv.reader(f)
        csv_headings = next(csv_reader)
        first_line = next(csv_reader)
        
    separator = re.findall(r'[;]',csv_headings[0])
    
    if len(separator)>0:
        return ";"
    return ","

def aggregate_time2(data,time_column,days=15):
    printing = 0
    updating = round_up(len(data)*0.05)
    # Creates a new column with the first day of its time range. Useful for time agreggating.
    data = data.sort_values(by=time_column)

    # Initializing
    rango = (data[time_column].max()-data[time_column].min()).days # how many days before oldest and newest date
    interval = datetime.timedelta(days=(days-1)) # creating a interval with length days defined above
    dynamic_date = data[time_column].min() # Starting the dynamic date on the first date 
    
    # Iterating for each week
    weeks = []
    for i in range(round_up(rango/days)+1):
        # computing the range for that week
        weeks.append(pd.date_range(start=dynamic_date, end=dynamic_date+interval))
        # removing hours from the days on week_i
        weeks[i] = list(map(lambda x: x.date(),weeks[i]))
        dynamic_date = dynamic_date+datetime.timedelta(days=(days))
    
    aux = 0
    dynamic_date = data[time_column].min() # Starting the dynamic date on the first date 
    for i,row in data.iterrows():
        if data.loc[i,time_column].date() in (weeks[aux]):
            data.loc[i,'time_range'] = dynamic_date
        else:
            aux +=1
            dynamic_date = dynamic_date+datetime.timedelta(days=(days))
            data.loc[i,'time_range'] = dynamic_date
        # updating the column 'week' for the rows that lie within week_i
        # Optional ~ printing
        if (i+1)%updating==0:
            printing += updating
            print('%.1f%% completed.' %(printing/len(data)*100),end='\r')
    print('100.0% completed.',end='\r')
    
    return data


"""
    def get_separator(file):
    with open(file, newline='') as f:
        csv_reader = csv.reader(f)
        csv_headings = next(csv_reader)
        first_line = next(csv_reader)
        
    separator = re.findall(r'[;]',csv_headings[0])
    
    if len(separator)>0:
        return ";"
    return ","""