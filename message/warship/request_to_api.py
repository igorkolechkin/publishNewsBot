import requests

from datetime import datetime
from config import WARSHIP_API_URL
from message.warship.categories import categories


def get_warship_info(time_of_day: str) -> str:
    current_date = datetime.now().date().strftime('%Y.%m.%d')
    answer = f"💀<b>Загальні бойові втрати русакiв станом на {time_of_day} {current_date}</b>💀\n\n"

    try:
        response = requests.get(WARSHIP_API_URL + '/statistics/latest')

        if response.status_code == 200:
            data = response.json()['data']

            for category, value in categories.items():
                increase = data['increase'][category]
                increase_str = f" (+{increase})" if increase != 0 else ""

                answer += f"- {value['title']}: " \
                          f"<b>{data['stats'][category]}{increase_str}</b>\n"
        else:
            print(f"Ошибка запроса. Код: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return answer
