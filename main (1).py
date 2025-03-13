from Connection_DB_c import make_connection_to_sakila, make_connection_insert_ich, make_close
from Helpers_c import *
import mysql.connector

def main():
    print('Welcome to our App')
    make_your_choice()
    
flag=True

def make_your_choice():
    while flag:  # Бесконечный цикл для возврата к выбору после выполнения
        choice = input("""\nHow do you want to choose a film:
       
        by genre/genre-year - put:            1
        by keyword - put:                     2
        by year or range of years:            3
        by actor - put:                       4
        by TOP request - put:                 5
        Finish Search - put:                  9
        Start your choice """)
        
        if choice == '1':
            films = get_film_by_genre_year()
            continue_search()
        elif choice == '2':
            films = search_by_keyword()
            continue_search()
        elif choice == '3':
            films = get_films_by_years()
            continue_search()
        elif choice == '4':
            films = set_film_by_actor()
            continue_search()
        elif choice == '5':
            films = execute_top_request()
            continue_search()
        elif choice == '9':
            print('Happy End')
            break  # Выход из цикла и завершение программы
        else:
            print("We can't find that option. Please, try again.")

def continue_search():
    global flag
    choice = input('''\nDo you want to continue searching?
                    If yes - put Y
                    if not just press N: ''')  
    if choice.upper() == 'Y':  # Если пользователь ввел Y (в любом регистре), продолжаем поиск
        flag=True  # Возвращаемся к выбору фильмов
    else:
        print("Happy End")
        flag=False

if __name__ == "__main__":
    main()