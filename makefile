default: *.py
	python3 main.py

g: *.py
	python3 gen.test.py

f: *.py
	python3 fitness.test.py
