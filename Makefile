run:
	python app.py

create-env:
	conda env create -f environment.yml

format:
	black .
