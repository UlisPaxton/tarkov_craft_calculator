
from craft_table import Craft, repeat


# ----------------------- наполнение таблицы крафта
Craft.add('Магазин 6Л31', 'Магазин 6Л31', [*repeat('Магазин 6Л23', 4), 'Липкая лента KEKТЕЙП'], 1, 80)
Craft.add('Моток паракорда', 'Paracord', [*repeat('Спортивная сумка', 5), *repeat('Пучок проводов', 3),
                                          'Барс А-2607 95х18', 'Зажигалка Crickent'], 1, 248)
Craft.add('Ткань рипстоп', 'Ripstop cloth', [*repeat('Жилет дикого', 3)], 2, 35)
Craft.add('Водный фильтр', 'Water filter', [*repeat('Воздушный фильтр для противогаза', 4),
                                            'Ножницы для резки металла', 'Бумага для принтера'], 1, 571)
Craft.add('Канистра Экспедиционная топливная (60/60)', 'Expeditionary fuel tank (60/60)',
          [*repeat('Бензиновая зажигалка Zibbo', 10), *repeat('Зажигалка Crickent', 10)], 1, 59)
Craft.add('Граната "хаттабка" на базе ВОГ-25', 'VOG-25 Khattabka grenade',
          [*repeat('Запал УЗРГМ для гранат', 5), *repeat('40 мм ВОГ-25', 5)], 8, 64)

# -------------------- корректировка цен, при желании можно скорректтировать цены
Craft.browser.cache.update({'Зажигалка Crickent': 12_000})
Craft.browser.cache.update({'Бензиновая зажигалка Zibbo': 18_000})
Craft.browser.cache.update({'Канистра Экспедиционная топливная (60/60)': 320_000})
Craft.browser.cache.update({'Запал УЗРГМ для гранат': 11_000})
Craft.browser.cache.update({'40 мм ВОГ-25': 16_000})
Craft.browser.cache.update({'Граната "хаттабка" на базе ВОГ-25': 22_000})

# -------------------- вызов крафта
Craft.craft('Канистра Экспедиционная топливная (60/60)')
Craft.craft('Граната "хаттабка" на базе ВОГ-25')
Craft.craft('Водный фильтр')

"""for index, value in enumerate(Craft.craft_table):
    print(index, value['name'])
"""




