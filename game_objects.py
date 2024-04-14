# coding: utf-8
import random as r
from game_func import list_item_load
import game_text as gt


class Locals:
    '''Класс используется для генерации случайной локации'''

    def __init__(self):
        # случайный выбор локации
        self.local_name = r.choice(
            ['Вход на кладбище', 'Старая Часовня', 'Безымянный склеп', 'Могила графа Д.'])

    def print_local(self):
        '''Метод информирует игрока о локации куда он попал'''

        print(f'Вы пришли в район кладбища, где стоит {self.local_name}')
        print()

    def endgame_local(self) -> bool:
        '''Метод проверяет, место окончания игры'''

        if self.local_name == 'Вход на кладбище':
            return True
        return False


class Item:
    '''Класс представляет собой предмет'''

    def __init__(self, type_item: str, name: str,
                 param: int, type_param: str, desc=None):
        self.name: str = name  # Имя предмета
        self.param = int(param)  # Параметр предмета
        self.type_item: str = type_item  # Тип предмета
        self.type_param: str = type_param  # Тип параметра предмета
        self.desc: str = desc  # описание предмета, сделали заранее вдруг захотим добавить


class DictItem:
    ''' Класс представляет собой словарь предметов,
        Данный класс используется для генерации случайного предмета'''

    @staticmethod
    def load_items() -> dict[str:list[Item]]:
        '''Статистический метод для загрузки предметов из словаря'''

        list_items: list = list_item_load()
        result_dict = {}

        for item in list_items:
            # item[0] - этот срез содержит тип
            # предмета(head,hand,body,legs,key)
            result_dict.setdefault(item[0], []).append(Item(*item))
        return result_dict


class GetItem:
    '''Класс используется для гнерации случайного предмета.
    Генерация предмета зависит от имени противника.
    Сторож это босс и он всегда получает ключ от ворот кладбища.
    Остальные противники получают случайный предмет из словаря items.json.
    Класс нужен только для генерации предмета, экземпляры класса не создавать.
    Класс нужен для инициализации экземпляра класса Monster.
    При создании противника у него есть случайный предмет'''

    all_items: dict[str:list[Item]] = DictItem.load_items()

    @classmethod
    def get_item(cls, monster_name: str) -> Item:
        '''Функция используется для возвращения случайного предмета.
        Случайным образом мы генерируем тип предмета, на основании
        типа предмета получаем все предметы данного типа и из них
        случайным образом выбираем один предмет и возвращаем его.'''

        if monster_name == 'Сторож':
            return (Item('key', 'Большой ржавый ключ от ворот кладбища', '1', 'def'))
        else:
            # случайный тип предмета
            type_item: str = r.choice(['hand', 'hand', 'head', 'body', 'leg'])

            # случайный предмет на основе случайного типа предмета
            item: str = r.choice(cls.all_items.get(type_item, None))

            # возвращаем экземпляр предмета
            return item


class Monster(GetItem):
    ''' Класс ипользуется при создании противника.
        Противник имеет атрибуты : имя, здоровье, атаку и предметов.
        Атрибуты определяются статистическими методами.'''

    def __init__(self):
        self.name: str = self.__get_name()
        self.hp: int = self.__get_hp()
        self.attack: int = self.__get_attack()
        self.item: Item = self.get_item(self.name)

    @staticmethod
    def __get_name() -> str:
        '''Метод возвращает случайным образом имя противника'''

        return r.choice(['Вампир', 'Скелет', 'Зомби', 'Сторож'])

    @staticmethod
    def __get_hp() -> int:
        '''Метод возвращает рандомно сгерированное hp в диопазоне от 5 до 7 '''
        return r.randint(3, 6)

    @staticmethod
    def __get_attack() -> int:
        ''' Метод возвращает рандомно сгерированное атаку в диопазоне от 2 до 3 '''

        return r.randint(2, 3)

    def get_monster(self) -> bool:
        '''Метод отвечает случайное событие появление монстра в локации'''

        return True if r.randint(1, 10) <= 5 else False

    def print_monster(self):
        '''Метод информирует игрока о типе встреченного монстра'''

        print(
            f"Вы повстречали на своем пути, {self.name} (hp:{self.hp}, dmg:{self.attack})")
        print()

    def get_attack_monster(self) -> str:
        '''Метод возвращает рандомно сгенерированную часть тела куда бьет монстр'''

        monster_target = ['Голова', 'Грудь', 'Ноги']
        return r.choice(monster_target)

    def get_defence_monster(self) -> str:
        '''Метод возвращает рандомно сгенерированную часть тела которую защищает монстр'''

        monster_defence = ['Голова и ноги', 'Грудь и голова', 'Ноги и грудь']
        return r.choice(monster_defence)


class Player():
    '''Класс ипользуется при создании персонажа игрока.
    Персонаж имеет атрибуты : имя, здоровье, атаку и инвентарь.
    Атрибуты определяются статистическими методами.'''

    default_attack: int = 3
    default_hp: int = 7

    def __init__(self, name='Безымянный'):
        self.hp: int = type(self).default_hp
        self.attack: int = type(self).default_attack
        self.name: str = name
        self.bonus_param = {'hand': 0, 'head': 0, 'body': 0, 'leg': 0}
        self.inventory = {}

    def put_item(self, new_item: Item) -> None:
        '''Метод отвечает за логику добавления предмета в инвентарь'''
        # получаем тип нового предмета это hand/head/body/leg
        new_item_type: str = new_item.type_item

        # получаем тип параметра нового предмета
        new_item_type_param: str = new_item.type_param

        # получаем числовую характеристику предмета
        new_item_param: int = new_item.param

        if new_item_type_param == 'dmg':

            # удаляем бонус текущего предмета, перед тем как одеть новый
            self.attack -= self.bonus_param[new_item_type]

            # добавляем параметры от нового предмета в характеристики игрока
            self.attack += new_item_param

        elif new_item_type_param == 'def':

            # удаляем бонус текущего предмета, перед тем как одеть новый
            # если хп у игрока больше чем давал бонус от предмета,
            # то уменьшаем хп игрока на бонус от предмета
            if self.hp > self.bonus_param[new_item_type]:
                self.hp -= self.bonus_param[new_item_type]

            # добавляем параметры от нового предмета в характеристики игрока
            self.hp += new_item_param

        # после всех изменений добавляем новый предмет в инвентарь
        self.inventory[new_item_type] = new_item

        # так же добавляем бонус от нового предмета в словарь бонусов
        self.bonus_param[new_item_type] += new_item_param

    @staticmethod
    def check_input(func) -> callable:
        '''Декоратор, проверяющий ввод пользователя на корректность'''

        def wrapper(self):
            flag = True
            if func.__name__ == 'get_attack_player':
                print('Куда бьем? 1 - Голова, 2 - Грудь, 3 - Ноги')
                print()
            elif func.__name__ == 'get_defence_player':
                print(
                    'Что защищаем? 1 - Голова и ноги, 2 - Грудь и голова, 3 - Ноги и грудь')
                print()

            while flag:
                try:
                    keyboard_input = int(input('Введите число от 1 до 3: '))
                    print()
                    if keyboard_input in range(1, 4):
                        flag = False
                        return func(self, keyboard_input)
                    else:
                        print('Введено неверное значение, повторите попытку....')
                        print()
                except Exception:
                    print("Ошибка: введена не цифра.")
                    print()
        return wrapper

    @check_input
    def get_attack_player(self, keyboard_input: int = None) -> str:
        '''Метод возвращает часть тела, которую игрок выбрал для нанесение удара '''

        # словарь с частями тела для удара
        target_dict = {1: 'Голова', 2: 'Грудь', 3: 'Ноги'}

        # возврат части тела для удара
        if keyboard_input in target_dict:
            return target_dict.get(keyboard_input)
        else:
            raise ValueError(
                'Введеное значение отсутствует в словаре target_dict')

    @check_input
    # Если будет None, то raise ValueError
    def get_defence_player(self, keyboard_input: int = None) -> str:
        '''Метод возращает часть тела,которую игрок выбрал для защиты '''

        # словарь с частями тела для защиты
        defence_dict = {
            1: 'Голова и ноги',
            2: 'Грудь и голова',
            3: 'Ноги и грудь'}

        # возврат части тела для защиты
        if keyboard_input in defence_dict:
            return defence_dict.get(keyboard_input)
        else:
            raise ValueError(
                'Введеное значение отсутствует в словаре defence_dict')

# Компонентный класс


class TakeItem:

    def __init__(self, player: Player, monster: Monster):
        self.player = player
        self.monster = monster

    @staticmethod
    def check_input(func):
        '''Декоратор, проверяющий ввод пользователя на корректность'''

        def wrapper(self):
            flag: bool = True
            print(f'Из монстра выпадает предмет {self.monster.item.name}')
            print('Хотите использовать этот предмет? 1 - Да, 2 - Нет, ')
            print()
            while flag:
                try:
                    keyboard_input = int(input('Введите число от 1 до 2: '))
                    if keyboard_input in range(1, 3):
                        flag = False
                        return func(self, keyboard_input)
                    else:
                        print('Введено неверное значение, повторите попытку....')
                        print()
                except Exception:
                    print("Ошибка: введена не цифра.")
                    print()
        return wrapper

    @check_input
    def take_item(self, keyboard_input: int) -> None:
        '''Метод для передачи предмета от монстра к игроку'''

        if keyboard_input == 1:
            # определяем тип предмета, что бы его положить в нужное место в
            # инвентаре игрока
            monster_item = self.monster.item
            if monster_item.type_item == 'key':
                print(gt.key_info)
                print()
                self.player.inventory[monster_item.type_item] = monster_item
            else:
                if monster_item.type_param == 'def':
                    print(f'Вы получили +{monster_item.param} к защите')
                elif monster_item.type_param == 'dmg':
                    print(f'Вы получили +{monster_item.param} к атаке')

                # получаем предмет и его параметры
                self.player.put_item(monster_item)
                print('Вы надели предмет')
                print()
        else:
            print('Выпрошли мимо и предмет пропал во мраке ночи')


class Fight:
    '''Класс для управление логикой между игроком и противником.'''

    def __init__(self, player: Player, monster: Monster):
        self.player = player
        self.monster = monster

    def check_result(self, attak: str, defence: str):
        '''Метод определения успешности атаки и защиты игрока или монстра'''

        # если атака попала в защиту то, удар заблокирован
        if attak.lower() in defence.lower():
            return False  # удар заблокирован
        return True  # успешный удар

    def fight(self):
        """ Метод для управления логикой боя между игроком и монстром """

        flag: bool = True
        while flag:
            # выбор атаки для игрока
            target_attak_player: str = self.player.get_attack_player()

            # выбор защиты для игрока
            target_defence_player: str = self.player.get_defence_player()

            # расчет атаки для монстра
            target_attak_monster: str = self.monster.get_attack_monster()

            # расчет защиты для монстра
            target_defence_monster: str = self.monster.get_defence_monster()

            if self.monster.hp > 0:
                # проверка успешности атаки игрока
                if self.check_result(target_attak_player,
                                     target_defence_monster):
                    # уменьшение здоровья монстра
                    self.monster.hp -= self.player.attack
                    print(
                        f'Вы нанесли мощный удар {self.monster.name} в {target_attak_player}')
                    print(
                        f'У монстра осталось {max(0,self.monster.hp)} здоровья')
                    print()
                else:  # если игрок промахнулся
                    print(
                        f'Промах, монстр угадал вашу атаку и защитил {target_defence_monster}')
                    print()
                if self.monster.hp <= 0:
                    print(f'Монстер {self.monster.name} побежден!')
                    print()
                    TakeItem(self.player, self.monster).take_item()
                    flag = False  # если у монстра кончились хп, то останавливаем бой
                elif self.player.hp > 0:
                    # проверка успешности атаки монстра
                    if self.check_result(
                            target_attak_monster, target_defence_player):
                        # уменьшение здоровья игрока
                        self.player.hp -= self.monster.attack
                        print(
                            f'Монстр нанес вам удар в {target_attak_monster}')
                        print(
                            f'У вас осталось {max(0,self.player.hp)} здоровья')
                        print()
                        if self.player.hp <= 0:
                            print('Игрок погиб')
                            print()
                            input('Игра окончена, нажмите Enter...')
                            print()
                            flag = False
                            break
                    else:  # если монстр промахнулся то выводим сообщение
                        print(
                            f'Монстр промахнулся ударив в {target_attak_monster}')
                        print()
            else:  # если  self.monster.hp <=0
                print(f'Монстер {self.monster.name} побежден!')
                input('Для продолжения путеществия нажмите Enter...')
                break


class GameEngine:
    '''Класс для управления потоком игры'''

    flag = True
    player = Player()

    @classmethod
    def start(cls):
        '''Метод для запуска игры.
           Печать приветсвтенных сообщений.
           Запуск основного процесса игры.'''

        print(gt.welcome_text)
        print()
        print(gt.game_rule)
        print()
        cls.main_process()

    @classmethod
    def main_process(cls):
        '''Метод управления основным игровым процессом'''
        while cls.flag:
            # генерируем случайную локацию
            local = Locals()
            local.print_local()

            # генерируем случайного монстра
            monster = Monster()
            print('------------------Инвентарь-------------------------')
            print('Инвентарь: ', '/' .join(
                [f'{object_item.name}+{object_item.param}' for object_item in cls.player.inventory.values() if 'ключ' not in object_item.name]))
            print(
                'Характеристики игрока:',
                f'Жизни: {cls.player.hp}, Атака: {cls.player.attack}')
            print(
                'Ключ от кладбища: ',
                'Да' if cls.player.inventory.get('key') else 'Нет')
            print('------------------Инвентарь-------------------------')
            print()

            # если монстр сгенерировался, то начинаем драку
            if monster.get_monster():
                monster.print_monster()

                # начало боя с монстром
                Fight(cls.player, monster).fight()
            else:
                print('Шаг за шагом, вы прокладываете свой путь во мрак кладбищенской ночи, удача на вашей стороне, сейчас вокруг никого нет')
                print()
                input('Нажмите Enter....')
                print()
            cls.flag = cls.end(local)  # Проверка на конец игры
            if cls.flag:
                cls.flag = False if cls.player.hp <= 0 else True

        if cls.player.hp <= 0:
            print(gt.end_lose)
            print()
        else:
            print(gt.end_win)
            print()

    @classmethod
    def end(cls, local: Locals) -> bool:
        ''' Метод отвечает за окончание игры.
            Если у игрока есть ключ от кладбища и он находится у ворот,
            то запускает предложение окончить игру.
            False - игра закачнивается
            True - игра продолжается'''

        if local.endgame_local() and cls.player.inventory.get('key', False):
            print(
                'У Вас есть Большой ржавый ключ от ворот кладбища, хотите сбежать с кладбища?')
            print()
            d_answer_player = int(input('Введите 1 - Да, 2 - Нет: '))
            print()
            if d_answer_player == 1:
                print('Вы сбежали с кладбища')
                print()
                return False
            else:
                print('Вы остались в кладбище и решили продолжить игру')
                print()
                return True
        else:
            return True
