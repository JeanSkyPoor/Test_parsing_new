from secondary_defs import *
from main_class import MainClass

my_class = MainClass()
my_class.create_request()


for item in my_class.request:
    my_class.get_raw_data(item)
    my_class.transform_phone_data()
    my_class.transform_working_hours()
    my_class.add_info_in_final_results()
    my_class.create_json_file()
