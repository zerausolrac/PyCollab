import csv
import datetime
import Utilidades as ut
import sys



if __name__ == "__main__":
    param = ut.mainMinutes(sys.argv[1:])
    minutes = ut.collabMinutes(param[0])
    if minutes == None:
        print("The file is not Attendance Report format")
    else:
        print("total minutes:", minutes)




