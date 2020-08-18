import functions
import os
import yaml
from prettytable import PrettyTable

options={}
#get command line arguments
options = functions.func_get_arguments()

# get file list in directory
config_list= os.listdir(options['directory'])

#load yaml file
baseline_yaml_file = open(options['baseline_yaml'])
baseline_config = yaml.load(baseline_yaml_file,Loader=yaml.FullLoader)

# loop through config files
for config in config_list:
    file = options['directory'] + "\\" + config
    print("##############################")
    print("## " + file)
    print("##############################\n")

    table = PrettyTable()
    table.field_names = ["scope","command","type","result"]

    # open file and read content
    with open(file) as f_obj:
        content = f_obj.read()

        functions.func_check_global(content,baseline_config,table)
        # check all interfaces against baseline
        functions.func_check_interface(content,baseline_config,table)
        
        f_obj.close()

    print(table)
    print("\n")