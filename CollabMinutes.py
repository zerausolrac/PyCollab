import csv
import datetime
import Utilidades as ut
import sys



if __name__ == "__main__":
    param = ut.mainMinutes(sys.argv[1:])
    if ut.collabMinutes(param[0]) == None:
        print("The file is not Attendance Report format")




