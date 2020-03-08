# This scipt downloads the KML feed from Garmin's MapShare

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import os

try:
    import secret
except ModuleNotFoundError as err: 
    if str(err) == "No module named 'secret'":
        print(str(err), '\n\n Make a secret.py file containing a dictionary'
            ' with username, password, and delay key-value pairs.')
        exit()

class Get_KML():
    def __init__(self, username, password):
        """
        This class downloads and parses the KML feed from Garmin's InReach 
        portal and appends the user's current coordinates to a 
        coordinates.csv file. 

        Parameters
        ----------
        username : str
            Garmin MapShare username
        password : str
            Garmin MapShare password

        Returns
        -------
        coordinates : len(2) array
            The current user coordinates that are saved to 
            coordinates.csv file.
        """
        self.username = username
        self.password = password
        return

    def request_loop(self, request_delay):
        """
        Make periodic KML requests and then sleep for request_delay
        minutes between requests.
        
        Parameters
        ----------
        request_delay : int
            Number of minutes to sleep between requests. If 0 will 
            not make automatically request
        """
        if request_delay > 0:
            while True:
                print(f'Running KML request loop at {pd.datetime.now()}')
                # Download and append the current coordinates
                self.get_coordinates()
                self.save_coordinates()
                # Put the script to sleep to be nice to Garmin.
                time.sleep(60*request_delay)
        return

    def get_coordinates(self):
        """
        Request and parse the coordinates and time from the KML file.
        """
        raw_kml = requests.get(f'https://share.garmin.com/Feed/Share/{self.username}',
                                auth=(self.username, self.password))
        self.soup = BeautifulSoup(raw_kml.text, 'html.parser')
        self.current_coordinates = np.fromstring(self.soup.coordinates.text, sep=',')
        self.current_time = pd.to_datetime(self.soup.when.text).replace(tzinfo=None)
        return

    def save_coordinates(self):
        """
        Save the coordiantes to coordinates.csv file if it exists.
        """
        # Write a header if the file does not exist. 
        if os.path.exists('coordinates.csv'):
            header = False
        else:
            header = True

        # Format and save the data
        df = pd.DataFrame(data=np.array([[self.current_time, *self.current_coordinates]]), 
                        columns=['time_utc', 'longitude', 'latitude', 'altitude_meters'])
        df.to_csv('coordinates.csv', mode='a', index=False, header=header)

        # Drop duplicate entries if the KML coordinates have not updated.
        self.drop_duplicates()
        return

    def drop_duplicates(self):
        """ Drop duplicate entries from coordinates.csv file. """
        df = pd.read_csv('coordinates.csv')
        df.drop_duplicates(inplace=True)
        df.to_csv('coordinates.csv', index=False)
        return

if __name__ == '__main__':
    data = Get_KML(secret.secret['username'], secret.secret['password'])
    data.request_loop(1)
    # data.get_coordinates()
    # data.save_coordinates()
