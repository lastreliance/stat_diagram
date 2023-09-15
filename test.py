import random
from diagram import Diagram


diagram_ = Diagram(name="lottery", slow_mo=True)
people = list()

for p in range(100):
    value = 100
    max_val = 0
    max_point = 0
    for i in range(100):
        if random.random() > 0.5:
            value *= 1.8
        else:
            value *= 0.5
        if max_val < value:
            max_val = value
            max_point = i

    people.append(max_val)

    diagram_.add(max_point)
print(sum(people) / 100)
diagram_.display()
diagram_.window.mainloop()
