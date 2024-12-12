
import os
import platform
import sys
from single_measurement_files import framework
from termcolor import colored
from single_measurement_files.output import report_function
from collections import defaultdict
from single_measurement_files.save_report_to_csv import save_report_to_csv

def launch_measurement(input_filename=None, target_attribute_ML=None, num_to_categ = None, possible_known_attributes = None, secret_mode = None,  save_my_report_to_csv = None):

   
    plat = platform.system()
    items = None
    if plat == "Linux":
        if "microsoft" in platform.uname()[2].lower():
            print("This is a SubSystem for Linux")
            print("Executing the framework for non-Linux systems")
            items = framework.main_framework(input_filename, target_attribute_ML, num_to_categ, possible_known_attributes, secret_mode, 0)
            plat = 'Windows_WSL'
        else:
            print("Not running on WSL")
            print("The operating system is ", plat, ".")
            items = framework.main_framework(input_filename, target_attribute_ML, num_to_categ,  possible_known_attributes, secret_mode, 1)
            

    else:
        print("The operating system is ", plat, ".")
        items = framework.main_framework(input_filename, target_attribute_ML, num_to_categ,  possible_known_attributes, secret_mode, 0)
    items['input']['OS'] = plat
    if plat == "Linux":
        items['input']['Tool'] = "pyRAPL"
    else:
        items['input']['Tool'] = "CodeCarbon"
    report_function(items)
    
    # if not hasattr(sys.stdin, 'isatty') or sys.stdin.isatty():
    #     csv_request = input('Do you want it to be saved in .CSV? (Y for Yes, Nothing for no): ').replace(" ", "").upper()
    #     if csv_request == "Y":
    #         save_my_report_to_csv = 'Y'
    # if save_my_report_to_csv == 'Y':
    #     save_report_to_csv(items)
    print(f"You can find the report in the \'reports\' folder with the ID {items['ID']} !")
    
        



if __name__ == '__main__':
    launch_measurement()