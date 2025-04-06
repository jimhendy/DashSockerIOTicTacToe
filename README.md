# Pure Python Online Multiplayer Version of Tic-Tac-Toe

## Design

The backend and frontend run as separate concerns.

### Backend

A FastAPI server is used to handle the game logic and state. The server is responsible for:
- Listing available games
- Creating new games
- Joining games
- Making moves
- Ending games

As the whole communication is done via websockets, the server is also responsible for broadcasting game state changes to all players in a game.
We use cookies to store the player's current game, allowing them to reconnect to the game if they lose connection.
The game state is serialised to pickle files to allow for persistence across server restarts.

### Frontend

A Python dash application with our custom dash-socketio component is used to handle the user interface.
The frontend is responsible for:
- Displaying the game board
- Displaying the game state
- Displaying the list of available games
- Allowing the player to join a game
- Allowing the player to make moves

The frontend communicates with the backend via websockets, using the dash-socketio component to handle the communication.
# DashSockerIOTicTacToe
