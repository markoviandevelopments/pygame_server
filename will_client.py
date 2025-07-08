import socket
import json
import pygame
import select

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2-Player Othello")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)
host = '192.168.1.126'  # Replace with server IP
port = 12345

# Game variables
player_id = None
game_state = None
running = True

try:
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_state and game_state["game_started"] and not game_state["game_over"]:
                if player_id + 1 == game_state["turn"]:
                    mouse_x, mouse_y = event.pos
                    # Convert mouse click to board coordinates
                    row = (mouse_y - 100) // 50
                    col = (mouse_x - 200) // 50
                    if 0 <= row < 8 and 0 <= col < 8:
                        try:
                            client_socket.send(json.dumps({"type": "move", "row": row, "col": col}).encode())
                        except socket.error:
                            print("Server disconnected")
                            running = False

        # Receive game state
        readable, _, _ = select.select([client_socket], [], [], 0)
        if readable:
            try:
                data = client_socket.recv(1024)
                if data:
                    message = json.loads(data.decode())
                    if message["type"] == "assign":
                        player_id = message["player_id"]
                        print(f"Assigned as Player {player_id + 1}")
                    elif message["type"] == "state":
                        game_state = message["state"]
                else:
                    print("Server disconnected")
                    running = False
            except socket.error:
                print("Server disconnected")
                running = False

        # Render game
        screen.fill((0, 128, 0))  # Green background (Othello board style)
        if game_state and game_state["game_started"]:
            # Draw board grid
            for row in range(8):
                for col in range(8):
                    pygame.draw.rect(screen, (0, 0, 0), (200 + col * 50, 100 + row * 50, 50, 50), 1)
                    if game_state["board"][row][col] == 1:
                        pygame.draw.circle(screen, (0, 0, 0), (225 + col * 50, 125 + row * 50), 20)  # Black piece
                    elif game_state["board"][row][col] == 2:
                        pygame.draw.circle(screen, (255, 255, 255), (225 + col * 50, 125 + row * 50), 20)  # White piece

            # Highlight valid moves for current player
            if player_id + 1 == game_state["turn"]:
                valid_moves = get_valid_moves(game_state["board"], player_id + 1)
                for row, col in valid_moves:
                    pygame.draw.circle(screen, (255, 255, 0), (225 + col * 50, 125 + row * 50), 5)  # Yellow dot for valid moves

            # Draw scores
            score_text = font.render(f"Black: {game_state['scores'][0]}  White: {game_state['scores'][1]}", True, (255, 255, 255))
            screen.blit(score_text, (300, 50))

            # Draw turn indicator
            turn_text = font.render(f"{'Your Turn' if player_id + 1 == game_state['turn'] else 'Opponent\'s Turn'} (Player {game_state['turn']})", True, (255, 255, 255))
            screen.blit(turn_text, (200, 520))

            # Draw game over message
            if game_state["game_over"]:
                winner = "Black" if game_state["scores"][0] > game_state["scores"][1] else "White" if game_state["scores"][1] > game_state["scores"][0] else "Tie"
                game_over_text = font.render(f"Game Over! Winner: {winner}", True, (255, 255, 255))
                screen.blit(game_over_text, (250, 560))
        else:
            waiting_text = font.render("Waiting for other player...", True, (255, 255, 255))
            screen.blit(waiting_text, (250, 300))

        pygame.display.flip()
        clock.tick(60)

except ConnectionRefusedError:
    print("Error: Server is not running or connection was refused")
except KeyboardInterrupt:
    print("\nDisconnecting from server...")
finally:
    client_socket.close()
    pygame.quit()