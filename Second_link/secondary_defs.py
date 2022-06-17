def find_table(soup):
    return soup.find_all('tr', class_='mp-pharmacy-element')


def get_id(item: dict):
    return item.get('data-mp-id')


def get_address(json, id):
    address = json.get(id).get("address")
    city = json.get(id).get("city_name")[0]
    full_address = '{}, {}'.format(address, city)
    return full_address


def get_latlon(json, id):
    lat = json.get(id).get('lat')
    lon = json.get(id).get('lng')
    return [lat, lon]


def get_name(json, id):
    name = json.get(id).get("title")
    return name


def get_phones(item):
    phones = item.find('td', class_='mp-table-address').text.split('tel. ')[1].replace('Infolinia: ', '-').split('-')
    return phones

def get_working_hours(item):
    working_hours = item.find('td', class_='mp-table-hours').find_all('span')
    fast_list =[]

    while len(working_hours)!=0:
        first_item = working_hours.pop(0).text
        second_item = working_hours.pop(0).text
        fast_list.append([first_item, second_item])
    
    new_list = []
    for i in fast_list:
        s = ' '.join(i)
        new_list.append(s)
    return new_list