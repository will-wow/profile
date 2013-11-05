#!/usr/bin/python3

from addresscheck import File, AddressChecker

def main():
    '''main function'''
    #--init. the file instance--#
    billing = File('billing.csv')
    billing.zip_col(6)
    billing.city_col(4)
    billing.state_col(5)
    billing.other_col(0,'acct')
    billing.other_col(1,'name')
    billing.other_col(2,'street1')
    billing.other_col(3,'street2')

    #--init. the file instance--#
    service = File('service.csv')
    service.zip_col(8)
    service.city_col(4)
    service.county_col(5)
    service.state_col(7)
    service.other_col(0,'acct')
    service.other_col(1,'name')
    service.other_col(2,'street1')
    service.other_col(3,'street2')
    service.other_col(6,'county code')

    checker = AddressChecker()
    checker.check_file(billing)
    checker.check_file(service)

main()

