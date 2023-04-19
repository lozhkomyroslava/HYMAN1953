import random
import time

# define the function which generates the signals of different complexity
def generate_signal(difficulty):
    if difficulty == "simple":
        return "."
    elif difficulty == "medium":
        return random.choice(["A", "B", "C", "1", "2", "3"])
    elif difficulty == "complex":
        return "".join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", 6))

# define the function which estimate the reaction time in responce to the sicgnal
def measure_reaction_time(signal):
    start_time = time.time()
    # here we could change the code which shozs signal in the screen and wait on the bottom push
    end_time = time.time()
    return end_time - start_time

# generate and estimate reaction time for 10 signals different complexity
for i in range(10):
    difficulty = random.choice(["simple", "medium", "complex"])
    signal = generate_signal(difficulty)
    reaction_time = measure_reaction_time(signal)
    print(f"Signal: {signal}, Difficulty: {difficulty}, Reaction Time: {reaction_time:.3f}s")