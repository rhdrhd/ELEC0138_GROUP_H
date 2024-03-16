create-env:
	conda env create -f environment.yml

format:
	black .
