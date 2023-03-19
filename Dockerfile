# start by pulling the python image
FROM python:3.8-alpine

# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY requirements.txt ./

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . .

EXPOSE 8000
ENV PORT 5000

ENTRYPOINT [ "python", "app.py", "--host", "0.0.0.0"]
