import PySimpleGUI as sg
import sqlite3

def db_commands(query):
    with sqlite3.connect('dados.db') as con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return cur.fetchall()


layout_title = "Sistema de Cadastro"
headings = ["Nome","CPF","Email","Telefone"]
data = db_commands("SELECT * FROM users")

def main_window():
    window_main = [
    [sg.Text("Nome"),sg.Push(),sg.Input(key="-NAME-")],
    [sg.Text("CPF"),sg.Push(),sg.Input(key='-CPF-')],
    [sg.Text("Email"),sg.Push(),sg.Input(key='-EMAIL-')],
    [sg.Text("telefone"),sg.Push(),sg.Input(key='-PHONE-')],
    [sg.Button("Cadastrar"),sg.Button("Lista de Usuários",key="users"),sg.Button("Close")]]

    return sg.Window(layout_title,layout=window_main)

def table_window():
    table = [[sg.Table(values=data, headings=headings,
                   auto_size_columns=True,
                   num_rows=10,
                   justification='center',
                   key="-TABLE-",
                   selected_row_colors='red on yellow',
                   enable_click_events=True,
                   enable_events=True
                    )],
        [sg.Button("Editar",key="edit"),sg.Button("Voltar")]]

    return sg.Window(layout_title,layout=table)


def layout_update(id):
    name = db_commands("SELECT name, cpf, email, telefone FROM users WHERE cpf={}".format(id))
    window_edit  = [
        [sg.Text("Nome"),sg.Push(),sg.InputText(name[0][0])],
        [sg.Text("CPF"),sg.Push(),sg.InputText(name[0][1])],
        [sg.Text("Email"),sg.Push(),sg.InputText(name[0][2])],
        [sg.Text("Telefone"),sg.Push(),sg.InputText(name[0][3])],
        [sg.Button("Salvar",key="-SAVE-")]
    ]

    return sg.Window(layout_title,layout=window_edit)

def main():
    window_1 = main_window()
    while True:
        event, values = window_1.read(timeout=100)
        if event == sg.WIN_CLOSED or event == "Close":
            window_1.close()
            break

        if event == "Cadastrar":
            for value in values:
                pass

            if values[value] == '':
                sg.popup_error("Insira os Valores!")
            else:
                try:
                    db_commands(f"""INSERT INTO users
                    VALUES ("{values['-NAME-']}",
                    {values['-CPF-']},
                    "{values["-EMAIL-"]}",
                    {values['-PHONE-']})""")

                except sqlite3.IntegrityError:
                    sg.popup_error("CPF ou Email Já Cadastrados")
                else:
                    for key in values:
                        window_1[key]('')
                    sg.popup("Cliente Cadastrado com Sucesso!")

        if event == "users":
            window_1.Hide()
            window_2 = table_window()
            while True:
                event_table, value_table = window_2.read(timeout=100)
                if event_table == sg.WIN_CLOSED or event_table == "Voltar":
                    window_2.close()
                    window_1.UnHide()
                    break
                
                if "+CLICKED+" in event_table:
                    data_event_click = event_table[2][0]

                if event_table == "edit":
                    try:
                        window_3 = layout_update(data[data_event_click][1])
                    except UnboundLocalError:
                        pass
                    else:
                        while True:
                            event_update, value_update = window_3.read()
                            if event_update == "-SAVE-":
                                # if data[teste][0] == value_update[0]:
                                #     sg.popup("Nenhuma alteraçao feita")
                                db_commands(f"""UPDATE users SET name='{value_update[0]}',
                                        cpf={value_update[1]},
                                        email='{value_update[2]}',
                                        telefone={value_update[3]}
                                        WHERE cpf={data[data_event_click][1]}""")
                                
                                sg.popup("Dados Atualizados")
                                window_3.close()

                            if event_update == sg.WIN_CLOSED:
                                window_3.close()
                                break
                            
if __name__=="__main__":
    db_commands("""CREATE TABLE IF NOT EXISTS users(
                name TEXT,
                cpf INTEGER NOT NULL UNIQUE PRIMARY KEY,
                email TEXT UNIQUE,
                telefone INTEGER)""")
    main()

