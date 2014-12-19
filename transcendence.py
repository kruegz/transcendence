import sys
import re
import os

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# Get the unimporant words file
unimportant_words_file = open("unimportant_words.txt", "r")
unimportant_words = unimportant_words_file.read()
unimportant_words = unimportant_words.split(" ")
unimportant_words_file.close()

# Get the answers file
answers_file = open("answers.txt", "r")
raw_answers = answers_file.read()
answers_file.close()

# Format the answers file
q_a_list = re.split("\n| ", raw_answers)
q_a_list = q_a_list[:-1]
length = len(q_a_list) // 2
db_questions = []
db_answers = []

for x in range(length):
	question = q_a_list[x * 2]
	db_questions.append(question)
	answer = q_a_list[x * 2 + 1]
	db_answers.append(answer)

if len(sys.argv) == 1:									# Regular mode
	# Get the question
	question = input("Question: ")

	# Format the question
	if question.endswith("?"):
		question = question[:-1]
	question = question.lower()
	question_list = question.split(" ")

	# Get rid of the unimportant words
	for word_key in range(len(question_list)):
		if question_list[word_key] in unimportant_words:
			question_list[word_key] = " "

	while " " in question_list:
		question_list.remove(" ")

	question = ",".join(question_list)

	# Check to see if the question has a possible answer
	have_answer = False
	possible_answers = {}

	for key in range(len(db_questions)):
		score = 0
		db_question_words = db_questions[key].split(",")
		
		for word in question_list:
			if word in db_question_words:
				score += 1

		if score > 0:
			possible_answers[key] = score

	answer_key = -1
	answer_score = 0

	for key, score in possible_answers.items():
		if score > answer_score:
			have_answer = True
			answer_score = score
			answer_key = key

	if have_answer:
		# Get the answer key and print the answer
		answer = db_answers[answer_key]
		answer = answer.split(",")
		answer = " ".join(answer)
		print(answer)

		# Ask if it was right
		right = input("Was I right? (y/n): ")

		if right == "n":
			# Get the correct answer
			correct_answer = input("I'm sorry. Mind telling me the right answer?: ")

			# Format the correct answer
			correct_answer = correct_answer.lower()
			correct_answer_list = correct_answer.split(" ")

			# Put in database form
			answer_words = ",".join(correct_answer_list)
			question_answer = question + " " + answer_words

			# Check to see if that exact question is in the database
			if question in db_questions:
				# If it is, delete that question/answer combo from the database
				answers_file = open("answers.txt", "r")
				answers_lines = answers_file.readlines()
				answers_file.close()
				answers_file = open("answers.txt", "w")
				answers_file.write("")
				answers_file.close()
				answers_file = open("answers.txt", "a")
				
				for line in answers_lines:
					wrong_question_answer = question + " " + answer + "\n"
					if line != wrong_question_answer:
						answers_file.write(line)

				# Add to the database
				answers_file.write(question_answer + "\n")
				answers_file.close()
			else:
				# Add to the database
				answers_file = open("answers.txt", "a")
				answers_file.write(question_answer + "\n")
				answers_file.close()

			# Ask if the user has another question
			again = input("Have another question? (y/n): ")
			
			if again == "y":
				# Restart the program
				restart_program()
		elif right == "y":
			print("Awesome!")

			# Ask if the user has another question
			again = input("Have another question? (y/n): ")
			
			if again == "y":
				# Restart the program
				restart_program()

	else:
		# Get the answer
		answer = input("I'm not sure. Mind telling me?: ")

		# Format the answer
		answer = answer.lower()
		answer_list = answer.split(" ")

		# Put in database form
		answer_words = ",".join(answer_list)
		question_answer = question + " " + answer_words

		# Add to the database
		answers_file = open("answers.txt", "a")
		answers_file.write(question_answer + "\n")
		answers_file.close()

		# Ask if the user has another question
		again = input("Thanks! Have another question? (y/n): ")
		
		if again == "y":
			# Restart the program
			restart_program()
