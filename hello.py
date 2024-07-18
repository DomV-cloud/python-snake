import random
import numpy as np
import requests

class SnakeGame:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (0, 1)
        self.generate_food()
        self.game_over = False

    def generate_food(self):
        while True:
            self.food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if self.food not in self.snake:
                break

    def step(self, action):
        if action == "UP":
            self.direction = (-1, 0)
        elif action == "DOWN":
            self.direction = (1, 0)
        elif action == "LEFT":
            self.direction = (0, -1)
        elif action == "RIGHT":
            self.direction = (0, 1)

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= self.height or
                new_head[1] < 0 or new_head[1] >= self.width or
                new_head in self.snake):
            self.game_over = True
            return -1  # Game over

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.generate_food()
            return 1  # Ate food
        else:
            self.snake.pop()
            return 0  # Moved without eating

    def get_state(self):
        state = np.zeros((self.height, self.width), dtype=int)
        for segment in self.snake:
            state[segment] = 1
        state[self.food] = 2
        return state

    def render(self):
        state = self.get_state()
        print("\n".join("".join("█" if cell == 1 else "F" if cell == 2 else "." for cell in row) for row in state))

def get_ai_action(state):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": "API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": "Given the current state of the game, what action should the AI take to avoid collision and reach the food?",
        "input": state.tolist(),
        "max_tokens": 1,
        "temperature": 0.5
    }
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()

    if "choices" in response_json:
        action = response_json["choices"][0]["text"]
    else:
        action = "RIGHT"  # Default action if the API fails
    return action

def simulate_game():
    game = SnakeGame()
        
    while not game.game_over:
        game.render()
        state = game.get_state()
        action = get_ai_action(state)
        print(f"AI chooses action: {action}")
        game.step(action)

simulate_game()