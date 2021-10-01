secret_word = "giraffe"
guess = ""
tries = 0
guess_limit = 3

print("Guest de secret word: g----f-")

while guess != secret_word and tries < guess_limit: 
    guess = input("enter guess: ")
    if guess != secret_word and tries < guess_limit:
        tries = tries + 1

if tries > tries:
    print("you lost!!!")
else:
    print("you win!!!")