import requests

info_service_url = 'http://localhost:8000'
add_phone_info_url = f'{info_service_url}/add_phone'
get_phones_info_url = f'{info_service_url}/get_phones'
get_phone_info_by_id_url = f'{info_service_url}/get_phone_by_id'
update_phone_info_url = f'{info_service_url}/update_phone'
delete_phone_info_url = f'{info_service_url}/delete_phone'

new_phone_info = {
    "model": "iPhone 13",
    "brand": "Apple",
    "price": 999.99,
    "release_date": "2021-09-24",
    "description": "The latest iPhone with A15 Bionic."
}

new_desc = {
    "model": "iPhone 13",
    "brand": "Apple",
    "price": 999.99,
    "release_date": "2021-09-24",
    "description": "New description"
}


def test_1_add_phone_info():
    res = requests.post(add_phone_info_url, json=new_phone_info)
    assert res.status_code == 200
    assert res.json()['model'] == "iPhone 13"


def test_2_get_phones_info():
    res = requests.get(get_phones_info_url).json()
    assert any(phone['model'] == "iPhone 13" for phone in res)


def test_3_get_phone_info_by_id():
    phones = requests.get(get_phones_info_url).json()
    phone_id = next(phone['id'] for phone in phones if phone['model'] == "iPhone 13")
    res = requests.get(f"{get_phone_info_by_id_url}?phone_id={phone_id}").json()
    assert res['id'] == phone_id
    assert res['model'] == "iPhone 13"


def test_4_update_phone_info():
    phones = requests.get(get_phones_info_url).json()
    phone_id = next(phone['id'] for phone in phones if phone['model'] == "iPhone 13")
    res = requests.put(f"{update_phone_info_url}?phone_id={phone_id}", json=new_desc)
    assert res.status_code == 200


def test_5_delete_phone_info():
    phones = requests.get(get_phones_info_url).json()
    phone_id = next(phone['id'] for phone in phones if phone['model'] == "iPhone 13")
    res = requests.delete(f"{delete_phone_info_url}?phone_id={phone_id}")
    assert res.status_code == 200
    assert res.json() == {"message": "Phone deleted"}

    res_check = requests.get(get_phones_info_url).json()
    assert all(phone['id'] != phone_id for phone in res_check)
