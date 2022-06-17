import requests
from bs4 import BeautifulSoup
from secondary_defs import *
import re
import json


class MonomarchParser():
    def __init__(self) -> None:
        self.link = 'https://monomax.by/map'
        self.final_results = []

    def get_data(self):
        r = requests.get(self.link)
        self.soup = BeautifulSoup(r.text, 'lxml')

    
    def get_shop_forms(self):
        self.shops = self.soup.find_all('div', class_='shop')


    def get_address_and_name(self, shop):
        self.address, self.name = get_address_and_name(shop)


    def get_phones(self, shop):
        self.phones = get_phones(shop)

    
    def get_script(self):
        self.script = self.soup.find_all('script', type="text/javascript")[-1].text

    
    def get_all_coordinates(self):
        self.list_coordinates = re.findall("\[\d+\.\d+\,\s\d+\.\d+\]", self.script)
    

    def get_coordinates(self, id):
        self.coordinates = self.list_coordinates[id].replace('[', '').replace(']', '').split(',')


    def add_info_funal_result(self) -> None:
        fast_dict = {
            "address": self.address,
            "latlon": self.coordinates,
            "name": self.name,
            "phones": self.phones,
            }

        self.final_results.append(fast_dict)


    def create_json_file(self) -> None:
        json_object = json.dumps(self.final_results, indent=4, ensure_ascii=False)

        with open("sample_monomarchparser.json", "w", encoding='utf-8') as outfile:
            outfile.write(json_object)


    def solve_monomarch_parser(self):
        self.get_data()
        self.get_shop_forms()
        self.get_script()
        self.get_all_coordinates()

        for index, shop in enumerate(self.shops):            
            self.get_address_and_name(shop)
            self.get_coordinates(index)
            self.get_phones(shop)
            self.add_info_funal_result()
    
        self.create_json_file()

