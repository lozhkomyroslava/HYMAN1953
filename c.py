import random
import time

# Constants
SHAPE_DIAMOND = "diamond"
SHAPE_RECTANGLE = "rectangle"
FILLING_2_CIRCLES = 2
FILLING_3_CIRCLES = 3

RESPONSE_LEFT = "left"
RESPONSE_RIGHT = "right"

# Function to display an imperative stimulus and get participant's response
def present_stimulus(imperative_stimulus):
    print("Imperative stimulus:", imperative_stimulus)
    response = input("Enter response (left or right): ")
    return response.lower()

# Function to provide feedback for incorrect responses
def provide_feedback():
    print("That was the wrong key. Time is up.")

# Function to perform a block of trials
def perform_block(num_trials):
    for _ in range(num_trials):
        imperative_stimulus = random.choice([
            (SHAPE_DIAMOND, FILLING_2_CIRCLES),
            (SHAPE_DIAMOND, FILLING_3_CIRCLES),
            (SHAPE_RECTANGLE, FILLING_2_CIRCLES),
            (SHAPE_RECTANGLE, FILLING_3_CIRCLES)
        ])
        shape, filling = imperative_stimulus

        # Determine the correct response based on the task
        if random.random() < 0.5:
            task = "shape"
            correct_response = RESPONSE_LEFT if shape == SHAPE_DIAMOND else RESPONSE_RIGHT
        else:
            task = "filling"
            correct_response = RESPONSE_LEFT if filling == FILLING_2_CIRCLES else RESPONSE_RIGHT

        # Present the stimulus and collect the response
        response = present_stimulus(imperative_stimulus)

        # Check if the response is correct and provide feedback if necessary
        if response == correct_response:
            print("Correct!")
        else:
            provide_feedback()

        time.sleep(0.5)  # Pause between trials

# Main function
def main():
    # Training phase
    print("Training phase:")
    perform_block(40)

    # Experimental phase
    print("Experimental phase:")
    perform_block(192)

# Run the main function
if __name__ == "__main__":
    main()