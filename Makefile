test:
	pytest .
fmt:
	black .
	isort -rc .
	autoflake .