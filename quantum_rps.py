"""
Code created by: Jacob Prouty 10/12/2023

This is just a basic assignment to keep programming skills up
and may possibly be used as a teaching tool in the future.
Good for introducing basic concepts in both quantum mechanics
and coding
"""


from qiskit import qiskit, QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
import numpy as np

def print_rules():
    print("Here are the rules of Quantum Rock, Paper, Scissors:")
    print("First, each player will choose rock, paper, or scissors")
    print("Then the two options that the player didn't choose will be placed in an")
    print("equally weighted superposition between them. Finally that superposition")
    print("will be measured and compared with the measured outcome of the other player.")
    print("The game then proceeds as normal Rock, Paper, Scissors. As many rounds of the")
    print("game can be played with that choice until both players are satisfied.\n\n")


p1_name = "p1"
p1_score = 0
p2_name = "p2"
p2_score = 0
ties = 0
rounds = 1
# number of rounds to play
p1_name = input("What's the name of Player 1: ")
p2_name = input("What's the name of Player 2: ")
print_rules()

while True:
    p1_choice = input(p1_name+" choose Rock, Paper, or Scissors to exclude. ")
    p1_choice = p1_choice.lower()
    if p1_choice!='rock' and p1_choice!='paper' and p1_choice!='scissors':
        print("ERROR: invalid input. Try again.")
    else: break
while True:
    p2_choice = input(p2_name+" choose Rock, Paper, or Scissors to exclude. ")
    p2_choice = p2_choice.lower()
    if p2_choice!='rock' and p2_choice!='paper' and p2_choice!='scissors':
        print("ERROR: invalid input. Try again.")
    else: break

keepPlaying = 'y'

while keepPlaying == 'y':
    rounds = int(input("How many rounds would you like to play with your choice: "))
    # Actual quantum simulation BEGINS here:

    qc = QuantumCircuit(6)
    # for binary positions Rock=001, Paper=010, Scissors=100
    # Dealing with positions 0-2 here:
    if p1_choice == 'rock':
        # superposition of |010> + |100>
        qc.h(1)
        qc.x(2)
        qc.cx(1,2)
    if p1_choice == 'paper':
        # superposition of |001> + |100>
        qc.h(0)
        qc.x(2)
        qc.cx(0,2)
    if p1_choice == 'scissors':
        # superposition of |001> + |010>
        qc.h(0)
        qc.x(1)
        qc.cx(0,1)
    # Dealing with positions 3-5 here:
    if p2_choice == 'rock':
        # superposition of |010> + |100>
        qc.h(4)
        qc.x(5)
        qc.cx(4,5)
    if p2_choice == 'paper':
        # superposition of |001> + |100>
        qc.h(3)
        qc.x(5)
        qc.cx(3,5)
    if p2_choice == 'scissors':
        # superposition of |001> + |010>
        qc.h(3)
        qc.x(4)
        qc.cx(3,4)
    qc.measure_all()
    print(qc)

    sim = Aer.get_backend('qasm_simulator')
    result = qiskit.execute(qc, sim, shots=rounds).result()
    counts = result.get_counts(qc)
    print(counts)
    # Only have to deal with interpreting results for counts now.
    # counts is a dictionary where the key is a string, but the
    # values are ints

    resultStates = list(counts.keys())
    for i in range(len(resultStates)):
        if resultStates[i][0:3] == '001':
            # p2 has thrown rock
            if resultStates[i][3:6] == '001':
                # p1 has also thrown rock
                # tie game
                ties += counts[resultStates[i]]
            if resultStates[i][3:6] == '010':
                # p1 has thrown paper
                # p1 wins
                p1_score += counts[resultStates[i]]
            if resultStates[i][3:6] == '100':
                # p1 has thrown scissors
                # p2 wins
                p2_score += counts[resultStates[i]]
        if resultStates[i][0:3] == '010':
            # p2 has thrown paper
            if resultStates[i][3:6] == '001':
                # p1 has thrown rock
                # p2 wins
                p2_score += counts[resultStates[i]]
            if resultStates[i][3:6] == '010':
                # p1 has also thrown paper
                # tie game
                ties += counts[resultStates[i]]
            if resultStates[i][3:6] == '100':
                # p1 has thrown scissors
                # p1 wins
                p1_score+=counts[resultStates[i]]
        if resultStates[i][0:3] == '100':
            # p2 has thrown scissors
            if resultStates[i][3:6] == '001':
                # p1 has thrown rock
                # p1 wins
                p1_score+=counts[resultStates[i]]
            if resultStates[i][3:6] == '010':
                # p1 has thrown paper
                # p2 wins
                p2_score+=counts[resultStates[i]]
            if resultStates[i][3:6] == '100':
                # p1 has also thrown scissors
                # tie game
                ties+=counts[resultStates[i]]

    # print score here:
    print("SCORE:\n", p1_name, ": ", p1_score, "     ", p2_name, ": ", p2_score, "     TIES: ", ties)

    # Quantum simulation ENDS here:
    # check if the players are done here
    keepPlaying = input("Would you like to keep playing (y/n): ")
    keepPlaying.lower()
    if keepPlaying == 'n': break
    keepPlaying = input("Would you like to change your choices (y/n): ")
    keepPlaying.lower()
    if keepPlaying == 'y':
        while True:
            p1_choice = input(p1_name+" choose Rock, Paper, or Scissors to exclude. ")
            p1_choice = p1_choice.lower()
            if p1_choice!='rock' and p1_choice!='paper' and p1_choice!='scissors':
                print("ERROR: invalid input. Try again.")
            else: break
        while True:
            p2_choice = input(p2_name+" choose Rock, Paper, or Scissors to exclude. ")
            p2_choice = p2_choice.lower()
            if p2_choice!='rock' and p2_choice!='paper' and p2_choice!='scissors':
                print("ERROR: invalid input. Try again.")
            else: break

if (ties>p1_score and ties>p2_score) or p1_score==p2_score:
    print("TIE GAME")
if p1_score > p2_score:
    print("CONGRATULATIONS!!! ", p1_name, " won the game.")
else:
    print("CONGRATULATIONS!!! ", p2_name, " won the game." )
print("FINAL SCORE:\n", p1_name, ": ", p1_score, "     ", p2_name, ": ", p2_score, "     TIES: ", ties)