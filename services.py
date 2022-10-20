import mysql.connector
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

passkey=b"1234567890123456"

#utility functions
def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  
    IV = Random.new().read(AES.block_size)  
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  
    source += bytes([padding]) * padding  
    data = IV + encryptor.encrypt(source) 
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  
    IV = source[:AES.block_size]  
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  
    padding = data[-1]  
    if data[-padding:] != bytes([padding]) * padding:  
        raise ValueError("Invalid padding...")
    return data[:-padding]
 

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "pass1234@",
    database = 'mydb'
)
cursor = mydb.cursor()

#function to read player details and persist in database
def setPlayer(player_name,player_gender,player_age,player_email,password,db):
    #todo - validate input data
    sql = "INSERT INTO PLAYERS (name,gender,age,email) VALUES (%s,%s,%s,%s)"
    values = [player_name, player_gender, player_age, player_email]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    sql = "SELECT LAST_INSERT_ID();"
    cursor.execute(sql) 
    newId=cursor.fetchone()[0];
    userId = player_name.split(' ')[0].lower() +'.'+ str(newId)
    encPassword = encrypt(passkey,bytes(password,'utf-8'))
    sql = "INSERT INTO CREDENTIALS (playerId,username,password, isAdmin) VALUES (%s,%s,%s,%s)"
    values = [newId,userId,encPassword,0]
    cursor.execute(sql, values)
    db.commit()
    print("Player %s added",player_name)
    print("Player user ID is : ",userId)
    return (newId, userId)

#function to fetch player by id
def getPlayer(playerId,db):
    sql = "SELECT * FROM PLAYERS WHERE playerId = %s"
    values = [playerId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    player = cursor.fetchone()
    return player

#function to fetch all players
def getAllPlayers(db):
    sql = "SELECT * FROM PLAYERS"
    cursor = db.cursor()
    cursor.execute(sql)
    players = cursor.fetchall()
    return players

#funtion to add sport
def setSport(sport_name,db):
    sql = "INSERT INTO SPORTS (sportName) VALUES (%s)"
    values = [sport_name]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    sql = "SELECT LAST_INSERT_ID();"
    cursor.execute(sql) 
    newId=cursor.fetchone()[0];
    print("Sport %s added",sport_name)
    return newId
#function to add player to sport
def getAllSports(db):
    sql = "SELECT * FROM SPORTS"
    cursor = db.cursor()
    cursor.execute(sql)
    sports = cursor.fetchall()
    return sports

#function to add player to sport
def getSport(sportId,db):
    sql = "SELECT * FROM SPORTS WHERE sportId = %s"
    values = [sportId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    sport = cursor.fetchone()
    return sport

#funtion to create team
def createTeam(captain,team_name,sport_id,db):
  #todo - validate captain id
    sql = "INSERT INTO TEAMS (teamName,sportId,captainId) VALUES (%s,%s,%s)"
    values = [team_name,sport_id,captain]
    cursor = db.cursor()
    cursor.execute(sql, values)
    sql = "SELECT LAST_INSERT_ID();"
    cursor.execute(sql) 
    newId=cursor.fetchone()[0];
    sql = "INSERT INTO PLAYER_TEAM_MAPPING (playerId,teamId) VALUES (%s,%s)"
    values = [captain,newId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    print("Team %s added",team_name)
    return newId

#function to get all teams
def getAllTeams(db):
    sql = "SELECT * FROM TEAMS"
    cursor = db.cursor()
    cursor.execute(sql)
    teams = cursor.fetchall()
    return teams

#function to get team by id
def getTeam(teamId,db):
    sql = "SELECT * FROM TEAMS WHERE teamId = %s"
    values = [teamId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    team = cursor.fetchone()
    return team

#function to get teams by player id
def getTeamIds(playerId,db):
    sql = "SELECT teamId FROM player_team_mapping WHERE playerId = %s"
    values = [playerId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    team = cursor.fetchall()
    return team

#function to get players by team id
def getPlayerIds(teamId, db):
    sql = "SELECT playerId FROM player_team_mapping WHERE teamId = %s"
    values = [teamId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    team = cursor.fetchall()
    return team
#function to disband team
def disbandTeam(teamId,db):
    sql = "DELETE FROM player_team_mapping WHERE teamId = %s"
    values = [teamId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    sql = "DELETE FROM teams WHERE teamId = %s"
    values = [teamId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit
    return True


#function to add player to team
def assignPlayer(playerId,teamId,db):
    sql = "INSERT INTO player_team_mapping (playerId,teamId) VALUES (%s,%s)"
    values = [playerId,teamId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    print("Player %s added to team %s",playerId,teamId)
    return True

#function to remove player to team
def unassignPlayer(playerId,teamId,db):
    sql = "DELETE FROM player_team_mapping WHERE playerId = %s AND teamId = %s"
    values = [playerId,teamId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    print("Player %s removed from team %s",playerId,teamId)
    return True

#function to assing player to sport
def assignSport(playerId,sportId,db):
    sql = "INSERT INTO player_sport_mapping (playerId,sportId) VALUES (%s,%s)"
    values = [playerId,sportId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    print("Player %s added to sport %s",playerId,sportId)
    return True

#funtion to unassign player from sport
def unassignSport(playerId,sportId,db):
    sql = "DELETE FROM player_sport_mapping WHERE playerId = %s AND sportId = %s"
    values = [playerId,sportId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    print("Player %s removed from sport %s",playerId,sportId)
    return True

#function to fetch player sport list
def getPlayerSports(playerId,db):
    sql = "SELECT player_sport_mapping.sportId,sports.sportName FROM player_sport_mapping,sports WHERE player_sport_mapping.sportId=sports.sportId and playerId = %s"
    values = [playerId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    sports = cursor.fetchall()
    return sports

#function to add tournament
def setTournament(tournament_name,tournament_description,sport_id,db):
    sql = "INSERT INTO TOURNAMENTS (tournamentName,tournamentDescription,sportId) VALUES (%s,%s,%s)"
    values = [tournament_name,tournament_description,sport_id]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    sql = "SELECT LAST_INSERT_ID();"
    cursor.execute(sql) 
    newId=cursor.fetchone()[0];
    print("Tournament %s added",tournament_name)
    return newId
  
#function to get all tournaments
def getAllTournaments(db):
    sql = "SELECT * FROM TOURNAMENTS"
    cursor = db.cursor()
    cursor.execute(sql)
    tournaments = cursor.fetchall()
    return tournaments

#function to get tournament by id
def getTournament(tournamentId,db):
    sql = "SELECT * FROM TOURNAMENTS WHERE tournamentId = %s"
    values = [tournamentId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    tournament = cursor.fetchone()
    return tournament

def getPlayerTournaments(playerId, db):
    sql = "SELECT tournament_team_mapping.tournamentId, tournaments.tournamentName FROM player_team_mapping, tournament_team_mapping, tournaments where player_team_mapping.teamId = tournament_team_mapping.teamId and tournament_team_mapping.tournamentId = tournaments.tournamentId and player_team_mapping.playerId = %s"
    values = [playerId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    tournaments = cursor.fetchall()
    return tournaments


def getJoinableTournaments(playerId, db):
    sql = "SELECT tournaments.tournamentId,tournaments.tournamentName from player_team_mapping, teams, tournaments where player_team_mapping.teamId= teams.teamId and playerId = %s and teams.sportId = tournaments.sportId"
    values = [playerId]
    cursor = db.cursor()
    cursor.execute(sql,values)
    tournaments = cursor.fetchall()
    return tournaments

def assignPlayerTournament(playerId, tournamentId,db):
    sql = "INSERT into tournament_team_mapping (tournamentId, teamId) values (%s, (SELECT MIN(teams.teamId) from player_team_mapping, teams, tournaments where player_team_mapping.teamId= teams.teamId and playerId = %s and teams.sportId = tournaments.sportId))"
    values = [tournamentId, playerId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()

def removePlayerTournament(playerId, tournamentId, db):
    sql = "DELETE from tournament_team_mapping where tournamentId = %s and teamId = (SELECT MIN(teams.teamId) from player_team_mapping, teams, tournaments where player_team_mapping.teamId= teams.teamId and playerId = %s and teams.sportId = tournaments.sportId)"
    values = [tournamentId,playerId]
    cursor = db.cursor()
    cursor.execute(sql,values)
    db.commit()

#function to add team to tournament
def assignTournament(teamId,tournamentId,db):
    sql = "INSERT INTO tournament_team_mapping (teamId,tournamentId) VALUES (%s,%s)"
    values = [teamId,tournamentId]
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    print("Team %s added to tournament %s",teamId,tournamentId)
    return True

#auth function
def authenticate(username,password,db):
    sql = "SELECT * FROM CREDENTIALS WHERE username = %s"
    values = [username]
    cursor = db.cursor()
    cursor.execute(sql, values)
    user = cursor.fetchone()
    if user is None:
      return False,"invalid username"
    else:
      decPassword = decrypt(passkey,user[2])
      if decPassword.decode('utf-8') == password:
        if user[3] == 1:
          return True,"admin",user[0]
        else:
          return True,"user",user[0]
      else:
        return False,"invalid password"


# setPlayer("XYZ","M","25","name@domain.com","password",mydb)
# print(getPlayer(9 ,mydb))
# print(authenticate("anirudh.9","hello",mydb))