from tkinter import * # This line imports everything from Tkinter library,
                      
import random         # This imports the 'random' module, which we'll use to shuffle the questions
                

# --- Quiz Data Setup ---

#all the questions are here 
#more questions can be added the questios with options in the questions section and the answer to the question in the ams section
question = {
    "Father of the Nation": ['Sonia Gandhi', 'Mahatama Gandhi', 'Bose', 'Jawhar Lal Nehru'],
    "Capital of India": ['Delhi', 'Mumbai', 'Calcutta', 'Bihar'],
    "Who owns Facebook": ['Mark Zukerberg', 'Pricilia Chan', 'Edward', 'Shawn'],
    "What is the largest planet in our solar system?": ['Mars', 'Jupiter', 'Earth', 'Venus'],
    "Which is the longest river in the world?": ['Amazon River', 'Nile River', 'Yangtze River', 'Mississippi River'],
    "How many continents are there in the world?": ['5', '6', '7', '8'],
    "What is the chemical symbol for water?": ['O2', 'H2O', 'CO2', 'N2'],
    "Which animal is known as the 'Ship of the Desert'?": ['Lion', 'Camel', 'Tiger', 'Horse'],
    "What is the capital of Japan?": ['Seoul', 'Beijing', 'Tokyo', 'Bangkok'],
    "Which one is the closest plantet to sun?":["Mercury","Venus","Earth", "Mars"]
}

# it contains the answer to the above questions 
ans = ['Mahatama Gandhi', 'Delhi', 'Mark Zukerberg', 'Jupiter', 'Nile River', '7', 'H2O', 'Camel', 'Tokyo', 'Mercury']

# --- Global Variables for Quiz State ---

to_attempt = 0      # Number of questions user wants to answer .
quiz_data = []      
current_question = 0 # current  index in 'quiz_data').


# --- Quiz Game Functions ---

def start_quiz():
    """
    This function gets called when the 'Start Quiz' button is pressed.
    It sets up the quiz based on the user's input for the number of questions,
    hides the initial setup elements, and then displays the first question.
    """
    global to_attempt         #all set to global here 
    global quiz_data          
    global current_question   
    global user_score_var     

    # 1. Get user input for number of questions:
    try:
        # Try to convert the text from the input box ('num_questions_entry') into an integer (a whole number).
        requested_num = int(num_questions_entry.get())
        # Check if the number is permissible or not 
        if not (1 <= requested_num <= len(question)):
            # If invalid it will raise an error
            raise ValueError("Invalid number of questions")
        to_attempt = requested_num # If valid
    except ValueError:
        # If the user enter not a number
        # error message if not a number is entered 
        error_label.config(text=f"Please enter a number between 1 and {len(question)}.", fg='red')
        return # Stop the function here if there's an error, don't start the quiz.

    error_label.config(text="") # Clear any previous error message once input is valid.

    # 2. Prepare the quiz questions:
    all_quiz_items = [] # Create an empty list to hold our combined question-answer pairs.
    keys = list(question.keys()) # Get a list of all question texts 

    # Loop through each question and its correct answer to create a complete item.
    for i, q_key in enumerate(keys):
        all_quiz_items.append({
            'question_key': q_key,           # The actual question text.
            'options': question[q_key],      # The list of options for this question.
            'correct_answer': ans[i]         # The correct answer from our 'ans' list.
        })

    random.shuffle(all_quiz_items) # Mix up the order of all the question items randomly!
    quiz_data = all_quiz_items[:to_attempt] # Select only the number of questions the user requested.

    # 3. Reset quiz state for a new game:
    current_question = 0     # Start from the first question (index 0).
    user_score_var.set(0)    # Set the user's score back to zero.

    # 4. Hide initial setup elements:
    # Using .forget() to remove these widgets from the window so they are no longer visible.
    num_questions_label.forget()
    num_questions_entry.forget()
    error_label.forget()
    start_button.forget()

    # 5. Show the 'Next Question' button and start the quiz:
    next_button.pack(pady=15) # Make the 'Next Question' button visible.
    next_question()           # Call 'next_question' to display the very first question.

def next_question():
    """
    This function is invoked when next quuestion is pressed 
    It first check the answer to the previous question and clears the screen, and displays next question and option. 
    If all questions are attempted then display the final score.
    """
    global current_question # declaring it to global 

    # Check if there are still questions left to display in our 'quiz_data' list.
    if current_question < to_attempt:
       
        if current_question > 0:
            check_ans() # Call the function to check if the last answer was correct.

        user_ans.set('None') # Reset the user's selection for the new question (no option chosen yet).

        # Get the data for the current question we are about to display.
        current_q_data = quiz_data[current_question]
        c_question_text = current_q_data['question_key']     # The question text.
        c_question_options = current_q_data['options']       # The list of options.

        clear_frame() # Remove all existing widgets (previous question and options) from the display area.

        # Create and display the question label.
        Label(f1, text=f"Question {current_question + 1}/{to_attempt}: {c_question_text}",
              font=('Helvetica', 16, 'bold'), # Name of the font it can be changed ,have to look on the tkinter supported fonts 
              fg='darkblue',                   # Dark blue text color.
              bg='white',                      # White background for the label.
              padx=15,                         # Padding around the text.
              pady=10).pack(anchor=NW)         # Place it at the North-West (top-left) corner.

        # Create and display Radiobuttons for each option.
        for option in c_question_options:
            Radiobutton(f1, text=option, variable=user_ans, # 'user_ans' will store the value of the selected button.
                        value=option,                       # When this button is selected, its 'value' (the option text)
                                                            # will be stored in 'user_ans'.
                        font=('Helvetica', 13),
                        bg='white',
                        fg='black',
                        activebackground='lightblue',       # Color when the mouse is over it.
                        activeforeground='black',
                        selectcolor='lightgreen',           # Color of the radio button's dot when selected.
                        padx=28,
                        pady=5).pack(anchor=NW)

        current_question += 1 # Move our tracker to the next question's index for the next call.
    else:
        # --- Quiz End ---
        # If 'current_question' is no longer less than 'to_attempt', it means we've shown all questions.
        next_button.forget() # Hide the 'Next Question' button as the quiz is over.
        check_ans()          # Check the answer for the *very last* question before ending.

        clear_frame() # Clear the question frame to show the final results.

        # Display the final score.
        output = f"Your Score: {user_score_var.get()} out of {to_attempt}"
        Label(f1, text=output,
              font=('Helvetica', 25, 'bold'),
              fg='darkgreen',
              bg='white',
              pady=20).pack()

        # Display a thank you message.
        Label(f1, text="Thanks for Participating!",
              font=('Helvetica', 18, 'bold'),
              fg='darkblue',
              bg='white').pack()

def check_ans():
    """
    This function compares the answer the user selected on the screen
    with the correct answer for the question that was just displayed.
    If they match, it adds 1 to the user's score.
    """
    global user_score_var # We need to update the score, so we access this global Tkinter variable.
    temp_ans = user_ans.get() # Get the text value of the radio button the user selected.


    correct_answer_for_prev_q = quiz_data[current_question - 1]['correct_answer']

    # Check if the user actually selected an option (not 'None') AND if it matches the correct answer.
    if temp_ans != 'None' and temp_ans == correct_answer_for_prev_q:
        user_score_var.set(user_score_var.get() + 1) # If correct, increase the score by 1.

def clear_frame():
    """
    This is a helper function that removes (destroys) all the widgets
    (like labels, radio buttons) that are currently inside our 'f1' frame.
    We use this to "clear the screen" before putting new questions or the final score on it.
    """
    for widget in f1.winfo_children(): # Loop through every widget that is a child of 'f1'.
        widget.destroy()               # Remove (destroy) that widget from the window.

# --- Main Program Execution Start ---

# This block ensures that the following code only runs when this script is executed directly
# (not when it's imported as a module into another Python script).
if __name__ == "__main__":
    root = Tk() # This line creates the main window of our application. It's the base of our GUI.

    # 1. Setup basic window properties:
    root.title("The Quiz App") # Sets the title text that appears on the window's top bar.
    root.geometry("850x580")      # Sets the initial size of the window (width x height in pixels).
    root.minsize(800, 450)        # Sets the minimum size the window can be resized to.
    root.configure(bg='#E0F2F7')  # Sets the background color of the main window to a light blue.

    # 2. Tkinter variables for user interaction:
    user_ans = StringVar() # A special Tkinter variable to hold the string value of the user's selected answer.
    user_ans.set('None')   # Default value: 'None' means no option has been selected yet.

    user_score_var = IntVar() # A special Tkinter variable to hold the user's score as an integer.
    user_score_var.set(0)     # Initialize the score to 0.

    # 3. Header Label:
    Label(root, text="Quiz Challenge!", # Displays the main title of the quiz app.
          font=('Helvetica', 48, 'bold'), # Big, bold font.
          relief=FLAT,                     # No visible border (flat look).
          background="#2196F3",            # A bright blue background for the header.
          foreground="white",              # White text color.
          padx=20, pady=20).pack(fill=X, pady=(20,10)) # Pack it at the top, fill horizontally, with padding.

    # 4. Input widgets for number of questions:
    num_questions_label = Label(root, text=f"How many questions you want to attempt (1-{len(question)})?",
                                font=('Helvetica', 14),
                                bg="#7199B9", # A slightly darker blue for this label.
                                fg='darkblue')
    num_questions_label.pack(pady=10) # Display the label with some vertical padding.

    num_questions_entry = Entry(root, width=5, font=('Helvetica', 14), justify='center') # An input box for the user.
    num_questions_entry.insert(0, len(question)) # Puts the total number of questions as a default value in the box.
    num_questions_entry.pack(pady=5)

    error_label = Label(root, text="", font=('Helvetica', 12, 'italic'), bg='#E0F2F7') # A label to show error messages.
    error_label.pack(pady=5) # Initially empty, will show text if user enters bad input.

    # 5. Start Button:
    start_button = Button(root,
                          text="Start Quiz",    # Text displayed on the button.
                          command=start_quiz,   # When clicked, this button will call the 'start_quiz' function.
                          font=('Helvetica', 20, 'bold'),
                          bg='limegreen',       # Green background.
                          fg='white',           # White text.
                          activebackground='green', # Darker green when pressed.
                          activeforeground='white',
                          relief=GROOVE,        # Gives it a slightly raised, grooved look.
                          padx=30, pady=15)
    start_button.pack(pady=20) # Display the button.

    # 6. Frame for questions and options:
    # This 'Frame' widget acts as a container for our questions and answer options.
    # We'll clear and refill this frame for each new question.
    f1 = Frame(root,
               bg='white',           # White background for the question area.
               relief=RIDGE,         # A raised border.
               borderwidth=3,        # Thickness of the border.
               padx=25, pady=25)
    f1.pack(side=TOP, fill=BOTH, expand=True, padx=30, pady=20) # Place it at the top,
                                                              # make it fill available space,
                                                              # and expand with the window.

    # 7. Next Question Button:
    next_button = Button(root,
                         text="Next Question",  # Text for the button.
                         command=next_question, # When clicked, calls the 'next_question' function.
                         font=('Helvetica', 20, 'bold'),
                         bg='dodgerblue',       # Blue background.
                         fg='white',            # White text.
                         activebackground='blue', # Darker blue when pressed.
                         activeforeground='white',
                         relief=GROOVE,
                         padx=30, pady=15)

    # 8. Start the Tkinter event loop:
    root.mainloop() # This line starts the Tkinter application. It listens for events
                    
