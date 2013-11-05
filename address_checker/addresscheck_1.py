#!/usr/bin/python3
'''
Address Check:
    turns a zipcode database csv into a dictionary
    then checks it against given table
    and writs files of all inconsistencies
Author: Will Lee-Wagner, 2013

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import csv
import sys
import re
import pickle

class _Column:
    '''Column: a class to hold the data about an input column'''
    def __init__(self, col, title, out_file=None):
        self.col = col
        self.title = title
        self.check = False
        if out_file:
            self.check = True # flag that this Col should be checked
            self.bad_file = open(out_file, 'w')
            self.writer = csv.writer(self.bad_file)

class File:
    '''File: a class hold the info on an input file'''
    def __init__(self, file):
        '''get the name of the file being parsed through and other file init.'''
        file_name_match = re.match(r"^(.*)\.", file)
        # file info
        self.file = file #file.csv
        self.file_name = file_name_match.group(1) #file (no csv)
        # static output info
        self.OUTPUT_PATH = '/home/kaaaaaahnsolo/Web/public_html/crane/'
        # set up columns in lists to loop through
        self.cols = [] # holds the Column instances
    
    #Methods to create Column instances for all checked rows
    def zip_col(self, col):
        '''set up the zip column'''
        # instance the Column class
        title = 'zip'
        out_file = self.OUTPUT_PATH + self.file_name + '_bad_zip.csv' # file name
        self.cols.append(_Column(col, title, out_file))

    def city_col(self, col):
        '''set up the city column'''
        # instance the Column class
        title = 'city'
        out_file = self.OUTPUT_PATH + self.file_name + '_bad_city.csv' # file name
        self.cols.append(_Column(col, title, out_file))
    
    def state_col(self, col):
        '''set up the state column'''
        # instance the Column class
        title = 'state'
        out_file = self.OUTPUT_PATH + self.file_name + '_bad_state.csv' # file name
        self.cols.append(_Column(col, title, out_file))

    def county_col(self, col):
        '''set up the county column'''
        # instance the Column class
        title = 'county'
        out_file = self.OUTPUT_PATH + self.file_name + '_bad_county.csv' # file name
        self.cols.append(_Column(col, title, out_file))
    
    def other_col(self, col, title):
        '''Add other columns to be printed but not checks (like street address)'''
        self.cols.append(_Column(col, title))
    
    def c(self, title):
        '''c: return the column# of the named column'''
        column = None
        for col in self.cols:
            if col.title == title:
                column = col # get the col#
        return column #return the column object, or None if not found
    
    def base_row(self, row):
        '''base_row: return a row of data for writing'''
        row_list = []
        for c in self.cols:
            row_list.append(row[c.col])
        return row_list
    
    def close_files(self):
        '''close all open bad_files'''
        for c in self.cols:
            if c.check:
                c.bad_file.close()

class AddressChecker:
    '''AddressChecker: a class to check a given table of addresses against post office data'''
    
    def __init__(self):
        '''Create the dictionary from the post office info'''
        with open('zip_db.pickle','rb') as f:
            self.zips = pickle.load(f)
            self.db_cols = {'city':0, 'state':1, 'county':2} # track where the cols end up
    
    def _make_header(self, header_list, col):
        '''make_header: return a header list for a bad_col sheet'''
        new_header_list = list(header_list)
        new_header_list.append(col.title + '_correct')
        return new_header_list
    
    def _print_headers(self, file):
        '''print_headers: write the headers to the bal_col sheets'''
        # create the base header list
        headers = [] 
        file.cols.sort(key = lambda c: c.col) # sort the columns by col#
        for c in file.cols:
            headers.append(c.title) # add the column titles to the header list
        # write to the bal_cols files
        for c in file.cols:
            if c.check: # only cols that are checked
                if c.title == 'zip':
                    c.writer.writerow(headers) #zip doesn't get any extra cols
                else:
                    c.writer.writerow(self._make_header(headers, c))
    
    def _case_state(self, value):
        '''return upper if state, title otherwise'''
        if len(value) == 2:
            return value.upper()
        else:
            return value.title()
    
    def _case_value(self, value):
        '''set the case of a list or string for printing'''
        if isinstance(value,list):
            return_val = []
            for n in value:
                return_val.append(self._case_state(n))
        else:
            return_val = self._case_state(value)
        return return_val

    def check_file(self, file):
        '''check_file: check a given file against the zip database'''
        # get the dictionary of correct info
        zips = self.zips
        
        # make headers for the log files
        self._print_headers(file)
        
        with open(file.file) as f: #open the user's file
            reader = csv.reader(f)
            for r in reader: # for each row
                zip = r[file.c('zip').col][0:5] #get the 5-digit zip for lookup (still return the full zip)
                if zip not in zips: #if the zip code is not in the zip db
                    file.c('zip').writer.writerow(file.base_row(r))
                else: # if the zip is in the db, check the check columns
                    for c in file.cols:
                        if c.title != 'zip' and c.check:
                            # check if the given value = or is in the db values for that zip
                            check_value = zips[zip][self.db_cols[c.title]]
                            if isinstance(check_value,list): # multiple ciites
                                in_check = r[c.col].lower() not in check_value
                            else: #single value
                                in_check = r[c.col].lower() != check_value
                            if in_check: # if either test was true:
                                print_row = list(file.base_row(r))
                                #append the checked column 
                                print_row.append(self._case_value(check_value))
                                # write to the file
                                c.writer.writerow(print_row)
        # close the bad_col files
        file.close_files()

def main():
    '''main test function'''
    #--init. the file instance--#
    file = File('billing.csv')
    file.zip_col(6)
    file.city_col(4)
    file.state_col(5)
    #file.county_col()
    file.other_col(0,'acct')
    file.other_col(1,'name')
    file.other_col(2,'street1')
    file.other_col(3,'street2')
    
    checker = AddressChecker()
    checker.check_file(file)
    
if __name__ == '__main__':
    main()
