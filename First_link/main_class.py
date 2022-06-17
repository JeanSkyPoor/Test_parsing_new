import requests
import json
from secondary_defs import *


class MainClass():
    def __init__(self) -> None:
        self.link = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
        self.request = None
        self.final_results = []

    def create_request(self):
        self.request = requests.get(self.link).json().get('searchResults')


    def get_raw_address_from_request(self, item: dict) -> None:
        self.address = get_address_from_json(item)
        

    def get_raw_latlon_from_request(self, item: dict) -> None:
        self.latlon = get_latlon_from_json(item)

    
    def get_raw_name_from_request(self, item: dict) -> None:
        self.name = get_name_from_json(item)


    def get_raw_phone_from_request(self, item: dict) -> None:
        self.phone = get_phone_from_json(item)

    
    def get_raw_working_hours_from_request(self, item: dict) -> None:
        self.working_hours = get_working_hours_from_json(item)

    
    def get_raw_status_from_request(self, item: dict) -> None:
        self.status = get_status_from_json(item)

    
    def get_raw_data(self, item: dict) -> None:
        self.get_raw_address_from_request(item)
        self.get_raw_latlon_from_request(item)
        self.get_raw_name_from_request(item)
        self.get_raw_phone_from_request(item)
        self.get_raw_working_hours_from_request(item)
        self.get_raw_status_from_request(item)


    def transform_phone_data(self):
        """
        self.phone type list, for example ['+79218975664'] or ['+74952120000', ['5004', '5003']]
        """
        if self.phone == None:
            self.phone = 'Cannot find phone number'

        keys = self.phone.keys()
        fast_list = []

        for i in keys:
            fast_list.append(self.phone[i])

        if fast_list[1] == []:
            fast_list.pop(1)

        self.phone = fast_list


    def transform_working_hours(self) -> None:
        if self.status == "Closed":
            self.working_hours = ['closed']
            return 

        if self.status == None:
            self.working_hours = "Cannot find status"
            return

        if self.working_hours == None:
            self.working_hours = "Cannot find working hours"
            return

        map_days = {'Monday': 'пн',
            'Tuesday': 'вт',
            'Wednesday': 'ср',
            'Thursday': 'чт',
            'Friday':'пт',
            'Saturday': 'сб',
            'Sunday': 'вс'}
        fast_dict = {}

        for item in self.working_hours:
            start_day = item['timeFrom'][:5]
            end_day = item['timeTill'][:5]
            working_hours = f'{start_day}-{end_day}'

            formatted_day = map_days[item['weekDayName']]
            fast_dict[formatted_day] = working_hours

        formatted_data = format_data(fast_dict)
        working_day_groups = create_working_day_groups(formatted_data)
        self.working_hours = format_working_day_groups(working_day_groups)


    def add_info_in_final_results(self) -> None:
        fast_dict = {
            "address": self.address,
            "latlon": self.latlon,
            "name": self.name,
            "phones": self.phone,
            "working_hours": self.working_hours
        }

        self.final_results.append(fast_dict)


    def create_json_file(self) -> None:
        json_object = json.dumps(self.final_results, indent=4, ensure_ascii=False)

        with open("sample_first_link.json", "w") as outfile:
            outfile.write(json_object)


