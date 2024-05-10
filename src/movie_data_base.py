import flet as ft
from  sqlite3 import connect, Error
import ctypes
import logging
import os


if os.path.exists("movie_data_base_log.log"):
    logging.basicConfig(level=logging.ERROR, filename="movie_data_base_log.log",filemode="a", format="%(asctime)s %(levelname)s %(message)s")

else:
    logging.basicConfig(level=logging.ERROR, filename="movie_data_base_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
#Создание БД таблицы и колонок в ней
def sqlite_create_db():


    try:
        with connect('media.db') as db:
            cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS film (
               id INTEGER PRIMARY KEY,
               name TEXT,
               date TEXT,
               genre TEXT,
               director TEXT,
               actors TEXT,
               state TEXT
               )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS anime (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   date TEXT,
                   genre TEXT,
                   director TEXT,
                   state TEXT

                   )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS cartoon (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   date TEXT,
                   genre TEXT,
                   state TEXT
                   )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS series (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   date TEXT,
                   genre TEXT,
                   actors TEXT,
                   state TEXT
                   )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS  cartoonseries(
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   date TEXT,
                   state TEXT
                   )''')
    except Error as er:
        logging.exception(er, exc_info=True)
        ctypes.windll.user32.MessageBoxW(0, str(er), "Ошибка создания БД", 0x40) # вызов предупреждающего окна с ошибкой средствами Windows



    db.commit()




# функция создания главного окна с наследием всех свойств класса Page фреймворка Flet
def main(page: ft.Page):
    page.title = "Multimedia Data Base" # наименование окна программы

    page.scroll = True                  # разрешения вертикальной прокрутки  в основном окне
    page.window_resizable = False       # запрет расстягивания основного окна по ширине и высоте






    def clear_text_fields():
        movie_name.value = ""
        release_date.value = ""
        genre.value = ""
        director.value = ""
        aktors.value = ""
        state.value = ""
        id_number.value = ""
        page.update()

    #функция закрытия предупреждающего баннера вывода ошибок
    def close_banner(e):
        page.banner.open = False
        page.update()

    # баннер ошибок
    def alert_banner(message):
        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(message),
            actions=[ft.TextButton("Закрыть", on_click=close_banner), ])
        page.banner.open = True
        page.update()





    #добавление данные в БД
    def add_value(e):
        lv.controls.clear()
        page.update()
        try:
            with connect('media.db') as db:
                cur = db.cursor()
            if chekbox_film.value == True:


                cur.execute(f'INSERT INTO film VALUES(NULL,"{movie_name.value}","{release_date.value}","{genre.value}","{director.value}","{aktors.value}","{state.value}")')


            elif chekbox_series.value == True:

                cur.execute(f'INSERT INTO series VALUES(NULL,"{movie_name.value}","{release_date.value}","{genre.value}","{aktors.value}","{state.value}")')


            elif chekbox_anime.value == True:

                cur.execute(f'INSERT INTO anime VALUES(NULL,"{movie_name.value}","{release_date.value}","{genre.value}","{director.value}","{state.value}")')


            elif chekbox_mult.value == True:

                cur.execute(f'INSERT INTO cartoon VALUES(NULL,"{movie_name.value}","{release_date.value}","{genre.value}","{state.value}")')


            elif chekbox_mult_series.value == True:

                cur.execute(f'INSERT INTO cartoonseries VALUES(NULL,"{movie_name.value}","{release_date.value}","{state.value}")')


        except Error as er:
            logging.exception(er, exc_info=True)
            alert_banner(er)


        db.commit()


        clear_text_fields()

        page.snack_bar.open = True

        add_data_button.disabled = True

        page.update()

    #функция получения всех записей из таблицы
    def sqlite_get_all_data(name_table):
        lst = []
        lv.controls.clear()
        page.update()
        #page.add(lv)
        try:
            with connect('media.db') as db:
                cur = db.cursor()

            cur.execute(
                f'SELECT * FROM {name_table}')

        except Error as er:
            logging.exception(er, exc_info=True)
            alert_banner(er)


        rows = cur.fetchall()

        if  chekbox_series.value == True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_name.value = row[1]
                text_data.value = row[2]
                text_genre.value = row[3]

                text_actors.value = row[4]
                text_state.value = row[5]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}       {text_actors.value}   {text_state.value}"))

                page.update()

        elif chekbox_anime.value == True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_name.value = row[1]
                text_data.value = row[2]
                text_genre.value = row[3]
                text_director.value = row[4]

                text_state.value = row[5]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}     {text_director.value}     {text_state.value}"))

                page.update()

        elif chekbox_mult.value ==True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_name.value = row[1]
                text_data.value = row[2]
                text_genre.value = row[3]

                text_state.value = row[4]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}   {text_state.value}"))

                page.update()


        elif chekbox_mult_series.value == True:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_name.value = row[1]
                text_data.value = row[2]

                text_state.value = row[3]

                lv.controls.append(ft.Text(
                    f"{text_id.value}   {text_name.value}   {text_data.value}   {text_state.value}"))

                page.update()

        else:
            for row in rows:
                lst.append(row)
                text_id.value = row[0]
                text_name.value = row[1]
                text_data.value = row[2]
                text_genre.value = row[3]
                text_director.value = row[4]
                text_actors.value = row[5]
                text_state.value = row[6]


                lv.controls.append(ft.Text(
                            f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}    {text_director.value}   {text_actors.value}   {text_state.value}"))

                page.update()


        clear_text_fields()

        page.update()

    #корневая функция получения данных из БД по одному из параметров запроса
    def sql_test(name_table,name_column,value_column):
        lst = []
        try:
            with connect('media.db') as db:
                cur = db.cursor()

            cur.execute(
                f'SELECT * FROM {name_table}  WHERE  {name_column} LIKE "%{value_column}%"')
        except Error as er:
            logging.exception(er, exc_info=True)
            alert_banner(er)



        rows = cur.fetchall()


        if rows == [] :

            page.snack_bar = ft.SnackBar(content=ft.Text("По данному запросу ничего не найдено"), open=False)
            page.snack_bar.open = True
            clear_text_fields()

            page.update()


        else:
            if chekbox_series.value == True:
                for row in rows:
                    lst.append(row)
                    text_id.value = row[0]
                    text_name.value = row[1]
                    text_data.value = row[2]
                    text_genre.value = row[3]

                    text_actors.value = row[4]
                    text_state.value = row[5]

                    lv.controls.append(ft.Text(
                        f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}       {text_actors.value}   {text_state.value}"))

                    page.update()

            elif chekbox_anime.value == True:
                for row in rows:
                    lst.append(row)
                    text_id.value = row[0]
                    text_name.value = row[1]
                    text_data.value = row[2]
                    text_genre.value = row[3]
                    text_director.value = row[4]

                    text_state.value = row[5]

                    lv.controls.append(ft.Text(
                        f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}     {text_director.value}     {text_state.value}"))

                    page.update()


            elif chekbox_mult.value == True:
                for row in rows:
                    lst.append(row)
                    text_id.value = row[0]
                    text_name.value = row[1]
                    text_data.value = row[2]
                    text_genre.value = row[3]

                    text_state.value = row[4]

                    lv.controls.append(ft.Text(
                        f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}   {text_state.value}"))

                    page.update()


            elif chekbox_mult_series.value ==True:
                for row in rows:
                    lst.append(row)
                    text_id.value = row[0]
                    text_name.value = row[1]
                    text_data.value = row[2]

                    text_state.value = row[3]

                    lv.controls.append(ft.Text(
                        f"{text_id.value}   {text_name.value}   {text_data.value}   {text_state.value}"))

                    page.update()

            elif chekbox_film.value == True:
                for row in rows:
                    lst.append(row)
                    text_id.value = row[0]
                    text_name.value = row[1]
                    text_data.value = row[2]
                    text_genre.value = row[3]
                    text_director.value = row[4]
                    text_actors.value = row[5]
                    text_state.value = row[6]

                    lv.controls.append(ft.Text(
                                f"{text_id.value}   {text_name.value}   {text_data.value}    {text_genre.value}    {text_director.value}   {text_actors.value}   {text_state.value}"))

                    page.update()



    #промежуточная функция получения данных из БД с вызовом корневой функции получения данных по одному из параметров запроса
    def sub_selection_condition (table):
        if movie_name.value != "":

            sql_test(table, "name", movie_name.value)
            clear_text_fields()

            page.update()


        elif release_date.value != "":
            sql_test(table, "date", release_date.value)
            clear_text_fields()

            page.update()

        elif genre.value != "":
            sql_test(table, "genre", genre.value)
            clear_text_fields()


            page.update()


        elif director.value != "":
            sql_test(table, "director", director.value)

            clear_text_fields()

            page.update()


        elif aktors.value != "":
            sql_test(table, "actors", aktors.value)
            clear_text_fields()

            page.update()


        else:

            sqlite_get_all_data(table)



    #вызов промежуточной функции получения данных из БД по одному из параметров запроса
    def get_value(e):

        lv.controls.clear()
        page.update()
        if chekbox_film.value == True:
            sub_selection_condition("film")
            id_number.value = ""
            page.update()


        elif chekbox_series.value == True:

            sub_selection_condition("series")
            id_number.value = ""
            page.update()



        elif chekbox_anime.value == True:
            sub_selection_condition("anime")
            id_number.value = ""
            page.update()



        elif chekbox_mult.value == True:
            sub_selection_condition("cartoon")
            id_number.value = ""
            page.update()



        elif chekbox_mult_series.value == True:
           sub_selection_condition("cartoonseries")
           id_number.value = ""
           page.update()


    #корневая функция обновления данных в БД по одному параметру
    def abs_upd_query(name_table,name_column,value_column,id_value):
        lv.controls.clear()
        page.update()
        try:
            with connect('media.db') as db:
                cur = db.cursor()

            cur.execute(
                f'UPDATE {name_table}  SET  {name_column} = "{value_column}" WHERE id = "{id_value}"')

            db.commit()

        except Error as er:
            logging.exception(er, exc_info=True)
            alert_banner(er)

        lv.controls.clear()
        page.update()
        page.snack_bar = ft.SnackBar(content=ft.Text("Данные обновлены"), open=False)
        page.snack_bar.open = True
        clear_text_fields()

        upd_btn.disabled = True
        page.update()




    def update_value_db(e):

        if chekbox_film.value == True:
            sub_update_value_db("film")



        elif chekbox_series.value == True:

            sub_update_value_db("series")




        elif chekbox_anime.value == True:
            sub_update_value_db("anime")




        elif chekbox_mult == True:
            sub_update_value_db("cartoon")




        elif chekbox_mult_series == True:
            sub_update_value_db("cartoonseries")



    #функция проверки ввода поля номера по порядку для возможности включения кнопки обновления данных
    def updade_validate(e):
        if id_number.value != "":
            upd_btn.disabled = False


        else:
            upd_btn.disabled = True

        page.update()


    def sub_update_value_db(table):
        if movie_name.value != "":
            abs_upd_query(table, "name", movie_name.value,id_number.value)

        elif release_date.value !="":
            abs_upd_query(table, "date", release_date.value,id_number.value)
        elif genre.value !="":
            abs_upd_query(table, "genre", genre.value,id_number.value)
        elif director.value !="":
            abs_upd_query(table, "director", director.value,id_number.value)
        elif aktors.value !="" :
            abs_upd_query(table, "actors", aktors.value)
        elif state.value != "":
            abs_upd_query(table,"state", state.value,id_number.value)




    #функуия проверки заполнености полей ввода текста
    def validate(e):
        try:
            if all([movie_name.value,release_date.value,genre.value,director.value,aktors.value,state.value]) or all([movie_name.value,release_date.value,genre.value,aktors.value,state.value]) or all([movie_name.value,release_date.value,genre.value,director.value,state.value]): #or all(movie_name.value,release_date.value,genre.value,state.value) or all(movie_name.value,release_date.value,state.value):
                add_data_button.disabled = False

            elif movie_name.value and release_date.value and genre.value and state.value !="":
                add_data_button.disabled = False

            elif movie_name.value and release_date.value  and state.value !="":
                add_data_button.disabled = False

            else:
                add_data_button.disabled = True

        except TypeError:
            pass

        page.update()







    #функция проверки активности чекбоксов
    def checkboxes_changed(e):
        if chekbox_film.value == True:
            chekbox_series.disabled = True
            chekbox_mult.disabled = True
            chekbox_anime.disabled = True
            chekbox_mult_series.disabled = True
            clear_text_fields()

            page.update()

        elif chekbox_series.value == True:
            chekbox_mult.disabled = True
            chekbox_anime.disabled = True
            chekbox_mult_series.disabled = True
            chekbox_film.disabled = True
            director.disabled = True
            clear_text_fields()

            page.update()


        elif chekbox_anime.value == True:
            chekbox_mult.disabled = True
            chekbox_mult_series.disabled = True
            chekbox_film.disabled = True
            chekbox_series.disabled = True
            aktors.disabled = True
            clear_text_fields()

            page.update()


        elif chekbox_mult.value == True:
            chekbox_anime.disabled = True
            chekbox_mult_series.disabled = True
            chekbox_film.disabled = True
            chekbox_series.disabled = True
            director.disabled = True
            aktors.disabled = True

            genre.label = "студия"
            clear_text_fields()

            page.update()


        elif chekbox_mult_series.value == True:
            chekbox_anime.disabled = True
            chekbox_mult.disabled = True
            chekbox_film.disabled = True
            chekbox_series.disabled = True
            director.disabled = True
            aktors.disabled = True
            genre.disabled = True
            clear_text_fields()

            page.update()


        else:
            chekbox_series.disabled = False
            chekbox_mult.disabled = False
            chekbox_anime.disabled = False
            chekbox_mult_series.disabled = False
            chekbox_film.disabled = False
            director.disabled = False
            aktors.disabled = False
            genre.disabled = False
            genre.label = "жанр"
            clear_text_fields()

            page.update()

    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(""),
        actions=[ft.TextButton("Закрыть", on_click=close_banner),])

    #создание полей ввода данных
    id_number = ft.TextField(label="№п\п",width=100,input_filter=ft.InputFilter(allow= True, regex_string= r"[0-9]",replacement_string=""),on_change=updade_validate)
    movie_name = ft.TextField(label="Название", width=500,on_change= validate,input_filter=ft.InputFilter(allow= True, replacement_string="",regex_string=r"[0-9А-яA-Za-z,:.-\s/]+"))
    release_date = ft.TextField(label="год выхода", width=500,on_change= validate,input_filter=ft.InputFilter(allow= True, regex_string= r"[0-9-]",replacement_string=""))
    genre = ft.TextField(label="жанр", width=500,on_change= validate,input_filter=ft.InputFilter(allow= True, replacement_string="",regex_string=r"[ЁёА-яA-Za-z,.-\s/]+"))
    director = ft.TextField(label="режисёр", width=500,on_change= validate,input_filter=ft.InputFilter(allow= True, replacement_string="",regex_string=r"[ЁёА-я,.-\s/]+"))
    aktors = ft.TextField(label="актёры", width=500,on_change= validate, input_filter=ft.InputFilter(allow= True, replacement_string="",regex_string=r"[ЁёА-я,.-\s/]+"))
    state = ft.TextField(label="состояние", width=500,on_change= validate,
                          input_filter=ft.InputFilter(allow=True, replacement_string="",
                                                      regex_string=r"[ЁёА-я,.-\s/]+"))
    #создание чекбоксов выбора таблиц медиа
    chekbox_film = ft.Checkbox(label="Фильмы", value= False,on_change=checkboxes_changed,adaptive=True)
    chekbox_anime = ft.Checkbox(label= "Аниме",value= False,on_change=checkboxes_changed,adaptive= True)
    chekbox_mult = ft.Checkbox(label="Мультфильмы", value= False,on_change=checkboxes_changed,adaptive= True)
    chekbox_series = ft.Checkbox(label= "Сериалы", value= False,on_change=checkboxes_changed,adaptive=True)
    chekbox_mult_series = ft.Checkbox(label="Мультсериал", value= False,on_change=checkboxes_changed,adaptive= True)

    #создание кнопок действия
    get_datab = ft.OutlinedButton(text="Получить из БД", width=200, on_click=get_value)
    add_data_button = ft.OutlinedButton(text="Добавить в БД", width=200, on_click=add_value,
                                        disabled=True)
    upd_btn = ft.OutlinedButton(text="Обновить данные", width=200, disabled= True,on_click=update_value_db)

    #создание списка просмотра выходных данных результата выдачи БД
    lv = ft.ListView(expand=1, spacing=10, padding=0, auto_scroll=True, divider_thickness=1)

    page.snack_bar = ft.SnackBar(content=ft.Text("Данные добавлены"), open=False)

    #текстовые поля содержимые объекта Списка Просмотра созданого выше
    text_id = ft.Text(value="")
    text_name = ft.Text(value="TEST_NAME")
    text_data = ft.Text(value="TEST_DATE")
    text_genre = ft.Text(value="TEXT_GENRE")
    text_director = ft.Text(value="TEST_DIRECTOR")
    text_actors = ft.Text(value="TEXT_ACTORS")
    text_state = ft.Text(value="TEST_STATE")



    results_panel = ft.Row([id_number,ft.Text("       ",weight=ft.FontWeight.BOLD),
                            ft.Text("          ",weight=ft.FontWeight.BOLD),
                            ft.Text("Результаты выдачи",weight=ft.FontWeight.BOLD),
                            ft.Text("        ",weight=ft.FontWeight.BOLD),
                            ft.Text("          ",weight=ft.FontWeight.BOLD)],wrap=True,spacing=50)
    panel_checkboxes0 = ft.Row(
        [ft.Row([chekbox_film,
            chekbox_series,
            chekbox_anime,
            chekbox_mult,
            chekbox_mult_series],),results_panel],spacing=30,)

    panel_textfields = ft.Row( [ft.Column([movie_name,release_date,genre,director,aktors,state]),lv],spacing= 50,auto_scroll=True)
    panel_buttons = ft.Row([add_data_button,get_datab,upd_btn],spacing= 20)


    page.add(panel_checkboxes0,panel_textfields,panel_buttons)  #добавление элементов созданых выше в основное окно



#основная точка входа выполнения кода
if __name__ == "__main__":
    sqlite_create_db()
    ft.app(main)


