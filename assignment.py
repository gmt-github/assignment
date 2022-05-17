import re
import argparse

from pathlib import Path
from collections import Counter


usage_help = """
            -h (--help) ==> Argument usage help
            -f (--file) ==> To provide full extended path
            -cdb (--count_date_basis) ==> To count data on date basis
            -cub (--count_ua_basis) ==> To count data on user agent basis
            -cvb (--count_verb_basis) ==> To count data on verb basis
"""
#*********************** Global APACHE REGEX ******************************************************
APACHE_REGEX = '\[([\w:/]+\s[+\-]\d{4})\] \"(.+?)\" (\\d{3}) (\\d+) \"([^\"]+)\" \"(.+?)\"'
#................. This can be reffered from apache documentation .................................

def count_per_day_data(file_data):
    APACHE_ACCESS_LOG_PATTERN = r'\[([\w:/]+\s[+\-]\d{4})\]'
    log_pattern_match_value = re.findall(APACHE_ACCESS_LOG_PATTERN, str(file_data))
    find_value = [sp.split(":")[0] for sp in log_pattern_match_value if re.search("\d{2}/(Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)/\d{4}", sp) is not None ]
    date_wise_data_count = Counter(find_value)
    return date_wise_data_count

def count_per_day_user_agent_data(file_data):
    global_pattern_match = re.findall(APACHE_REGEX, file_data)
    date_count = [(i[0].split(":")[0], i[-1])  for i in global_pattern_match]
    counter_user_agent_wise  = Counter (e for e in date_count).most_common(3)
    dict_count_ua_data = dict(counter_user_agent_wise)
    return dict_count_ua_data


def count_os_per_day_verb_data(file_data):
    # Count the number of GET and POST on the basis of OS currently we are count "windows", "linux" and "darwin" it and be added up more just to another or value
    global_pattern_match = re.findall(APACHE_REGEX, file_data)
    output_dict_os_wise = {}
    os_specific_find = [(i[0].split(":")[0].strip(), re.search("Windows|Linux|Darwin", i[-1], re.IGNORECASE).group(), i[1].split("/")[0].strip()) for i in global_pattern_match if re.findall("Windows|Linux|Darwin", i[-1], re.IGNORECASE) != []]
    counter_os  = dict(Counter (e for e in os_specific_find))
    for keys, val in counter_os.items():
        output_dict_os_wise.setdefault(keys[0], {}).setdefault(keys[1], {}).setdefault(keys[2], {val})
    return output_dict_os_wise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=usage_help, description='Description of your program')
    parser.add_argument('-f','--file', required=True, action="store", type=Path)
    parser.add_argument('-cdb', '--count_date_basis', required=False, action="store_true")
    parser.add_argument('-cub', '--count_ua_basis', required=False, action="store_true")
    parser.add_argument('-cvb', '--count_verb_basis', required=False, action="store_true")
    args = parser.parse_args()

    if args.file:
        file_name = args.file
        if file_name.exists(): # Expecting file in same directory, can be provided full path using os.join method {keeping it simple}
            try:
                with file_name.open('r') as fb:
                    fl_dsptr = fb.read()
                    print (type(fl_dsptr))
                    if args.count_date_basis:
                        date_wise_value = count_per_day_data(fl_dsptr)
                        for k, v in date_wise_value.items(): 
                            print("Number of request on " + str(k) + " " + "is "  + "==> " + str(v))
                    elif args.count_ua_basis:
                        dict_ua_wise = count_per_day_user_agent_data(fl_dsptr)
                        print (f"\n\n*****************************************************\n")
                        print (dict_ua_wise)
                        print (f"\n\n*****************************************************\n")
                    elif args.count_verb_basis:
                        dict_verb_wise = count_os_per_day_verb_data(fl_dsptr)
                        print (f"\n\n*****************************************************\n")
                        print (dict_verb_wise)
                        print (f"\n\n*****************************************************\n")
                    else:
                        print (usage_help)
            except BaseException as err :
                raise "ERROR !!! file {} not able to read".format(file_name)
        else:
            print ("File Does not exists, Please re-verify the file name")
