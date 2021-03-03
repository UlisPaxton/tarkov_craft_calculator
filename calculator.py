from sys import exit
from craft_table import Craft


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



