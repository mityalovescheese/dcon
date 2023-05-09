import gen

terminal_input = input("enter a number: ")

g = gen.Genetic(int(terminal_input))
print(g.create_model())
