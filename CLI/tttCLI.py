import requests
import sys

def index():
    print(" What do you want? ")
    print("[1] Sign Up")
    print("[2] Log in")
    print("[3] Exit")
    n = input()
    
    while n!="1" and n!="2" and n!="3":
        print("\n")
        print("Please enter a valid input")
        n = input()
    
    if n=='1':
        print("\n")
        signup()
    elif n=='2':
        print("\n")
        login()
    elif n=='3':
        print("\n")
        print("See you soon. Goodbye.")
        sys.exit()

def signup():
    print("\n")
    print("Enter your username: ")
    username = input()
    print("Enter your password: ")
    password = input()
    if username == '' or password == '':
        print("\n")
        print("Please enter a valid username or password.")
        signup()
    r = requests.post(url = 'http://localhost:8000/api/user/', data = {"username": username, "password": password})
    if r.status_code == 400:
        print("\n")
        print(r.json())
        signup()
    print("\n")
    print("The user has been successfully registered.")
    print("\n")
    index()

def login():
    print("Enter your username: ")
    username = input()
    print("Enter your password: ")
    password = input()
    r = requests.patch(f'http://localhost:8000/api/user/login/', data = {"username":username, "password":password})
    if r.status_code == 400:
        print("\n")
        print(r.json())
        print("\n")
        login()
    print("\n")
    user_stage(username)

def user_stage(username):
    users = requests.get("http://localhost:8000/api/user/").json()
    for user in users:
        if user['username'] == username:
            idUser = user['id']
    print(f"Welcome {username}, what do you want?")
    print("[1] See my statistics")
    print("[2] Create a game")
    print("[3] Join game")
    print("[4] Start Game")
    print("[5] Exit")
    n = input()

    while n!="1" and n!="2" and n!="3" and n!="4" and n!="5":
        print("\n")
        print("Please enter a valid input")
        n = input()
    
    if n=="1":
        print("\n")
        user = requests.get(f"http://localhost:8000/api/user/{idUser}/").json()
        print(f"Your stats are: {user['won_games']} wins, {user['lost_games']} losses, {user['tied_games']} ties.")
        print("\n")
        user_stage(username)
    
    elif n=="2":
        create_game(idUser, username)

    elif n=="3":
        join_game(idUser, username)

    elif n=="4":
        start_game(idUser, username)
    
    elif n=="5":
        index()

def create_game(idUser, username):
    print("\n")
    r = requests.post('http://localhost:8000/api/game/', data = {'id_player1': idUser})
    if r.status_code == 400:
        print(r.json())
        print("\n")
        create_game()
    print("\n")
    idGame = r.json()['id']
    print(f"Game with ID {idGame} has been created successfully. When player 2 joins it, click on START GAME")
    print("\n")
    user_stage(username)

def join_game(idUser, username):
    print("\n")
    print("Enter Game ID:")
    idGame = input()
    if idGame == '':
        print("\n")
        print("Please enter a valid Game ID.")
        join_game(idUser, username)
    idGame = int(idGame)
    r = requests.put(f'http://localhost:8000/api/game/{idGame}/user/', data = {'id_player2': idUser})
    if r.status_code == 400:
        print("\n")
        print(r.json())
        print("\n")
        join_game(idUser, username)
    print("\n")
    print(f"You have been added to the game with id {idGame}. If you want to play, click on START GAME")
    print("\n")
    user_stage(username)

def start_game(idUser, username):
    print("\n")
    print("Enter Game ID:")
    idGame = input()
    if idGame == '':
        print("\n")
        print("Please enter a valid Game ID.")
        start_game(idUser, username)
    idGame = int(idGame)
    r = requests.get(f'http://localhost:8000/api/game/{idGame}/')
    if r.status_code == 400:
        print(r.json())
        print("\n")
        start_game(idUser, username)
    if idUser != r.json()['id_player1'] and idUser != r.json()['id_player2']:
        print("\n")
        print("You cannot access this game. You are not playing in it")
        print("\n")
        start_game(idUser, username)
    print("\n")
    game_stage(idGame, idUser, username)

def print_board(board):
    virgin_board = "---------\n| - - - |\n| - - - |\n| - - - |\n---------"
    virgin_board = virgin_board[:12] + board[0] + virgin_board[13:]
    virgin_board = virgin_board[:14] + board[1] + virgin_board[15:]
    virgin_board = virgin_board[:16] + board[2] + virgin_board[17:]
    virgin_board = virgin_board[:22] + board[3] + virgin_board[23:]
    virgin_board = virgin_board[:24] + board[4] + virgin_board[25:]
    virgin_board = virgin_board[:26] + board[5] + virgin_board[27:]
    virgin_board = virgin_board[:32] + board[6] + virgin_board[33:]
    virgin_board = virgin_board[:34] + board[7] + virgin_board[35:]
    virgin_board = virgin_board[:36] + board[8] + virgin_board[37:]
    virgin_board = virgin_board.replace('0', '-')
    virgin_board = virgin_board.replace('1', 'O')
    virgin_board = virgin_board.replace('2', 'X')
    print(virgin_board)

def move_to_board(move, board, player):
    m = int(move)-1
    if player == 1:
        mark = "1"
    else:
        mark = "2"
    new_board = board[:m]+mark+board[m+1:] 
    return new_board

def game_stage(idGame, idUser, username):
    print("Player 1 -> O")
    print("Player 2 -> X")
    game = requests.get(f"http://localhost:8000/api/game/{idGame}/")
    if idUser == game.json()['id_player1']:
        print("You are Player 1")
        who_i_am = 1
    else:
        print("You are Player 2")
        who_i_am = 2
    print_board(game.json()['board'])
    while not game.json()['winner']:
        if game.json()['turn'] == idUser:
            print("It's your turn. Enter a valid move from 1 to 9 to select the square on the board.")
            n = input()
            movements = [str(x) for x in range(1,10)]
            if n not in movements:
                print("\n")
                print("Please enter a valid move.")
                print("\n")
                game_stage(idGame, idUser, username)
            new_board = move_to_board(n, game.json()['board'], who_i_am)
            r = requests.patch(f'http://localhost:8000/api/game/{idGame}/move/', data={"id_player":idUser, "board":new_board})
            if r.status_code == 400:
                print("\n")
                print(r.json())
                print("\n")
            game_stage(idGame, idUser, username)
        else:
            print("It's not your turn. Please press enter to reload and check if the other player has already moved.")
            n = input()
            game_stage(idGame, idUser, username)
    if game.json()['winner'] == idUser:
        print("\n")
        print("TIC TAC TOE! Congratulations! You won this game!")
        print("\n")
    elif game.json()['winner'] == game.json()['id_player1'] or game.json()['winner'] == game.json()['id_player2']:
        print("\n")
        print("Sorry, you lost the game :(")
        print("\n")
    else:
        print("\n")
        print("Game Over with a tie")
        print("\n")
    print("Press enter to go to your user page.")
    input()
    user_stage(username)

if __name__ == "__main__":
    print("WELCOME TO TIC TAC TOE GAME")
    print("--------------------")
    print("|  O --  X  --  X  |")
    print("|  X --  O  --  X  |")
    print("|  X --  X  --  O  |")
    print("--------------------")
    
    index()
        
            

