# Tabagism INCA RAG

To execute the application you can utilize docker, docker compose or fastapi in a virtual environment, first of all we need to specify our PDF file and OpenAI API token in .env, you can check the example that I provided. 

To run with only docker command follow the steps below:

- `docker build --tag "tabagism_rag"`
- `docker run tabagism_rag`

This will run the application into a container from docker, although, you can run with docker compose by just running the following command:

- `docker compose up`

To run as a virtual environment just follow the next commands:

- `python3 -m venv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- `fastapi run app.py --port 8000`

This will prepare all libraries needed to run the application.

If there's any doubt about how to do a request for the application, go to you're browser and type the following url:

`localhost:8000/docs`

This url will provide you a swagger from the application and you can see all that is needed to run a request, also you can run a request in this swagger if you want.