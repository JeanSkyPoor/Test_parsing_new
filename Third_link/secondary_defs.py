def get_address_and_name(shop):
    address = shop.find('p', class_='name').text.split('(')[0]
    name = shop.find('p', class_='name').text.split('(')[-1].replace(')','')
    if name == address:
        return address, 'No name'
    return address, name


def get_phones(shop) -> str:
    phone = shop.find('p', class_='phone').text.replace('(', '').replace(')', '').replace(' ', '')
    return phone