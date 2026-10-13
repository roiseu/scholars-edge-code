docker build -t fedids-paper:1.0 .
docker run --rm -v "$(pwd)/results:/app/results" fedids-paper:1.0
