import socket
import json
import select

# Initialize 8x8 Othello board: 0=empty, 1=black (Player 1), 2=white (Player 2)
board = [[0] * 8 for _ in range(8)]
board[3][3] = board[4][4] = 2  # White
board[3][4] = board[4][3] = 1  # Black

# Game state
game_state = {
    "board": board,
    "turn": 1,  # 1 for Player 1 (black), 2 for Player 2 (white)
    "scores": [2, 2],  # Black, White
    "game_started": False,
    "game_over": False
}

def get_valid_moves(board, player):
    """Return list of valid moves [(row, col), ...] for the player."""
    valid_moves = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    opponent = 2 if player == 1 else 1

    for row in range(8):
        for col in range(8):
            if board[row][col] != 0:
                continue
            for dr, dc in directions:
                r, c = row + dr, col + dc
                to_flip = []
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                    to_flip.append((r, c))
                    r += dr
                    c += dc
                if to_flip and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    valid_moves.append((row, col))
                    break
    return valid_moves

def apply_move(board, row, col, player):
    """Apply a move, flip pieces, and return updated board."""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    opponent = 2 if player == 1 else 1
    board[row][col] = player
    for dr, dc in directions:
        r, c = row + dr, col + dc
        to_flip = []
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc
        if to_flip and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for fr, fc in to_flip:
                board[fr][fc] = player

def count_scores(board):
    """Count pieces for each player."""
    black = sum(row.count(1) for row in board)
    white = sum(row.count(2) for row in board)
    return [black, white]

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '0.0.0.0'
port = 12345
server_socket.bind((host, port))
server_socket.listen(2)
server_socket.setblocking(False)
print(f"Server listening on {host}:{port}")

clients = []
player_ids = {}  # Map client socket to player ID (0 or 1)

try:
    while True:
        readable, _, _ = select.select([server_socket] + clients, [], [], 0.016)

        for sock in readable:
            if sock is server_socket:
                if len(clients) < 2:
                    client_socket, client_address = server_socket.accept()
                    client_socket.setblocking(False)
                    clients.append(client_socket)
                    player_id = len(clients) - 1
                    player_ids[client_socket] = player_id
                    print(f"Player {player_id + 1} connected from {client_address}")
                    client_socket.send(json.dumps({"type": "assign", "player_id": player_id}).encode())
                    if len(clients) == 2:
                        game_state["game_started"] = True
                        print("Game started with 2 players!")
                else:
                    client_socket, _ = server_socket.accept()
                    client_socket.close()
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        input_data = json.loads(data.decode())
                        player_id = player_ids[sock]
                        if input_data["type"] == "move" and game_state["turn"] == player_id + 1 and not game_state["game_over"]:
                            row, col = input_data["row"], input_data["col"]
                            if (row, col) in get_valid_moves(game_state["board"], player_id + 1):
                                apply_move(game_state["board"], row, col, player_id + 1)
                                game_state["scores"] = count_scores(game_state["board"])
                                # Switch turn
                                next_player = 2 if player_id == 0 else 1
                                game_state["turn"] = next_player
                                # Check if next player has valid moves
                                if not get_valid_moves(game_state["board"], next_player):
                                    # Try the other player
                                    game_state["turn"] = 1 if next_player == 2 else 2
                                    if not get_valid_moves(game_state["board"], game_state["turn"]):
                                        game_state["game_over"] = True
                    else:
                        print(f"Player {player_ids[sock] + 1} disconnected")
                        clients.remove(sock)
                        del player_ids[sock]
                        sock.close()
                        game_state["game_started"] = False
                        game_state["game_over"] = False
                except socket.error:
                    print(f"Player {player_ids[sock] + 1} disconnected")
                    clients.remove(sock)
                    del player_ids[sock]
                    sock.close()
                    game_state["game_started"] = False
                    game_state["game_over"] = False

        # Broadcast game state
        if game_state["game_started"] and len(clients) == 2:
            for client in clients:
                try:
                    client.send(json.dumps({"type": "state", "state": game_state}).encode())
                except socket.error:
                    print(f"Player {player_ids[client] + 1} disconnected")
                    clients.remove(client)
                    del player_ids[client]
                    client.close()
                    game_state["game_started"] = False
                    game_state["game_over"] = False

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    for client in clients:
        client.close()
    server_socket.close()

    