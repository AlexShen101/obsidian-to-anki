# match to signal the end of the question secdtion
termination_line = "- Sources:"

input_files = []

# answer type will affect the behaviour of the add_question_object()
# code: in code mode, will not check for anything
current_answer_type = ""

# line type will affect the behaviour of the main file as it is looking for questions
# code: ignores any questions inside the code block
current_line_type = ""