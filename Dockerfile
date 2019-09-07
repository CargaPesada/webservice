#Latest version of the Python
FROM python:latest

#Work directory of the folder
WORKDIR /app

#Copy the source code to the container
COPY requirements.txt ./

#Install python libraries
RUN pip install --no-cache-dir -r requirements.txt

#Set environment variables
ENV FLASK_APP=app.py

EXPOSE 5000

COPY . .

ENTRYPOINT ["python"]
CMD ["app.py"]