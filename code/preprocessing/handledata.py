# Imports


import math
import random
import pandas as pd
import csv
import numpy as np


'''
This class deals with reading in all of the data and storing it in a format we can work with - the pandas dataframe.
'''


class Handledata:
    def __init__(self):
        print("Doing nothing in constructor woo")

    #Takes in the default dataframe and converts it to a format we want
    def preprocess_data(self, raw_data):
        print("In preprocess function")

    def read_raw_data(self):
        with open('../../data/data.csv','rt')as f:
            data = csv.reader(f)
            column_names = next(data)
            data_frame = pd.read_csv('../../data/data.csv', names=column_names)
                
                    
            return data_frame.drop(0)

#this function for converting Latitude and Longitude data into a 3-dimensional
#representation of data was taken from StackOverflow at this link
#https://stackoverflow.com/questions/10473852/convert-latitude-and-longitude-to-point-in-3d-space
    def convert(self, lat, lon):
        # see http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html

        #print("Lat long:", lat, lon)
        rad = np.float64(6378137.0)        # Radius of the Earth (in meters)
        x = (rad )*np.sin(-(lat-90)*np.pi/180) * np.cos((lon+180)*np.pi/180)
        y = (rad )*np.sin(-(lat-90)*np.pi/180)* np.sin((lon+180)*np.pi/180)
        z = (rad )*np.cos(-(lat-90)*np.pi/180)

        return [x, y, z]        
            

    def ones(self, raw_data_frame):
    #turn the data into 1's (if number is greater than 50) or a 0 (if number is less than 50)
        for column_labels, column_values in raw_data_frame.items():
            row_num = 0
            if (column_labels != 'Province/State') and (column_labels !='Country/Region') and (column_labels !='Lat') and (column_labels !='Long'):
                for col_val in column_values:
                    #x = corona_data_frame.loc[row_num+1, column_labels]

                    if int(col_val) <= 50:
                        raw_data_frame.loc[row_num+1, column_labels] = 0
                    else:
                        raw_data_frame.loc[row_num+1, column_labels] = 1
                    row_num = row_num + 1
        #if there are more than 50 cases in a country, they will have a 1 for true in that date slot, and 0 otherwise. 
        #print(corona_data_frame)
        return raw_data_frame
          

    def tosphere(self, corona_data_frame):
        all_days= []
        for column_labels, column_values in corona_data_frame.items():
            row_num = 0

            location_label = []
            province_label = []
            lat_long = []

            one_day = []
            if (column_labels != 'Province/State') and (column_labels !='Country/Region') and (column_labels !='Lat') and (column_labels !='Long'):
                for col_val in column_values:
                    if int(col_val) == 1:
                        lat = float(corona_data_frame.loc[row_num+1, "Lat"])
                        lon = float(corona_data_frame.loc[row_num+1, "Long"])
                        #convert Latitude, Longitude data into a 3D representation of that same data
                        #will let TDA occur correctly at all points on a map
                        converted_loc = self.convert(lat, lon)
                        #send the converted data into a list, having all points for one day in one list together
                        one_day.append(converted_loc)
                        location_label.append(corona_data_frame.loc[row_num+1,'Country/Region'])
                        province_label.append(corona_data_frame.loc[row_num+1,'Province/State'])
                        lat_long.append([lat,lon])



                        #add one_day entry to the entire collection of data in a List data structure
                    row_num = row_num + 1

                one_day = np.array(one_day)

                all_days.append(one_day)
                all_days.append(location_label)
                all_days.append(province_label)
                all_days.append(lat_long)
                '''
                for x in range(0,one_day.size/3):
                    print(one_day[x], location_label[x], province_label[x])
                '''
        # hold all the data in a numpy array, indexed such that day 1  (January 22, 2020) = 0
        #print(all_days[1])

        corona_3D_data = np.array(all_days)
        return corona_3D_data




if __name__ == '__main__':
    print('Running COVID-19 Preprocessor...')

    preprocess_impl = Handledata()

    corona_data_frame = preprocess_impl.read_raw_data()

    '''
    for column_label, column_values in corona_data_frame.items():
        print(column_label, column_values[1])
    '''
    corona_data_frame = preprocess_impl.ones(corona_data_frame)

    point_data = preprocess_impl.tosphere(corona_data_frame)

    y = 4*2
    for x in range(0,len(point_data[y])):
        print(point_data[y][x], point_data[y+1][x], point_data[y+2][x], point_data[y+3][x])
    #print(point_data.shape)

               
        

#OUTPUT: Pandas dataframe with rows going from 1 to n, each representing a geographic area and its time evolution of coronavirus cases over time. 





