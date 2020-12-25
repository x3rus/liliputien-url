
test:
	python3 liliputien_test.py
	python3 webui_test.py

local-db:
	docker-compose up -d mongo 

run-webui: local-db
	export FLASK_APP=webui.py ; flask run

