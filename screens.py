from cProfile import label
import PySimpleGUI as sg
from matplotlib.style import available
import services
import mysql.connector
import new2

login =[
    [sg.Text('username', size=(8, 1)),sg.InputText(key='username')],
    [sg.Text('password', size=(8, 1)),sg.InputText(key='password',password_char='*')],
    [sg.Button('login')]
]

def get_view_players(list):
    return [[sg.Text(text="Player List")], [sg.Table(list, headings=['Id', 'Name', 'Gender', 'Age', 'email'])]]

def get_view_sports(list):
    return [[sg.Text(text="Sports List")], [sg.Table(list, headings=['Id', 'Name'])]]

def get_view_tournaments(list):
    return [[sg.Text(text="Tournament List")], [sg.Table(list, headings=['Id', 'Name', 'Description', 'SportId'])]]

def get_admin_dashboard():
    return [[sg.Text(text="Admin Dashboard")], [sg.Column([[sg.Button(button_text="Create Tournament", expand_x=True), sg.Button(button_text="View Tournaments", expand_x=True)]])], [sg.Button(button_text="Create Sport", expand_x=True), sg.Button(button_text="View Sports", expand_x=True)], [sg.Button(button_text="Create Player"), sg.Button(button_text="View Players")]]

def get_player_dashboard(name,gender,age,email,sports):
    player_dashboard = [[sg.Text(text="Sports Management System", size=(100, 2)), sg.Column([[sg.Text(text="Welcome, "+name.split(" ")[0])], [sg.Text(text="You are logged in as a user")]])], [sg.Table([['Name', name], ['Gender', gender], ['Age', age], ['email', email]], headings=['Personal', 'Details'], col_widths=80, def_col_width=80, max_col_width=90, row_height=20, justification="center", hide_vertical_scroll=True, size=(None, 5), expand_x=True, expand_y=True), sg.Column([[sg.Text(text="Sports list")], [sg.Table(sports, headings=['Sports'], justification="centre", size=(None, 5), expand_x=True, expand_y=True)]], pad=0, expand_x=True, expand_y=True)], [sg.Text(text="Actions : "), sg.Button(button_text="Enroll In new Sport", pad=(50, 5)),sg.Button(button_text="Delist from Sport", pad=(50, 5)), sg.Button(button_text="View Team Information", pad=(50, 5)), sg.Button(button_text="View Tournament List", pad=(50, 5))]]
    return player_dashboard

def  get_team_dashboard(teams):
    x= []
    for i in teams:
        x.append([sg.Table(values=i[2:],headings=[i[1]], def_col_width=15, auto_size_columns=False, num_rows=5, justification="center", hide_vertical_scroll=True), sg.Column([[sg.Button(button_text="Disband Team", expand_x=True, expand_y=True,key=("disband"+i[0]))], [sg.Button(button_text="Add player", expand_x=True, expand_y=True,key=("add"+i[0]))]])])
    team_dashboard = [[sg.Text(text="Team View"), sg.Button(button_text="Create Team", expand_x=True, expand_y=True)], x]
    return team_dashboard

def get_tournament_dashboard(tournaments,enrolled):
    available_list = [[sg.Text(text="Available")]]
    enrolled_list =  [[sg.Text(text="Enrolled")]]
    for i in tournaments:
        available_list.append([sg.Column([[sg.Text(text=i[1])]]), sg.Column([[sg.Button(button_text="Enroll", key = ("enroll"+str(i[0])))]])])
    for i in enrolled:
        enrolled_list.append([sg.Column([[sg.Text(text=i[1])]]), sg.Column([[sg.Button(button_text="Remove", key = ("remove"+str(i[0])))]])])
    y=[[sg.Text(text="Tournaments")], [sg.Canvas(background_color="black", size=(400, 1))], [sg.Column(enrolled_list), sg.Canvas(background_color="black", size=(1, 100)), sg.Column(available_list)]]
    return y
#utility functions
def get_key(my_dict,val):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"

layout = [[sg.Text('Welcome to the Sports Database')]]
window = sg.Window('Sports Management System', login)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "pass1234@",
    database = 'mydb'
)
cursor = mydb.cursor()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if(event == 'login'):
        auth = services.authenticate(values['username'],values['password'],mydb)
        if auth[0]:
            if auth[1] == 'user':
                flag="Dashboard"
                while flag!="Exit":
                    if flag == "Dashboard":
                        print('logged in as user')
                        window.close()
                        print(auth)
                        player=services.getPlayer(auth[2],mydb)
                        sports_list=[]
                        for i in services.getPlayerSports(auth[2],mydb):
                            sports_list.append([i[1]])
                        all_sports={}
                        for i in services.getAllSports(mydb):
                            if(i[1] not in sum(sports_list, [])):
                                all_sports[i[1]]=i[0]
                        window = sg.Window('Sports Management System', get_player_dashboard(player[1],player[2],player[3],player[4],sports_list))
                        event, values = window.read()
                        print(event)
                        if event == 'Enroll In new Sport':
                            if(len(list(all_sports.keys()))==0):
                                sg.Popup('You have enrolled in all available sports')
                            else:
                                selection = new2.popup_select(list(all_sports.keys()))
                                services.assignSport(auth[2],all_sports[selection],mydb)
                                sg.popup('You have enrolled in '+selection+' successfully')
                        if event == 'Delist from Sport':
                            if(len(sports_list)==0):
                                sg.Popup('You are not enrolled in any sports')
                            else:
                                selection = new2.popup_select(sports_list)
                                selection_id= get_key(dict(services.getAllSports(mydb)),selection[0])
                                services.unassignSport(auth[2],selection_id,mydb)
                                sg.popup('You have delisted from '+selection[0]+' successfully')
                        if event == 'View Team Information':
                            flag="Team"
                            window.close()
                            continue
                        if event == 'View Tournament List':
                            flag = "Tournaments"
                            window.close()
                            continue
                        if event == sg.WIN_CLOSED:
                            flag="Exit"
                    elif(flag=="Team"):
                        temp=[]
                        teams = services.getTeamIds(auth[2],mydb)
                        for i in teams:
                            x = services.getTeam(i[0],mydb)
                            t1 = [str(x[0]),str(x[1])]
                            for j in services.getPlayerIds(x[0],mydb):
                                t1.append(services.getPlayer(j[0],mydb)[1])
                            temp.append(t1)
                        window.close()
                        window = sg.Window('Sports Management System', get_team_dashboard(temp))
                        event, values = window.read()
                        print(event)
                        if event == sg.WIN_CLOSED:
                            flag = 'Dashboard'
                        elif event == "Create Team":
                            selection = new2.popup_select(services.getAllSports(mydb))
                            player=services.getPlayer(auth[2],mydb)
                            services.createTeam(auth[2],player[1]+"'s "+selection[1]+" Team",selection[0],mydb)
                        elif event.__contains__('disband'):
                            services.disbandTeam(event.replace('disband',''),mydb)
                        elif event.__contains__('add'):
                            services.assignPlayer(sg.popup_get_text("Enter player Id of player to add"),event.replace('add',''),mydb)
                    elif(flag=="Tournaments"):
                        all_tournaments = services.getJoinableTournaments(auth[2],mydb)
                        player_tournaments = services.getPlayerTournaments(auth[2],mydb)
                        available_tournaments = []
                        if(player_tournaments):
                            for i in all_tournaments :
                                if(i[0] not in list(zip(*player_tournaments))[0]):
                                    available_tournaments.append((i[0],i[1]))
                        else:
                            for i in all_tournaments :
                                available_tournaments.append((i[0],i[1]))
                        window.close()
                        window = sg.Window('Sports Mangement System', get_tournament_dashboard(available_tournaments,player_tournaments))
                        event, values = window.read()
                        print(event)
                        if event == sg.WIN_CLOSED:
                            flag = 'Dashboard'
                        elif event.__contains__('enroll'):
                            services.assignPlayerTournament(auth[2],event.replace('enroll',''),mydb)
                        elif event.__contains__('remove'):
                            services.removePlayerTournament(auth[2],event.replace('remove',''),mydb)
            elif auth[1] == 'admin':
                flag="Dashboard"
                while flag!="Exit":
                    if flag == "Dashboard":
                        print('logged in as admin')
                        window.close()
                        print(auth)
                        window = sg.Window('Sports Management System', get_admin_dashboard())
                        event, values = window.read()
                        print(event)
                        if event == sg.WIN_CLOSED:
                            flag="Exit"
                        if event == 'View Tournaments':
                            flag = "View Tournaments"
                            window.close()
                            continue
                        if event == 'View Players':
                            flag = "View Players"
                            window.close()
                            continue
                        if event == 'View Sports':
                            flag = "View Sports"
                            window.close()
                            continue
                        if event == "Create Tournament":
                            name = sg.popup_get_text("Enter Tournament Name")
                            desc = sg.popup_get_text("Enter Tournement Description")
                            sportId = sg.popup_get_text("Enter Sport Id")
                            services.setTournament(name,desc,sportId,mydb)
                        if event == "Create Sport":
                            name = sg.popup_get_text("Enter Sport Name")
                            services.setSport(name,mydb)
                        if event == "Create Player":
                            name = sg.popup_get_text("Enter Player Name")
                            gender = sg.popup_get_text("Enter Player Gender")
                            age = sg.popup_get_text("Enter Player age")
                            email = sg.popup_get_text("Enter Player Email")
                            password = sg.popup_get_text("Enter Player Password")
                            services.setPlayer(name,gender,age,email,password,mydb)
                    elif(flag == "View Players"):   
                        window.close()
                        window = sg.Window('Sports Mangement System', get_view_players(services.getAllPlayers(mydb)))
                        event, values = window.read()
                        print(event)
                        if event == sg.WIN_CLOSED:
                            flag = 'Dashboard'
                    elif(flag == "View Tournaments"):   
                        window.close()
                        window = sg.Window('Sports Mangement System', get_view_tournaments(services.getAllTournaments(mydb)))
                        event, values = window.read()
                        print(event)
                        if event == sg.WIN_CLOSED:
                            flag = 'Dashboard'
                    elif(flag == "View Sports"):   
                        window.close()
                        window = sg.Window('Sports Mangement System', get_view_sports(services.getAllSports(mydb)))
                        event, values = window.read()
                        print(event)
                        if event == sg.WIN_CLOSED:
                            flag = 'Dashboard'
                        

        else:
            print(sg.popup(auth[1]))
window.close()