format:
	black .
	isort . --profile black

create-env:
	conda env create -f environment.yml
