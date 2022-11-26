from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from tttApp.serializers import UserSerializer, GameSerializer
from tttApp.models import User, Game
import tttApp.utils as utils
import requests

class UserAPI(APIView):
    
    def get(self, request, idUser=None):
        if (idUser):
            user = User.objects.filter(id = idUser).first()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        users = User.objects.all().order_by('id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not utils.check_user(request.data['username']):
            return Response("The user is already registered. Please enter a valid username.", status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if utils.check_user(request.data['username']):
            return Response("The user does not exist.", status=status.HTTP_400_BAD_REQUEST)
        
        if not utils.check_password(request.data['username'], request.data['password']):
            return Response("The password is not correct", status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)

    def put(self,request,idUser):
        user = User.objects.filter(id = idUser).first()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if user and serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,idUser):
        user = User.objects.filter(id = idUser).first()
        serializer = UserSerializer(user)
        if (user):
            print(f"User {user.id} deleted")
            user.delete()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GameAPI(APIView):
    
    def get(self, request, idGame=None):
        if (idGame):
            game = Game.objects.filter(id = idGame).first()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        games = Game.objects.all().order_by('id')
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        idUser = request.data['id_player1']
        new_request = {'id_player1': idUser}

        if not utils.check_player(idUser):
            return Response("That user is not registered", status=status.HTTP_400_BAD_REQUEST)

        new_request['turn'] = idUser
        serializer = GameSerializer(data=new_request)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        utils.add_player_to_game(serializer.data['id'], idUser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, idGame):
        game = Game.objects.filter(id = idGame).first()
        idUser = request.data['id_player2']

        if not utils.check_game(idGame):
            return Response("That game does not exist", status=status.HTTP_400_BAD_REQUEST)

        if not utils.check_player(idUser):
            return Response("That user is not registered", status=status.HTTP_400_BAD_REQUEST)

        serializer = GameSerializer(game, data=request.data, partial=True)
        
        if not game or not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not utils.waiting_player_to_game(game, idUser):
            return Response("The game is already full of players", status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, idGame):
        game = Game.objects.filter(id = idGame).first()
        serializer = GameSerializer(game, data=request.data, partial=True)
        new_board = request.data['board']
        id_player = int(request.data['id_player'])
        
        new_request = {"id_player": id_player, "board": new_board}
        
        if not game or not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not utils.user_in_game_and_his_turn(id_player, game): 
            return Response("It's not that player's turn.", status=status.HTTP_400_BAD_REQUEST)
        
        if not utils.allowed_movement(game, new_board):
            return Response("That movement is not allowed", status=status.HTTP_400_BAD_REQUEST)

        if utils.game_finished(new_board):
            new_request['winner'] = game.turn if utils.check_tie(new_board)==False else -1
            utils.update_stats_players(game.turn, game.id_player2 if game.turn == game.id_player1 else game.id_player1, utils.check_tie(new_board))
            utils.delete_game_in_users(game.id, game.id_player1, game.id_player2)

        new_request['turn'] = utils.update_turn(game)
        
        serializer = GameSerializer(game, data=new_request, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,idGame):
        game = Game.objects.filter(id = idGame).first()
        serializer = GameSerializer(game)
        if (game):
            print(f"Game {game.id} deleted")
            utils.delete_game_in_users(game.id, game.id_player1, game.id_player2)
            game.delete()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

