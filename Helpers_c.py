from Connection_DB_c import make_connection_to_sakila, make_connection_insert_ich, make_close
from tabulate import tabulate
from colorama import Fore, Style, init
init()

#__________________Блок выборки по жанру________________________________
#%%
unique_genre = """
SELECT
    DISTINCT name
FROM category
"""
#%%
query_by_genre_year = """
    Select f.title, f.release_year, c.name
    from film f
    inner join film_category fc on f.film_id = fc.film_id
    inner join category c on fc.category_id = c.category_id
    where c.name = %s and f.release_year = %s
    limit 20
"""

#%%
query_by_genres_of_years = """
    Select f.title, f.release_year, c.name
    from film f
    inner join film_category fc on f.film_id = fc.film_id
    inner join category c on fc.category_id = c.category_id
    where c.name = %s and f.release_year between %s and %s
    order by f.release_year
    limit 20
"""
#%%
query_by_genre = """
    Select f.title, f.release_year, c.name
    from film f
    inner join film_category fc on f.film_id = fc.film_id
    inner join category c on fc.category_id = c.category_id
    where c.name = %s
    limit 20
"""
#%%
def get_genre():  # выбрать жанр из списка
    connection, cursor = make_connection_to_sakila()
    cursor.execute(unique_genre)
    genres = cursor.fetchall()
    make_close(connection, cursor) 
    headers = ['Genre from the list']
    print(tabulate(genres,
            headers=headers,
            tablefmt='pretty',
            colalign=('center',)))


#%%
def select_year_to_genre():
    start_year = input('If you want to search film also by year, input the year and press enter: ').strip()
    if start_year == '':
        return None, None
    else:
        finish_year = input('If you want to search in a range of years, input the ending year and press enter: ').strip()
        if finish_year == '':
            return int(start_year), None
        else:
            return int(start_year), int(finish_year)

#%%
def get_user_genre():
    genre = input('Input the genre, which you want to watch: ').strip().capitalize()
    return genre

def get_query_genre_year(genre, start_year=None, finish_year=None):
    if start_year:
        if finish_year:
            query = query_by_genres_of_years
            request_id = 'GY'
            return query, (genre, start_year, finish_year), request_id
        else:
            query = query_by_genre_year
            request_id = 'GY'
            return query, (genre, start_year), request_id
    else:
        query = query_by_genre
        request_id = 'G'
        return query, (genre,), request_id
#%%
def get_film_by_genre_year():
    get_genre()
    genre = get_user_genre()
    start_year, finish_year = select_year_to_genre()
    query, parameters, request_id = get_query_genre_year(genre, start_year, finish_year)
    films = do_query(query, parameters)
    # Формируем текст запроса для вставки в журнал запросов
    request_text = ', '.join(map(str, parameters))
    insert_film_request(request_id, request_text)  
    if films:
        headers = ['Title','Release_year','Name']
        print(tabulate(films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center','center')))

#%%
#_________________________________Блок выборки по актеру_____________________________
def get_actors_list(): 
    # SQL-запрос для получения списка актёров
    query_get_actors_list = 'select first_name, last_name from actor limit 30'
    
    # Устанавливаем соединение с базой данных
    connection, cursor = make_connection_to_sakila()
    
    # Выполняем запрос и получаем список актёров
    cursor.execute(query_get_actors_list)
    actors = cursor.fetchall()
    
    # Заголовки для вывода
    headers = ['First_name', 'Last_name']
    
    # Выводим данные в табличной форме с помощью tabulate
    print(tabulate(actors,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center')))
    
    # Закрываем соединение
    make_close(connection, cursor)

#%%
def get_actor_name_from_user(): # запрос имени актера от пользователя
    actor_first_name = (input('Input actor\'s first name: ')).strip().upper()
    actor_last_name = (input('Input actor\'s last name: ')).strip().upper()
    return actor_first_name, actor_last_name
#%%
def get_film_by_actor(actor_first_name, actor_last_name): # функция, которая дает выбор фильма по имени актера
    query_by_actor = """select a.first_name, a.last_name, f.title from actor a
                        inner join film_actor fa
                        on a.actor_id = fa.actor_id
                        inner join film f
                        on fa.film_id = f.film_id
                        where a.first_name = %s and a.last_name = %s limit 10"""
                    
    connection, cursor = make_connection_to_sakila()
    cursor.execute(query_by_actor, (actor_first_name, actor_last_name))
    film_by_actor_choice = cursor.fetchall()
    make_close(connection, cursor)
    return film_by_actor_choice

 #%%   

def set_film_by_actor():
    get_actors_list()
    actor_first_name, actor_last_name = get_actor_name_from_user()
    films = get_film_by_actor(actor_first_name, actor_last_name)
    if films:
        request_id = 'A'
        request_text = ', '.join([actor_first_name, actor_last_name])
        insert_film_request(request_id, request_text)
        headers = ['First_name','Last_name','Title']
        print(tabulate(films,
        headers=headers,
        tablefmt='pretty',
        colalign=('center','center', 'center')))
    else:
        print('No movies found with this actor')

#____________________________________Блок выборки по ключевому слову________________________________________   

def get_keyword():
    keyword =(input('Input keyword: ')).strip()
    return keyword
#%%
def search_by_keyword():
    keyword = get_keyword()
    connection, cursor = make_connection_to_sakila()
    query = '''
    select title, description
    from film
    where title like %s or description like %s 
    limit 20'''
    keyword = f'%{keyword}%'      
    cursor.execute(query, (keyword, keyword))
    films = cursor.fetchall()
    request_id = 'KW'
    request_text = keyword
    insert_film_request(request_id, request_text)
    make_close(connection, cursor)
    if films:
        colored_films = []
        
        for title, description in films:
            # Replace keyword in title and description with colored version
            plain_keyword = keyword.strip('%').upper()  # Prepare the plain keyword for comparison
            colored_title = title.replace(plain_keyword, f"{Fore.GREEN}{plain_keyword}{Style.RESET_ALL}")
            colored_description = description.replace(keyword.strip('%'), f"{Fore.GREEN}{keyword.strip('%')}{Style.RESET_ALL}")
            colored_films.append((colored_title, colored_description))
        headers = ['Title', 'Description']
        print(tabulate(colored_films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center')))
    else:
        print('Films not found')
    
#________________________________________________________________________________________________________________

#%%
def do_query(query, parameters):
    connection, cursor = make_connection_to_sakila()
    cursor.execute(query, parameters)
    result = cursor.fetchall()
    make_close(connection, cursor)
    return result
#________________________________________Блок выборки по году_____________________________________________________

#%%
def get_user_year():
    start_year = int(input('Please, input the year of the movie\'s release: ').strip())
    
    finish_year = input('If you want to search in a range of years, put the ending year and press enter: ').strip()
    
    return start_year, int(finish_year) if finish_year else None

#%%
def get_query_by_years(start_year, finish_year = None):
    if finish_year:
        query = """
        select title, release_year
        from film 
        where release_year between %s and %s
        order by release_year
        """
        return query, (start_year, finish_year)
    else:
        query = """
        select title, release_year
        from film 
        where release_year = %s
        """
        return query, (start_year,)

#%%
def get_films_by_years():
    start_year, finish_year = get_user_year() 
    query, parameters = get_query_by_years(start_year, finish_year)
    films = do_query(query, parameters)
    request_text = str(parameters)
    if finish_year:
        request_id = 'Y-Y'
    else:
        request_id = 'Y'
    if films:
        insert_film_request(request_id, request_text)
        headers = ['Title','Release_year']
        print(tabulate(films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center')))
    
       
#_________________________________________Блок на запись результатов запросов_______________________________________________________________________

#%%
def insert_film_request(request_id, request_text):   #функция на запись
    
    if request_id == 'G':
        query_description = 'genre'
    elif request_id == 'A':
        query_description = 'actor'
    elif request_id == 'GY':
        query_description = 'genre, year'
    elif request_id == 'Y':
        query_description = 'year'
    elif request_id == 'Y-Y':
        query_description = 'range year'
    elif request_id == 'KW':
        query_description = 'keyword'
    elif request_id == 'TR':
        query_description = 'top request'
  
    
    insert_query = """
    insert into film_searching (request_id, query_description, request_text)
    values (%s, %s, %s)
    """
    
    connection, cursor = make_connection_insert_ich()
    
    try:
        cursor.execute(insert_query, (request_id, query_description, request_text))
        connection.commit()
        
    except Exception:
        connection.rollback()  
    finally:
        make_close(connection, cursor)

#__________________________________________Блок выборки по ТОПам______________________________________________________________________

#%%
def get_top_request():
    request_get_top = '''select request_id, request_text, count(*) as cnt_queries
                    from film_searching
                    group by request_id, request_text
                    order by cnt_queries desc
                    limit 1'''

    connection, cursor = make_connection_insert_ich()
    cursor.execute(request_get_top)
    top_request = cursor.fetchall() 
    make_close(connection, cursor)
    return top_request



#%%
def search_by_actor_for_top(): # как строится запрос, если человек выбрал топ запросов по актеру
    actor_first_name, actor_last_name = top_request[0][1].split(', ')
    films = get_film_by_actor(actor_first_name, actor_last_name)      
    headers = ['First_name','Last_name','Title']
    print(tabulate(films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center', 'center')))



#%%
def select_by_genre_for_top():
    top_request=get_top_request()
    request_text = top_request[0][1]
    info = top_request[0][1].split(', ')
    genre = info[0]
    query_by_genre = """
    Select f.title, f.release_year, c.name
    from film f
    inner join film_category fc on f.film_id = fc.film_id
    inner join category c on fc.category_id = c.category_id
    where c.name = %s
    limit 20 """
    connection, cursor = make_connection_to_sakila()
    cursor.execute(query_by_genre, (genre,))
    result = cursor.fetchall()
    make_close(connection, cursor)
    if result:
        headers = ['Title','Release_year','Name']
        print(tabulate(result,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center','center')))
    else:
        print('Films not found')


#%%
def select_film_by_year_for_top():
    # Получаем запрос для топа фильмов
    top_request = get_top_request()  
    
    # Извлекаем начальный год
    info = top_request[0][1].split(', ')
    start_year = info[0]
       
    try:
        # Пробуем извлечь конечный год, если он указан
        finish_year = top_request[1][1]
    except IndexError:
        # Если конечный год не указан, задаем значение None
        finish_year = None

    # Формируем запрос для поиска фильмов по годам
    query, parameters = get_query_by_years(start_year, finish_year)
    
    # Выполняем запрос и получаем список фильмов
    films = do_query(query, parameters)
    if films:
        headers = ['Title','Release_year']
        print(tabulate(films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center')))

#%%
def search_by_keyword_for_top():
    top_request = get_top_request()
    keyword = top_request[0][1] 
    connection, cursor = make_connection_to_sakila()
    query = '''
    select title, description
    from film
    where title like %s or description like %s 
    limit 20'''
    keyword = f'%{keyword.strip("%")}%'
    cursor.execute(query, (keyword, keyword))
    films = cursor.fetchall()
    make_close(connection, cursor)
    if films:
        colored_films = []
        
        for title, description in films:
            # Replace keyword in title and description with colored version
            plain_keyword = keyword.strip('%').upper()  # Prepare the plain keyword for comparison
            colored_title = title.replace(plain_keyword, f"{Fore.GREEN}{plain_keyword}{Style.RESET_ALL}")
            colored_description = description.replace(keyword.strip('%'), f"{Fore.GREEN}{keyword.strip('%')}{Style.RESET_ALL}")
            colored_films.append((colored_title, colored_description))
        headers = ['Title', 'Description']
        print(tabulate(colored_films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center')))
    else:
        print('Films not found')
#%%
def select_film_by_genre_year_for_top():
    top_request = get_top_request()
    request_text = top_request[0][1]
    info = request_text = top_request[0][1].split(', ')
    start_year = info[1]
    genre = info[0]
    try:
        finish_year = info[2]
    except IndexError:
        finish_year = None
    query, parameters, request_id = get_query_genre_year(genre, start_year, finish_year)
    films = execute_query(query, parameters)
    request_text = ', '.join(parameters)
    if films:
        headers = ['Title','Release_year','Name']
        print(tabulate(films,
            headers=headers,
            tablefmt='pretty',
            colalign=('center','center','center')))
    else:
        print('Films not found')



#%%

def execute_top_request():
    top_request = get_top_request()
    request_id = top_request[0][0]
    request_text = top_request[0][1]
    
    if request_id == 'G':
        film_set = select_by_genre_for_top()
    elif request_id == 'A':
        #actor_first_name, actor_last_name = request_text.split(', ')
        film_set = search_by_actor_for_top()    
    elif request_id == 'GY':
        film_set = select_film_by_genre_year_for_top()
    elif request_id in ['Y', 'Y-Y']:
        film_set = select_film_by_year_for_top()
    elif request_id == 'KW':
        film_set = search_by_keyword_for_top()
    return  film_set

