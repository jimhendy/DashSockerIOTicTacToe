from dash import Dash, Input, Output, dcc, html, State, MATCH, callback_context, ALL
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_socketio import DashSocketIO

from typing import Any
import uuid
import re
from loguru import logger


def websocket_request(
    event: str,
    data: Any = None,
):
    """
    Simple helper function to create a websocket request.

    This is required because we need to alter the "send" property of the
    DashSocketIO component so we had a uuid to each request.
    Otherwise, if we requested two identical events in a row, the second
    request would be ignored.

    :param event: The event to send
    :param data: The data to send with the event. Defaults to None. Usually a dict.
    :return: A dictionary with the event, data, and a uuid.
    """
    return {
        "event": event,
        "data": data,
        "id": str(uuid.uuid4()),
    }


def _str_dict_key(str_dict: str, key: str) -> Any:
    """
    Take in a str which is a dict and return the value of the requested key.

    Handles both single ('') and double ("") quoted keys and values.
    """
    pattern = re.compile(rf"[\"']{key}[\"']:\s*[\"'](.+?)[\"']")
    match = pattern.search(str_dict)
    if match:
        return match.group(1)
    else:
        return None


def _str_index_in_list(
    str_dict: str, items: list[dict], key: str = "index"
) -> int | None:
    """
    Take in a list of dicts and a str which is a dict and return the index of the dict in the list.

    E.g.

    items = [{"index": 1}, {"index": 2}, {"index": 3}], str_dict = "{'index': 2}", key = "index" -> 1

    items = [{"index": 1}, {"index": 2}, {"index": 3}], str_dict = "{'index': 10}", key = "index" -> -1
    """
    logger.warning(f"{str_dict=}")
    logger.warning(f"{items=}")
    value = _str_dict_key(str_dict, key)
    logger.debug(f"{value=}")
    not_found_value = None
    if value is not None:
        return next(
            (i for i, item in enumerate(items) if item[key] == value), not_found_value
        )
    else:
        return not_found_value


app = Dash(__name__)

app.layout = html.Div(
    children=[
        # html.Div(id="dummy-output", style={"display": "none"}),
        DashSocketIO(
            id="websocket",
            url="ws://localhost:5000",
        ),
        html.Div(
            style={
                "display": "flex",
                "justify-content": "center",
                "flexDirection": "row",
                "alignItems": "center",
            },
            children=[
                html.Div(
                    children=[
                        html.H1("Available Games"),
                        html.Div(id="available_games"),
                    ],
                ),
                html.Div(
                    id="create-game-container",
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                    },
                    children=[
                        html.Button(
                            id="create-game-button",
                            children="Create Game",
                        )
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("websocket", "send", allow_duplicate=True),
    Input("websocket", "id"),
    prevent_initial_call="initial",
)
def initial_socket_request(id):
    return websocket_request(
        event="available_rooms",
    )


@app.callback(
    Output("websocket", "send", allow_duplicate=True),
    Input("create-game-button", "n_clicks"),
    prevent_initial_call=True,
)
def create_game(n_clicks):
    logger.info(f"create_game triggered with {n_clicks=}")
    return websocket_request(
        event="request_create_game",
    )


@app.callback(
    Output("websocket", "send", allow_duplicate=True),
    Input({"type": "delete-game", "index": ALL}, "n_clicks"),
    Input({"type": "delete-game", "index": ALL}, "id"),
    prevent_initial_call=True,
)
def delete_game(n_clicks_list: list[int], delete_button_ids: list[str]):
    ctx = callback_context

    if len(ctx.triggered) != 1:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    calling_index = _str_index_in_list(trigger_id, delete_button_ids)
    logger.info(f"{trigger_id=} {calling_index=}")
    n_clicks = n_clicks_list[calling_index]
    logger.info(f"{n_clicks=}")

    if not n_clicks:
        raise PreventUpdate

    logger.info(f"delete_game triggered with {n_clicks=} by {ctx.triggered}")
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    game = _str_dict_key(button_id, "index")
    return websocket_request(event="delete_game", data={"game": game})


@app.callback(
    Output("available_games", "children"),
    Input("websocket", "data-available_rooms"),
    prevent_initial_call=True,
)
def update_available_games(response):
    games = response["rooms"]
    return html.Ul(
        children=[
            html.Li(
                [
                    html.H5(game),
                    html.Button(
                        id={"type": "delete-game", "index": game},
                        children="Delete Game",
                        n_clicks=0,
                    ),
                ]
            )
            for game in games
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=False)
