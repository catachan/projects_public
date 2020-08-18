import os
import sys
import re
import yaml

def func_check_global(content,baseline_config,table):

    for global_command in baseline_config['global_commands']:
        global_pattern = r"(?m)^"+ global_command

        result = re.search(global_pattern,content)
        if result:
            table.add_row(["Global",global_command,"","PASS"])
        else:
            table.add_row(["Global",global_command,"","FAIL"])

    #print(table)

def  func_check_interface(content,baseline_config,table):
    ###########################################
    # function to parse interface commands
    ###########################################

    # defining regex search pattern
    pattern_interface_block = r"(?m)^interface[^!]*"

    # get all interface config blocks
    interfaces = re.findall(pattern_interface_block,content,re.DOTALL)

    # loop through interface blocks
    for interface in interfaces:

        #DEBUG
        #print(baseline_config)
        #print(interface)

        # get and display interface name
        interface_name = re.match("interface.*",interface)
        
        # check if interface is on blocklist --> set flag then
        exclude_interface = False
        for exclude in baseline_config['interface_exclude']:
            if interface_name[0] == "interface "+exclude:
                exclude_interface = True

        trunk_mode_interface = re.search("switchport mode trunk",interface)
        if trunk_mode_interface:
            trunk_interface = True
        else:
            trunk_interface = False 

        if exclude_interface:
            table.add_row([interface_name[0],"","EXCLUDED",""])
        elif trunk_interface == True:
            for command in baseline_config['uplink_interface_commands']:
                #check if command is there
                result = re.search(command,interface)
                if result:
                    table.add_row([interface_name[0],command,"INT-TRUNK","PASS"])
                else:
                    table.add_row([interface_name[0],command,"INT-TRUNK","FAIL"])
        else:
            # loop through baseline and check if commands exist
            for command in baseline_config['interface_commands']:
                #check if command is there
                result = re.search(command,interface)
                if result:
                    table.add_row([interface_name[0],command,"INT","PASS"])
                else:
                    table.add_row([interface_name[0],command,"INT","FAIL"])
        

def func_get_arguments():
    ###########################################
    # function to get command line arguments
    ###########################################

    i=0
    # define dict to hold options / command line switches
    options={}
    
    #parse through arguments and fill citionary with value pairs
    for argument in sys.argv:
        i=i+1
        if argument == "-d":
            options['directory'] = sys.argv[i]
        elif argument == "-b":
            options['baseline_yaml'] = sys.argv[i]

    

    if "baseline_yaml" not in options:  
        print("-b is mandatory")
        exit()
    else:
        if ("directory" or "connection_yaml") not in options:
            print("-d (offline mode) or -c (online mode) is mandatory")
            exit()
        else:    
            return options