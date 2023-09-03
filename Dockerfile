# selecting the python version
FROM python:3.11
# exposing the port where the app will run

EXPOSE 4000

COPY requirements.txt .
# install requirements
RUN pip install -r requirements.txt
# copy everything (first .) to the directory we are at (second .)
COPY . .
# say what commands will run the container
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "4000"]


# flask run --host 0.0.0.0 --port 4000
