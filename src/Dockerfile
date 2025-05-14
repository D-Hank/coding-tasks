#ARG HTTP_PROXY=
#ARG HTTPS_PROXY=

# Pick a slim base that already has Python
FROM python:3.12-slim AS base

# 1) Install OS-level libs first (only the ones you really need)
#RUN apt-get update && apt-get install -y --no-install-recommends \
#        build-essential libpq-dev \
#    && rm -rf /var/lib/apt/lists/*

# 2) Copy your code and dependency list
WORKDIR /eval
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy the rest of your source
COPY . .

# 4) Choose the default command
CMD ["python", "evaluate.py"]