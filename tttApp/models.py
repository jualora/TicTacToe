from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key = True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    actual_game = models.CharField(max_length= 50, blank=True, default="")
    won_games = models.IntegerField(default=0)
    lost_games = models.IntegerField(default=0)
    tied_games = models.IntegerField(default=0)

class Game(models.Model):
    id = models.AutoField(primary_key = True)
    id_player1 = models.IntegerField()
    id_player2 = models.IntegerField(null=True)
    board = models.CharField(max_length=9, default="000000000")
    turn = models.IntegerField(default=1)
    winner = models.IntegerField(blank=True, null=True)

