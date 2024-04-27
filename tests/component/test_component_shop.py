import requests

# URL для сервиса магазина телефонов
phone_store_url = 'http://localhost:8001'
add_phone_url = f'{phone_store_url}/add_phone'
sell_phone_url = f'{phone_store_url}/sell_phone'
get_phones_url = f'{phone_store_url}/phones'
delete_phone_url = f'{phone_store_url}/delete_phone'

# Тестовые данные для телефона
new_phone = {
    "id": 99,
    "name": "iPhone 13",
    "quantity": 10
}

def test_1_add_phone():
    res = requests.post(add_phone_url, json=new_phone)
    assert res.status_code == 200

def test_2_get_phones():
    res = requests.get(get_phones_url).json()
    assert any(phone['name'] == "iPhone 13" and phone['quantity'] == 10 for phone in res)

def test_3_sell_phone():
    # Получаем ID добавленного телефона
    phones = requests.get(get_phones_url).json()
    phone_id = next(phone['id'] for phone in phones if phone['name'] == "iPhone 13")
    res = requests.post(f"{sell_phone_url}?id={phone_id}")
    assert res.status_code == 200
    updated_phone = requests.get(f"{get_phones_url}").json()
    assert any(phone['id'] == phone_id and phone['quantity'] == 9 for phone in updated_phone)

def test_4_delete_phone():
    # Получаем ID добавленного телефона
    phones = requests.get(get_phones_url).json()
    phone_id = next(phone['id'] for phone in phones if phone['name'] == "iPhone 13")
    res = requests.delete(f"{delete_phone_url}?id={phone_id}")
    assert res.status_code == 200
    # Проверяем, что телефон удален
    res_check = requests.get(get_phones_url).json()
    assert all(phone['id'] != phone_id for phone in res_check)
