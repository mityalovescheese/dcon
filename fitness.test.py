import fitness
import random
from gen import Initialization

# testing code
fit = fitness.Fitness()


print("bool result   - fitness function")
result = fit.fitness(10, "6+9-\\\\\\\")
print(result)

print("---------------------------------------")

print("string result - equation solver function")
equ_solver = fit.solve_equation("6+7+4-2-7+1-")
print(equ_solver)
