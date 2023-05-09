default: *.py
	python3 main.py

g: *.py # genetic testing - replaced makefile target name with letter 'g' so testing would be easier
	python3 gen.test.py

f: *.py # fitness testing - replaced makefile target name with letter 'f' so testing would be easier
	python3 fitness.test.py
