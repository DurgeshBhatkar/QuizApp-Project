# https://opentdb.com/api.php?amount=1
import requests
import json
import html
import random


def call_api(api):
  return requests.get(api)


def shuffle_options(optionList):
  random.shuffle(optionList)
  finalList = [html.unescape(option) for option in optionList]
  return finalList


def storeFile(question, optionList, answer):
  questionDB = {
    'question': question,
    'optionList': optionList,
    'answer': answer
  }
  with open("Question_database.txt", "a") as file:
    file.write(str(questionDB))
    file.write("\n")


stopFlag = True
score = 0
looserCount = 0
print("-----Welcome to the Quiz Game-----")
print(f"Your current score is {score}")
print("----------------------------------")
while stopFlag:
  apiCall = call_api("https://opentdb.com/api.php?amount=1")
  if apiCall.status_code == 200:
    apiText = apiCall.text
    # Method -1 to convert the string object into dictionary which is coming from response
    apiDict = json.loads(apiText)
    apiResult = apiDict["results"]
    data = apiResult[0]
    '''
    We are passing the question key from the data variable to the html.unescape() because we want to process html entities in human readable form 
     E.g.=>
     1. Original string is 
     => temp=In &quot;Team Fortress 2&quot;, the &quot;Bill&#039;s Hat&quot; is a reference to the game &quot;Dota 2&quot;.'
     2. After passing it into the html.unescape() as html.unescape(temp) we will get following string
     => In "Team Fortress 2", the "Bill's Hat" is a reference to the game "Dota 2".
    '''
    question = html.unescape(data['question'])
    answer = data['correct_answer']
    incorrectAnswer = data['incorrect_answers']
    incorrectAnswer.append(answer)
    optionList = shuffle_options(incorrectAnswer)
    print(f"Q. {question}")
    for index, option in enumerate(optionList):
      print(f"{index+1}) {option}")
    userChoice = int(input("Enter your choice: "))
    if optionList[userChoice - 1] == answer:
      print("Yess! You are right")
      score += 1
      print("-------------------")
    else:
      print("Better luck next time!")
      looserCount += 1
      if looserCount >= 10:
        stopFlag = False
      print("----------------------")
    print(f"Your score is {score}")
    print("--------------------")

    storeFile(question, optionList, answer)
  else:
    print("Error occured while API calling")

else:
  print(f"Your final score is {score} ")
