from sys import exit
from craft_table import Craft, repeat


# ----------------------- наполнение таблицы крафта
Craft.add('Водный фильтр', 'Water filter', [*repeat('Воздушный фильтр для противогаза', 4),
                                            'Ножницы для резки металла', 'Бумага для принтера'], 1, 571)
Craft.add('Бронежилет модуль 3М', 'Module-3M bodyarmor (40/40)', [*repeat('Арамидная ткань', 2),
                                                                  *repeat('Ткань рипстоп', 2)], 1, 52)
Craft.add('Кейс для Хлама', 'Lucky Scav Junkbox', [*repeat('Кейс для магазинов', 3), *repeat('Болты', 6),
                                                   *repeat('Липкая лента KEKТЕЙП', 3),
                                                   'Ножницы для резки мателла'], 1, 657)
Craft.add('Канистра Экспедиционная топливная (60/60)', 'Expeditionary fuel tank (60/60)',
          [*repeat('Бензиновая зажигалка Zibbo', 10), *repeat('Зажигалка Crickent', 10)], 1, 59)
Craft.add('Рулон туалетной бумаги', 'Toilet paper', [*repeat('Бумага для принтера', 2)], 2, 25)
Craft.add('Отбеливатель', 'Ox bleach', ['Кусок мыла', 'Средство для промывки теплообменных поверхностей',
                                        'Пачка соды'], 5, 37)
Craft.add('Воздушный фильтр для противогаза', 'Air filter for gas mask', ['Противогаз ГП-5'], 1, 1)
Craft.add('Арамидная ткань', 'Aramid fiber cloth', ['Бронежилет PACA Soft Armor'], 2, 32)
Craft.add('Алюминиевая шина для переломов', 'Immobilizing splint (alu)', ['Бронежилет MF-UNTAR (0/45)',
                                                                          'Ножницы для резки металла'], 2, 51)
Craft.add('Ткань рипстоп', 'Ripstop cloth', [*repeat('Жилет дикого', 3)], 2, 35)
Craft.add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)

Craft.add('Разгрузочный жилет BlackRock chest rig', 'BlackRock chest rig',
          ['Разгрузочный жилет Сплав Тарзан М22', 'Ткань рипстоп', 'Полиамидная ткань Кордура'], 1, 57)
Craft.add('Кейс для гранат', 'Grenade case', [*repeat('Канистра Металлическая топливная (0/100)', 2),
                                              *repeat('Гайки', 5),
                                              *repeat('Болты', 5),
                                              'Ножницы для резки металла', 'Гаечный ключ'], 1, 962)
Craft.add('Бронежилет PACA Soft Armor', 'PACA Soft Armor (50/50)', [*repeat('Арамидная ткань', 3),
                                                                    *repeat('Ткань рипстоп', 2)], 1, 70)
Craft.add('Бутылка шампуня Schaman', 'Schaman shampoo', ['Кусок мыла', 'Бутылка воды 0.6 л'], 2, 33)
Craft.add('Рюкзак Дикого', 'Scav Backpack', ['Флисовая ткань', 'Ткань рипстоп'], 2, 52)
Craft.add('WD-40 100мл', 'WD-40 100ml.', ['WD-40 400мл', 'Ножницы для резки металла'], 2, 144)
Craft.add('Бинт нестерильный', 'Aseptic bandage', ['Флисовая ткань'], 6, 30)
Craft.add('Моток паракорда', 'Paracord', [*repeat('Спортивная сумка', 5), *repeat('Пучок проводов', 3),
                                          'Барс А-2607 95х18', 'Зажигалка Crickent'], 1, 248)
Craft.add('Разгрузочный жилет Сплав Тарзан М22', 'Splav Tarzan M22 Rig', ['Полиамидная ткань Кордура',
                                                                          'Ткань рипстоп'], 1, 44)
Craft.add('Липкая лента KEKТЕЙП', 'KEKTAPE duct tape', [*repeat('Монтажный скотч', 2), *repeat('Изолента', 2),
                                                        'Стеклоочиститель'], 1, 77)
Craft.add('Гофрированный шланг', 'Corrugated hose', [*repeat('Пучок проводов', 3), *repeat('Изолента', 3),
                                                     'Силиконовая трубка'], 2, 194)

Craft.add('Граната "хаттабка" на базе ВОГ-25', 'VOG-25 Khattabka grenade',
          [*repeat('Запал УЗРГМ для гранат', 5), *repeat('40 мм ВОГ-25', 5)], 8, 64)

"""
 при желании можно скорректтировать цены и провести рассчёты исходя из указанных цен
 
Craft.browser.cache.update({'Зажигалка Crickent': 12_000})
Craft.browser.cache.update({'Бензиновая зажигалка Zibbo': 18_000})
Craft.browser.cache.update({'Канистра Экспедиционная топливная (60/60)': 320_000})
Craft.browser.cache.update({'Запал УЗРГМ для гранат': 11_000})
Craft.browser.cache.update({'40 мм ВОГ-25': 16_000})
Craft.browser.cache.update({'Граната "хаттабка" на базе ВОГ-25': 22_000})
"""
""" Пример вызова крафта
# Craft.craft('Канистра Экспедиционная топливная (60/60)')
# Craft.craft('Граната "хаттабка" на базе ВОГ-25')
# Craft.craft('Водный фильтр')

"""

while True:
    for count, item in enumerate(Craft.craft_table):
        print(count, item['name'])
    try:
        item_number_to_craft = int(input('Выберите номер предмета для рассчёта:> '))
        item_to_craft = Craft.craft_table[item_number_to_craft]
        Craft.craft(item_to_craft['name'])
    except IndexError:
        print('Такого номера в списке нет.')
    except ValueError:
        print('Числовой номер, пожалуйста.')

    if input("Ещё?(Y/N)").upper() == 'N':
        exit()



