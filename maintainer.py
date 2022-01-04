# OPEN WEBCAM MAINTAINER

# Author: Shaikh Aquib
# Description: Runs through all the values in CSV and checks if host are alive, 
# if host does not replay to ping the value is deleted from file

import subprocess 
import copy
import pandas

class Maintainer:
    def __init__(self, filename, ip_addr_col, location_col):
        print("$$$$$$$$$$$$ OPEN WEBCAM MAINTAINER $$$$$$$$$$$$$$$\nAuthor: Shaikh Aquib\n")
        self.filename = filename
        self.__data = self.read_to_dict(filename)
        self.__ip_addr_col = ip_addr_col
        self.__location_col = location_col

    def read_to_dict(self, filename, sep='\t'):
        """Reads the CSV data and converts it into a dict list."""
        df = pandas.read_csv(filename, sep=sep)
        return df.to_dict('list')

    def ping(self, ip_address: str, verbose=True) -> int:
        """Runs ping command on system

        Parameters
        ----------
        ip_address: str
            IP Address of the server to ping

        Returns
        -------
        response: int
            0 if sucessfull, 1 if unsucessfull.
        """
        if verbose:
            print(f"[+] Pinging {ip_address}")
        response = subprocess.Popen(f"ping -c 1 {ip_address}", shell=True, stdout=subprocess.PIPE)
        response.wait()
        return response.returncode

    def perform_validation(self, ip_address, response):
        """Checks the response, 
        if the response indicates that server is down then it deletes the row.
        """
        TARGET_ACTIVE = 0
        if (response != TARGET_ACTIVE):
            print("[!] Target inactive, removing record...")
            index = self.__data[self.__ip_addr_col].index(ip_address)
            self.delete_row(index)

    def delete_row(self, index):
        for col in self.__data.keys():
            del self.__data[col][index]

    def run(self):
        dcopy = copy.deepcopy(self.__data)
        total_rows = len(dcopy[self.__ip_addr_col])

        for i in range(0, total_rows):
            ip_with_port = dcopy[self.__ip_addr_col][i]
            ip = ip_with_port.split(":")[0]
            location = dcopy[self.__location_col][i]
            response = self.ping(ip, verbose=True)
            self.perform_validation(ip_with_port, response)

        self.save()
        print("###"*10)

    def save(self):
        print("[+] Saving file")
        df = pandas.DataFrame(self.__data)
        df.to_csv(self.filename, sep='\t', index=False)


if __name__ == "__main__":
    filename = 'webcamXP5.csv'
    ip_addr_col = 'IP'
    location_col = 'Location'
    
    worker = Maintainer(filename, ip_addr_col, location_col)
    worker.run()
