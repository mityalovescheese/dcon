import random
import string
import fitness
import sys
from itertools import chain

sys.setrecursionlimit(10000)

class Initialization:
	def __init__(self):
		self.operations = ["+", "-"]

	def create_root(self):
		result = []
		for i in range(6):
			result.append(random.choice(string.digits))
			result.append(random.choice(self.operations))
		return "".join(result)

class Genetic(Initialization):
	def __init__(self, desired_result):
		self.init = Initialization()
		self.init.__init__()

		self.answer = ""
		self.solution_reached = False
		self.fit = fitness.Fitness()
		self.desired_result = desired_result

		self.reproduction_combinations = ["parallel", "skip", "in_out"]
		self.current_reproduction_type = ""
		self.model = [ ]
		[self.model.append([self.init.create_root()]) for i in range(100000)] # simulating this type -> vector<pair<bool, vector<string> > >

		# child mutations/logic
	def _mutate_child_node(self, arg):
		all_possible_mutations = list(chain(string.digits, self.init.operations))
		all_possible_mutations.append("del")
		prereturn_string_buffer = []

		del_char = False
		rand_mutation = random.choice(all_possible_mutations)

		random_index = random.randint(0, len(arg)-1)
		if rand_mutation == "del":
			for i in range(len(arg)):
				if i == random_index:
					prereturn_string_buffer.append("")
				else:
					prereturn_string_buffer.append(arg[i])
     
		for i in range(len(arg)):
			if i == random_index and rand_mutation != "del":
				prereturn_string_buffer.append(rand_mutation)
			else:
				prereturn_string_buffer.append(arg[i])
		return "".join(prereturn_string_buffer)

	def _weave(self, str1, str2):
		result_string = "".join(i for j in zip(str2, str1) for i in j)
		return result_string

	def _birth_mutated_child_nodes(self, i, amount_to_subtract):
		# i                  -> the variable for the iterator
		# amount_to_subtract -> the amount to... subtract.
		first_child_first   = "".join(str(self.first_half(i)) + str(self.second_half(i-amount_to_subtract)))
		first_child_second  = "".join(str(self.second_half(i)) + str(self.second_half(i-amount_to_subtract)))
		second_child_first  = "".join(str(self.first_half(i)) + str(self.first_half(i-amount_to_subtract)))
		second_child_second = "".join(str(self.first_half(i-amount_to_subtract)) + str(self.second_half(i)))

		# mutating children
		first  = "".join(self._mutate_child_node(first_child_first))
		second = "".join(self._mutate_child_node(first_child_second))
		third  = "".join(self._mutate_child_node(second_child_first))
		fourth = "".join(self._mutate_child_node(second_child_second))

		sibling_nodes = [repr(first), repr(second), repr(third), repr(fourth)]

		return sibling_nodes

	def _test_node_fitness(self, four_node_list): # four nodes in four_node_list
		tested_nodes = []
		for i, c in enumerate(four_node_list):
			tested_nodes.append(self.fit.fitness(self.desired_result, four_node_list[i]))

		fittest_from_first_lineage  = ""
		fittest_from_second_lineage = ""

		# testing fitness for the first lineage
		if tested_nodes[0] < 0 and tested_nodes[0] >= tested_nodes[1]:
			fittest_from_first_lineage = four_node_list[0]
		elif tested_nodes[0] > 0 and tested_nodes[0] < tested_nodes[1]:
			fittest_from_first_lineage = four_node_list[0]
		else:
			fittest_from_first_lineage = four_node_list[1]

		# testing fitness for the second lineage
		if tested_nodes[2] < 0 and tested_nodes[2] >= tested_nodes[3]:
			fittest_from_second_lineage = four_node_list[2]
		elif tested_nodes[2] > 0 and tested_nodes[2] < tested_nodes[3]:
			fittest_from_first_lineage = four_node_list[2]
		else:
			fittest_from_first_lineage = four_node_list[3]

		if fittest_from_first_lineage[0] == "'" or fittest_from_first_lineage[0] == '+':
			fittest_from_first_lineage = fittest_from_first_lineage[1:]
		if fittest_from_first_lineage[-1] == "'" or fittest_from_first_lineage[-1] == '-':
			fittest_from_first_lineage = fittest_from_first_lineage[:-1]


		return [fittest_from_first_lineage, fittest_from_second_lineage]

	def create_model(self):
		for i in range(len(self.model)):
			self.model_length      = len(self.model[i])
			self.individual_length = len(self.model[i][-1])


			self.first_half   = lambda index: self.model[index][self.model_length//2]
			self.second_half  = lambda index: self.model[index][self.model_length//2]

			self.reproduction_type = self.reproduction_combinations[random.randint(0, len(self.reproduction_combinations)-1)]
			if self.reproduction_type == self.reproduction_combinations[0]: # parallel
				if i % 2 == 0 and i > 0:
					# birthing children
					mutated_child_buffer = self._birth_mutated_child_nodes(i, 1)

					for j in range(len(mutated_child_buffer)):
						mutated_child_buffer[j] = mutated_child_buffer[j][0:len(mutated_child_buffer)-1]
						mutated_child_buffer[j] += str(random.randint(0, 9))


					fit_test = self._test_node_fitness(mutated_child_buffer)

					self.model[i].append(fit_test[0])
					self.model[i-1].append(fit_test[1])

					if self.fit.solve_equation(self.model[i][-1]) == self.desired_result:
						self.answer = self.model[i][-1]
						break
					if self.fit.solve_equation(self.model[i-1][-1]) == self.desired_result:
						self.answer = self.model[i-1][-1]
						break

			elif self.reproduction_type == self.reproduction_combinations[2]: # skip
				if i % 2 != 0 and i > 1:
					# 1, 3, 5, 7
					mutated_child_buffer = self._birth_mutated_child_nodes(i, 2)

					for j in range(len(mutated_child_buffer)):
						mutated_child_buffer[j] = mutated_child_buffer[j][0:len(mutated_child_buffer[j])-1]
						mutated_child_buffer[j] += str(random.randint(0, 9))

					fit_test = self._test_node_fitness(mutated_child_buffer)

					if self.fit.solve_equation(self.model[0]) == self.desired_result:
						self.answer = self.model[0]
						break
					if self.fit.solve_equation(self.model[1]) == self.desired_result:
						self.answer = self.model[1]
						break
  
					self.model[i].append(fit_test[0])
					self.model[i-2].append(fit_test[1])

				if i % 2 == 0 and i > 0:
					# 2, 4, 6, 8
					mutated_child_buffer = self._birth_mutated_child_nodes(i, 2)

					for j in range(len(mutated_child_buffer)):
						mutated_child_buffer[j] = mutated_child_buffer[j][0:len(mutated_child_buffer[j])-1]
						mutated_child_buffer[j] += str(random.randint(0, 9))

					fit_test = self._test_node_fitness(mutated_child_buffer)

					self.model[i].append(fit_test[0])
					self.model[i-2].append(fit_test[1])

					if self.fit.solve_equation(self.model[i][-1]) == self.desired_result:
						self.answer = self.model[i][-1]
						break
					if self.fit.solve_equation(self.model[i-2][-1]) == self.desired_result:
						self.answer = self.model[i-2][-1]
						break

			elif self.reproduction_type == self.reproduction_combinations[1]:
				# last, first | second_last, second | third_last, third
				first_child_first   = str(self.first_half(i)) + str(self.second_half(self.model_length-i))
				first_child_second  = str(self.first_half(i)), str(self.first_half(self.model_length-1))
				second_child_first  = str(self.second_half(i)), str(self.second_half(self.model_length))
				second_child_second = str(self.second_half(self.model_length-i)) + str(self.first_half(i))

				self._mutate_child_node(first_child_first)
				self._mutate_child_node(first_child_second)
				self._mutate_child_node(second_child_first)
				self._mutate_child_node(second_child_second)

				mutated_child_buffer = [first_child_first, first_child_second, second_child_first, second_child_second]

				fit_test = self._test_node_fitness(mutated_child_buffer)

				self.model[i].append(fit_test[0])
				self.model[i-2].append(fit_test[1])

				if self.fit.solve_equation(self.model[i][-1]) == self.desired_result:
					self.answer = self.model[i][-1]
					break
				if self.fit.solve_equation(self.model[i-2][-1]) == self.desired_result:
					self.answer = self.model[i-2][-1]
					break
 
		return self.answer

