import json
from pathlib import Path
from loader import dinner_sets, logging

path = Path(__file__).parent / 'DinnerDB.json'


def create_db():
    structure = {
        'users': {
            # 'tg_id': [tg_username, tg_name, [dinners_sets]] внутри словаря будет такая конструкция
        },
        'admins_id': []
    }
    with open('DinnerDB.json', 'w', encoding='utf8') as f:
        json.dump(structure, f, indent=4, ensure_ascii=False)


class DBConnect:
    def __init__(self):
        with open(path, 'r', encoding='utf8') as f:
            self.db: dict = json.load(f)

    def __save(self):
        with open(path, 'w', encoding='utf8') as f:
            json.dump(self.db, f, indent=4, ensure_ascii=False)

    def add_admin(self, tg_id: int):
        admins = self.db
        try:
            tg_id = int(tg_id)
            assert not tg_id in admins['admins_id'], logging.warning(f'id {tg_id} уже находиться в списке админов (add_admin)')
            admins['admins_id'].append(tg_id)
            self.__save()
            return True
        except Exception as err:
            logging.warning(f'{err}')
            return False

    def get_admins(self) -> list[int]:
        return self.db['admins_id']

    def remove_admin(self, tg_id: int):
        admins = self.db
        try:
            tg_id = int(tg_id)
            assert tg_id in admins['admins_id'], logging.warning(f'id {tg_id} нет в списке админов (remove_admin)')
            admins['admins_id'].remove(tg_id)
            self.__save()
            return True
        except Exception as err:
            logging.warning(f'{err}')
            return False

    def add_user(self, tg_id, tg_username: str, tg_name: str):
        users = self.db
        try:
            assert not str(tg_id) in users['users'].keys(), logging.warning(f'id {tg_id} уже находиться в списке пользователей (add_user)')
            tg_username = None if tg_username == '-' else tg_username
            users['users'][str(tg_id)] = [tg_username, tg_name, []]
            self.__save()
            return True
        except Exception as err:
            logging.warning(f'{err}')
            return False

    def remove_user(self, tg_id):
        users = self.db
        try:
            assert str(tg_id) in users['users'].keys(), logging.warning(f'id {tg_id} нет в списке пользователей (remove_user)')
            del users['users'][str(tg_id)]
            self.__save()
            return True
        except Exception as err:
            logging.warning(f'{err}')
            return False

    def get_users(self) -> dict[str:list]:
        return self.db['users']

    def set_meal(self, tg_id, meal: str):
        users: dict = self.db
        tg_id = str(tg_id)
        try:
            assert tg_id in users['users'].keys(), logging.warning(f'id {tg_id} meal:{meal} нет в списке пользователей (set_meal)')
            meals_list: list = users['users'][tg_id][-1]
            meals_list.append(meal)
            self.__save()
            return True
        except Exception as err:
            logging.warning(f'{err}')
            return False

    def del_my_meal(self, tg_id):
        users: dict = self.db
        try:
            tg_id = str(tg_id)
            assert tg_id in users['users'].keys(), logging.warning(f'id {tg_id} нет в списке пользователей (del_my_meal)')
            users['users'][tg_id][2] = []
            self.__save()
            return True
        except Exception as err:
            logging.warning(f'{err}')
            return False

    def reset_meals(self):
        users: dict = self.db['users']
        for tg_id, lst in users.items():
            lst[-1] = []
        self.__save()

    def get_usr_meal(self) -> str:
        """ Возвращает строку: имя - все его заказы """
        users = self.db['users'].values()
        result = ''
        try:
            for _, name, lst_meals in users:
                if lst_meals:
                    meals = ''
                    for meal in lst_meals:
                        if (count := lst_meals.count(meal)) > 1 and meal not in meals:
                            meals += f"{meal} x{count}, "
                        elif meal not in meals:
                            meals += meal + ', '
                    result += f"<i><b>{name}</b></i> - [{meals.strip(', ')}]\n"
            return result
        except Exception as err:
            logging.warning(f'{err}')
            return ''

    def get_tools(self) -> int:
        """ Возвращает целочисленное число: количество приборов(кол-во пользователей, сделавших заказ) """
        users = self.db['users'].values()
        total_order = 0
        for *_, lst_meals in users:
            if lst_meals:
                total_order += 1
        return total_order

    def get_order_status(self) -> dict:
        """ Возвращает словарь: блюдо - его количество """
        users = self.db['users'].values()
        dinners_sets_dict = {}
        for key, d_set in dinner_sets().items():
            dinners_sets_dict[d_set] = 0
            for _, _, lst_meals in users:
                if d_set in lst_meals:
                    dinners_sets_dict[d_set] += lst_meals.count(d_set)

        return dinners_sets_dict


def test():
    db = DBConnect()
    # users: dict[str:list] = db.get_users()

    # db.add_admin(32132131)
    # db.add_admin(532325532)
    # db.remove_admin(532325532)
    # db.add_user(430403403, 'username1', 'Имя1')
    # db.add_user(63565334, 'username2', 'Имя2')
    # db.remove_user(430403403)
    # db.set_meal(670076879, '1.1')
    # db.set_meal(670076879, '1.2')
    # db.set_meal(670076879, '1.2')
    # db.del_my_meal(670076879)
    # db.reset_meals()
    print(db.get_usr_meal())


if __name__ == '__main__':
    test()

db = DBConnect()
