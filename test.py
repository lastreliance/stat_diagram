import random
from diagram import Diagram


diagram_ = Diagram()

value = 100

for i in range(100):
    if random.random() > 0.5:
        value *= 1.8
    else:
        value *= 0.5
    diagram_.add(value)

diagram_.display()
diagram_.window.mainloop()
