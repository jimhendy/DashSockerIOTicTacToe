from collections import defaultdict
from enum import Enum
import uuid

from flask import Flask, request
from flask_socketio import SocketIO
from flask_socketio import emit as socketio_emit
from flask_socketio import join_room, leave_room
from loguru import logger

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:8050")


USER_TO_ROOM = {}
GAMES = []


_SOCKETIO_EVENT = "ws-event"


def emit(event: str, data: dict, **kwargs) -> None:
    logger.info(f"Sending {data=} to {event=}")
    socketio_emit(_SOCKETIO_EVENT, {event: data}, **kwargs)


@socketio.on("connect")
def handle_connect():
    sid = request.sid
    logger.info(f"Client connected with sid {sid}")


@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    room = USER_TO_ROOM.pop(sid, None)
    if room:
        leave_room(room, sid=sid)
        logger.info(f"User {sid} disconnected")
    else:
        logger.info(f"Unkown user with sid {sid} disconnected")
        


@socketio.on("available_rooms")
def handle_available_rooms():
    logger.debug("available_rooms triggered")
    emit("available_rooms", {"rooms": GAMES})
    
@socketio.on("request_create_game")
def handle_request_create_game():
    logger.debug("request_create_game triggered")
    game_id = uuid.uuid4().hex
    room = f"game-{game_id}"
    GAMES.append(room)
    handle_available_rooms()
    
@socketio.on("delete_game")
def handle_delete_game(data):
    logger.debug(f"delete_game triggered with {data=}")
    room = data["game"]
    GAMES.remove(room)
    handle_available_rooms()
    
@socketio.on("join_game")
def handle_join_game(data):
    logger.debug(f"join_game triggered with {data=}")
    room = data["game"]
    sid = request.sid
    USER_TO_ROOM[sid] = room
    
    join_room(room, sid=sid)
    emit("user_joined_game", {"game": room, "sid": sid}, room=room)

if __name__ == "__main__":
    socketio.run(app)