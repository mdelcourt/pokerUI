from random import shuffle

personnes=["David","Remi","Martin", "Amedee","Fredo","Thomas","JE","Lopta"]

for i in range(1000):
  shuffle(personnes)

print(personnes)
