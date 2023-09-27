# selecting the python version
FROM python:3.11
EXPOSE 4000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "4000"]
