def get_address_from_json(item: dict) -> str:

    return item.get('storePublic').get('contacts').get('streetAddress').get('ru')


def get_latlon_from_json(item: dict) -> list:

    return item.get('storePublic').get('contacts').get('coordinates').get('geometry').get('coordinates')


def get_name_from_json(item: dict) -> str:

    return item.get('storePublic').get('title').get('ru')


def get_phone_from_json(item: dict) -> list:

    return item.get('storePublic').get('contacts').get('phone')


def get_working_hours_from_json(item: dict) -> list:

    return item.get('storePublic').get('openingHours').get('regularDaily')


def get_status_from_json(item: dict) -> str:
    
    return item.get('storePublic').get('status')


def format_data(raw_data: dict) -> list:
    result = []
    for key, value in raw_data.items():
        result.append({"day": key, "time": value})

    return result


def create_working_day_groups(raw_working_data: list) -> list:
    current_day = raw_working_data[0]
    groups = []
    current_pair = []
    for index, day in enumerate(raw_working_data):
        if index == len(raw_working_data) - 1:
            current_pair.append(day)
            groups.append(current_pair)
            break

        if day['time'] == current_day['time']:
            current_pair.append(day)
        else:
            groups.append(current_pair)
            current_day = day
            current_pair = [day]

    return groups


def format_working_day_groups(groups: list) -> list:
    result = []

    for group in groups:
        if len(group) == 1:
            result.append(f'{group[0]["day"]} {group[0]["time"]}')
        else:
            first_item = group[0]
            last_item = group[-1]

            result.append(f'{first_item["day"]}-{last_item["day"]} {first_item["time"]}')

    return result