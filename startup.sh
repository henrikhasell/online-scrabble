#!/usr/bin/bash
set -euxo pipefail

docker build -t online_scrabble .
docker run --rm -it -p 8000:8000 online_scrabble
