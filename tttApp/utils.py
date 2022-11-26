from rest_framework import status
from rest_framework.response import Response
from tttApp.models import User, Game
from tttApp.serializers import UserSerializer, GameSerializer

# Convert a string separated by ";" in a list #
def str_to_list(str):
    return str.split(";")

# Convert a list in a string separated by ";" #
def list_to_str(list):
    return ";".join(list)

# Update the turn of the game #
def update_turn(game):
    t = game.turn
    id_player1 = game.id_player1
    id_player2 = game.id_player2

    if t == id_player1:
        return id_player2
    return id_player1

# Delete the game from the users who were playing it #
def delete_game_in_users(idGame, idUser1, idUser2):
    idGame = str(idGame)
    user1 = User.objects.filter(id = idUser1).first()
    user2 = User.objects.filter(id = idUser2).first()
    
    try:
        actual_games_1 = str_to_list(user1.actual_game)
        actual_games_2 = str_to_list(user2.actual_game)

        actual_games_1.remove(idGame)
        actual_games_2.remove(idGame)

        serializer1 = UserSerializer(user1, data={'actual_game': list_to_str(actual_games_1)}, partial=True)
        serializer2 = UserSerializer(user2, data={'actual_game': list_to_str(actual_games_2)}, partial=True)
    
    except:
        
        serializer1 = UserSerializer(user1, data={'actual_game': ""}, partial=True)
        serializer2 = UserSerializer(user2, data={'actual_game': ""}, partial=True)

    if serializer1.is_valid():
        serializer1.save()
    if serializer2.is_valid():
        serializer2.save()

# Update stats of the players after finishing the game #
def update_stats_players(winner, loser, tie=False):
    user1 = User.objects.filter(id = winner).first()
    user2 = User.objects.filter(id = loser).first()
        
    if not tie:
        won_games = user1.won_games
        lost_games = user2.lost_games

        req1 = {"won_games": won_games+1}
        req2 = {"lost_games": lost_games+1}
    else:
        tied_games1 = user1.tied_games
        tied_games2 = user2.tied_games
        req1 = {"tied_games": tied_games1+1}
        req2 = {"tied_games": tied_games2+1}


    serializer1 = UserSerializer(user1, data=req1, partial=True)
    serializer2 = UserSerializer(user2, data=req2, partial=True)

    if serializer1.is_valid():
        serializer1.save()
    if serializer2.is_valid():
        serializer2.save()

# Check if game is finished (with a winner) from current board #
def game_finished(b):
    combos = [
        b[0] == b[1] == b[2] != "0",
        b[0] == b[3] == b[6] != "0",
        b[0] == b[4] == b[8] != "0",
        b[1] == b[4] == b[7] != "0",
        b[3] == b[4] == b[5] != "0",
        b[6] == b[7] == b[8] != "0",
        b[2] == b[4] == b[6] != "0",
        b[2] == b[5] == b[8] != "0",
        b[0] == b[1] == b[2] != "0",
        "0" not in b,
    ]

    if True in combos:
        return True
    else:
        return False

# Check if the mvoement is allowed #
def allowed_movement(game, new_b):
    b = game.board
    t = game.turn
    id_player1 = game.id_player1
    id_player2 = game.id_player2
    
    if id_player1==None or id_player2==None:
        return False 
    res = True
    cont_changes = 0
    for i,j in zip(b, new_b):
        if i!=j:
            cont_changes += 1
            if i!='0':
                res = False
            elif t==id_player1 and j=="2":
                res = False
            elif t==id_player2 and j=="1":
                res = False 
    if cont_changes != 1:
        res = False
    return res

# Check if user is registered #
def check_player(idUser):
    user = User.objects.filter(id = idUser).first()
    if not user:
        return False
    return True

# Add player to game #
def add_player_to_game(idGame, idUser):
    user = User.objects.filter(id = idUser).first()
    actual_games = user.actual_game
    if actual_games == '':
        actual_games = str(idGame)
    else:
        actual_games = str_to_list(actual_games)
        actual_games.append(str(idGame))
        actual_games = list_to_str(actual_games)
    serializer = UserSerializer(user, data={"actual_game": actual_games}, partial=True)
    if serializer.is_valid():
        serializer.save()

# Check if player can join the game. If true, user joins it #
def waiting_player_to_game(game, idUser):
    if game.id_player2 == None:
        add_player_to_game(game.id, idUser)
        return True
    return False

# Check if the user who is making the move is in the game and if it is his turn or not #
def user_in_game_and_his_turn(idUser, game):
    
    if game.id_player1 == idUser or game.id_player2 == idUser:
        if game.turn == idUser:
            return True
    return False

# Check if game has finished with a tie #
def check_tie(b):
    if not '0' in b:
        return True
    return False 

# Check if an user is registered or not #
def check_user(usern):
    user = User.objects.filter(username = usern).first()
    if(user):
        return False
    return True

# Check if password is correct #
def check_password(usern, password):
    user = User.objects.filter(username = usern).first()
    if user.password == password:
        return True
    return False

# Check if game exists #
def check_game(idGame):
    game = Game.objects.filter(id = idGame).first()
    if (game):
        return True
    return False
    