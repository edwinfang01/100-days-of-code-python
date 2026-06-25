import turtle
import pandas
from pathlib import Path

screen = turtle.Screen()
tim = turtle.Turtle()
screen.title("U.S States Game")
base_path = Path(__file__).parent
image = str(base_path / "blank_states_img.gif")
screen.addshape(image)
turtle.shape(image)
data = pandas.read_csv(base_path / "50_states.csv")
all_states = data.state.tolist()

states_guessed_correctly = []
tim.ht()

while len(states_guessed_correctly) < 50:
    answer_state = screen.textinput(title=f"{len(states_guessed_correctly)}/50 States Correct",
                                    prompt="What's another state's name").title().strip()

    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in states_guessed_correctly]
        # for state in all_states:
        #     if state not in states_guessed_correctly:
        #         missing_states.append(state)
        pandas.DataFrame(missing_states).to_csv(base_path / 'missing states.csv')
        break

    state_found = data.get(data['state'] == answer_state)
    if not (state_found.empty or answer_state in states_guessed_correctly):
        states_guessed_correctly.append(answer_state)
        tim.teleport(state_found.x.item(), state_found.y.item())
        tim.write(answer_state)