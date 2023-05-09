import re
class Fitness:
	def solve_equation(self, solution_plaintext) -> float:
		result = sum(map(int, re.findall(r'[+-]?\d+', str(solution_plaintext))))
		return result

	def fitness(self, desired_result, current):
		is_fit_to_live = False
		distance_relative_to_previous = ""

		presolved_desired_result = self.solve_equation(desired_result)
		presolved_current_result = self.solve_equation(current)

		fitness_number = float(presolved_current_result) - float(presolved_desired_result)

		return fitness_number
