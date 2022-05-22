FROM python:3.8

RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  python3-gdal

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.

RUN python3 -m venv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
COPY requirements.txt .
RUN pip install -r requirements.txt
# Add the application source code.
ADD . /app
WORKDIR /app

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
CMD gunicorn -b :$PORT main_api.wsgi
