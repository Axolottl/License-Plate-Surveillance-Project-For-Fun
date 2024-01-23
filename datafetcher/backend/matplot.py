import matplotlib.pyplot as plt

army_a_soldiers = 56
army_b_soldiers = 87
kill_rate_a = 3  # Highly skilled soldiers kill 3 people on average
kill_rate_b = 1  # Normal mercenaries kill 1 person each

rounds = 10  # Number of battle rounds

remaining_a = [army_a_soldiers]
remaining_b = [army_b_soldiers]

for round in range(1, rounds + 1):
    losses_a = army_a_soldiers * kill_rate_a
    losses_b = army_b_soldiers * kill_rate_b

    army_a_soldiers -= losses_a
    army_b_soldiers -= losses_b

    remaining_a.append(army_a_soldiers)
    remaining_b.append(army_b_soldiers)

# Plotting the graph
plt.plot(range(rounds + 1), remaining_a, label='Highly Skilled Army')
plt.plot(range(rounds + 1), remaining_b, label='Normal Mercenaries')
plt.xlabel('Rounds')
plt.ylabel('Remaining Soldiers')
plt.legend()
plt.title('Battle Losses Over Rounds')
plt.show()
