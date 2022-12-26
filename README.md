# TicTacToe
Tic Tac Toe game implemented in Django Rest Framework for the Backend and with terminal and Python for the client.

## Building 

If you want to deploy the app on localhost, then:

Install the dependencies.
```
pip install -r requirements.txt
```
Then, run the server.
```
python manage.py runserver
```
Finally, start the client.
```
python CLI/tttCLI.py
```

## Deployment

The app is deployed on render.com via gunicorn and whitenoise. The webpage is https://tictactoe-dlgy.onrender.com/ (you must add API calls to that address for the request to work)
