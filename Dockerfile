FROM python:3.11

# Set the current working dir to "/code"
WORKDIR /code

# First copy requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Install dependencies.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy code from the root directory
COPY ./*.py /code/
COPY ./schema.sql /code/schema.sql
# run get_raw_data.py
CMD ["python", "get_raw_data.py"]

# Copy API related code
COPY ./financial /code/app

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]