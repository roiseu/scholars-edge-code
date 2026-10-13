# Reproducible environment for the companion code (book Chapter 12).
#   docker build -t scholars-edge .
#   docker run --rm -v "$(pwd)/results:/app/results" scholars-edge          # capstone
#   docker run --rm -p 8888:8888 scholars-edge jupyter lab --ip=0.0.0.0 --allow-root --no-browser
FROM python:3.11-slim

WORKDIR /app

# Install exact dependencies first (cached between builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Running the container regenerates all capstone results
CMD ["bash", "capstone/run_all.sh"]
