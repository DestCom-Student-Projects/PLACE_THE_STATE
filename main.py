import pandas as pd
import pygame
import sys
import os

WIDTH, HEIGHT = 1024, 768
CLOCK_TICK = 60
GAME_TIME = 600
SCORE_TO_WIN = 1

csv_path = os.path.join("assets", "50_states.csv")
df = pd.read_csv(csv_path)

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

image_path = os.path.join("assets", "blank_states_img.gif")
map_image = pygame.image.load(image_path)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("State Location Game")

# Set up the font
font = pygame.font.SysFont("arial", 30)
answer = "Type a state name and press ENTER or type ESC to exit"

score = 0
old_score = score
validated_state = []
game_timer = 0
activated_timer = False

display_feedback = False
feedback_text = ""
feedback_color = (0, 0, 0)
validated_counter = 0

if __name__ == "__main__":
    while True:
        clock.tick(CLOCK_TICK)
        if activated_timer:
            game_timer += 1
        elif game_timer == GAME_TIME:
            answer = "You lose! Press ESC to exit"
            break
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_timer == 0:
                    activated_timer = True
                    answer = ""
                if event.key == pygame.K_RETURN:
                    # Check if the text is a state
                    state = answer.title()
                    if state in df["state"].values and state not in validated_state:
                        score += 1
                        feedback_text = "Validé"
                        feedback_color = (0, 255, 0)
                        validated_state.append(state)
                    else:
                        feedback_text = "Non validé"
                        feedback_color = (255, 0, 0)
                        answer = ""
                elif event.key == pygame.K_BACKSPACE:
                    answer =  answer[:-1]
                else:
                    answer += event.unicode
                    
        if(score == SCORE_TO_WIN):
            validated_text = font.render("You win! You found {score} states in {game_timer//60} seconds", True, (0, 0, 0))
            activated_timer = False
        elif(score > old_score) and not display_feedback:
            old_score = score
            validated_text = font.render(feedback_text, True, feedback_color)
            screen.blit(validated_text, (WIDTH // 2 - validated_text.get_width() // 2, HEIGHT // 2 - map_image.get_height() // 2 - 50))
            answer = ""
            display_feedback = True
        elif score == SCORE_TO_WIN and not display_feedback:
            validated_text = font.render("You win! You found {score} states in {game_timer//60} seconds", True, (0, 0, 0))
            activated_timer = False
            screen.blit(validated_text, (WIDTH // 2 - validated_text.get_width() // 2, HEIGHT // 2 - map_image.get_height() // 2 - 50))
            display_feedback = True
        elif not display_feedback:
            old_score = score
            validated_text = font.render(feedback_text, True, feedback_color)
            screen.blit(validated_text, (WIDTH // 2 - validated_text.get_width() // 2, HEIGHT // 2 - map_image.get_height() // 2 - 50))
            display_feedback = True
            
        if display_feedback:
            validated_counter += 1
            validated_text = font.render(feedback_text, True, feedback_color)
            screen.blit(validated_text, (WIDTH // 2 - validated_text.get_width() // 2, HEIGHT // 2 - map_image.get_height() // 2 - 50))
            if validated_counter == 60:
                display_feedback = False
                validated_counter = 0

        answer_surf = font.render(answer, True, (0, 0, 0))
        screen.blit(map_image, (WIDTH // 2 - map_image.get_width() // 2, HEIGHT // 2 - map_image.get_height() // 2))
        screen.blit(answer_surf, (WIDTH // 2 - answer_surf.get_width() // 2, HEIGHT // 2 + map_image.get_height() // 2 + 50))
        
        score_surf = font.render(f"Score: {score}/50", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))
        
        if activated_timer:
            timer_surf = font.render(f"Remaining time: {GAME_TIME - game_timer//60} seconds", True, (0, 0, 0))
            screen.blit(timer_surf, (WIDTH - timer_surf.get_width() - 10, 10))
        
        for validated in validated_state:
            state_data = df[df["state"] == validated]

            center_x_image = (WIDTH // 2 - map_image.get_width() // 2) + map_image.get_width() // 2
            center_y_image = (HEIGHT // 2 - map_image.get_height() // 2) + map_image.get_height() // 2


            state_name = font.render(state_data["state"].values[0], True, (0, 0, 0))
            center_x_text = state_name.get_width() // 2
            center_y_text = state_name.get_height() // 2
            
            coord_x = 0
            coord_y = 0

            if state_data["x"].values[0] < center_x_image:
                coord_x = state_data["x"].values[0]
            else:
                coord_x = -state_data["x"].values[0]
            
            if state_data["y"].values[0] > center_y_image:
                coord_y = state_data["y"].values[0]
            else:
                coord_y = -state_data["y"].values[0]
            
            x = center_x_image + coord_x - center_x_text
            y = center_y_image + coord_y - center_y_text
        
            screen.blit(state_name, (x, y))

        
        # Update the display
        pygame.display.flip()
