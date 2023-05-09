import re
class Fitness:
	def solve_equation(self, solution_plaintext) -> float:
		result = sum(map(int, re.findall(r'[+-]?\d+', str(solution_plaintext))))
		return result

	def fitness(self, desired_result, current):
		# recent_population_set is the three most recent nodes in the lineage. lineages are just the sublists that contain a set of different genomes evolving from the previous entity.
		is_fit_to_live = False
		distance_relative_to_previous = ""

		# step 1: solve for the most recent equation and see how far off it is from the desired solution.
		presolved_desired_result = self.solve_equation(desired_result)
		presolved_current_result = self.solve_equation(current)

		fitness_number = float(presolved_current_result) - float(presolved_desired_result)

		return fitness_number
		# ((recent_average + most_recent_node)/amount_of_added_numbers - desired_result)
		# step 2: condition against previous nodes in the linage, and condition against the sibling node in order to determine fitness (not because it's what happens in the wild, but because it optimizes the process)

