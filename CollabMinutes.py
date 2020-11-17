import csv
import datetime
import Utilidades as ut
import sys


#fileName = 'AttendeeReport_UDLAP_2020-11-01_2020-11-12.csv'
#fileName = 'AttendeeReport_UCNCI_2020-11-01_2020-11-12.csv'
#fileName = 'AttendeeReport_UNITEC_2020-11-01_2020-11-12.csv'
#fileName = 'AttendeeReport_ULACIT_2020-11-01_2020-11-12.csv'

if __name__ == "__main__":
    param = ut.mainMinutes(sys.argv[1:])
    print(ut.collabMinutes(param[0]))



