FROM python:3.11-alpine

# Update package manager
RUN apk update

# Copy backend files to container
ADD . /api
WORKDIR /api

# Install Python dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

# Run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]