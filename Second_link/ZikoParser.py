import json
import requests
from bs4 import BeautifulSoup
from secondary_defs import *

class ZikoParser():
    def __init__(self) -> None:
        self.link_site = 'https://www.ziko.pl/lokalizator/'
        self.link_json = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'
        self.final_results = []

    def create_request_json(self) -> None:
        self.request_json = requests.get(self.link_json).json()


    def create_beautifulsoup(self) -> None:
        r = requests.get(self.link_site)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    
    def get_all_request(self) -> None:
        self.create_request_json()
        self.create_beautifulsoup()

   
    def find_elements(self) -> None:
        self.finded_elements = find_table(self.soup)


    def get_id(self, item: dict) -> None:
        self.id = get_id(item)

    
    def get_address(self) -> None:
        self.address = get_address(self.request_json, self.id)

    
    def get_latlon(self) -> None:
        self.latlon = get_latlon(self.request_json, self.id)


    def get_name(self) -> None:
        self.name = get_name(self.request_json, self.id)

    
    def get_phones(self, item: dict) -> None:
        self.phones = get_phones(item)

    
    def get_working_hours(self, item: dict) -> None:
        self.working_hours = get_working_hours(item)


    def get_data(self, item: dict) -> None:
        self.get_id(item)
        self.get_address()
        self.get_latlon()
        self.get_name()
        self.get_phones(item)
        self.get_working_hours(item)


    def add_info_funal_result(self) -> None:
        fast_dict = {
            "address": self.address,
            "latlon": self.latlon,
            "name": self.name,
            "phones": self.phones,
            "working_hours": self.working_hours
        }

        self.final_results.append(fast_dict)


    def create_json_file(self) -> None:
        json_object = json.dumps(self.final_results, indent=4, ensure_ascii=False)

        with open("sample_zikoparser.json", "w", encoding='utf-8') as outfile:
            outfile.write(json_object)


    def solve_ziko_parser(self) -> None:
        self.find_elements()
        for item in self.finded_elements:
            self.get_data(item)
            self.add_info_funal_result()
        self.create_json_file()
