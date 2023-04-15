FROM prefecthq/prefect:2.10.4-python3.9

RUN ["pip", "install", "gcsfs"]

# COPY requirements.txt /tmp/
# COPY setup.py /tmp/
# COPY src /tmp/src

# RUN pip install --upgrade pip setuptools --no-cache-dir

# ARG PREFECT_API_KEY
# ENV PREFECT_API_KEY=$PREFECT_API_KEY

# ARG PREFECT_API_URL
# ENV PREFECT_API_URL=$PREFECT_API_URL

# ENV PYTHONUNBUFFERED True

# RUN pip install --requirement /tmp/requirements.txt
# COPY . /tmp/

# ENTRYPOINT ["prefect", "agent", "start", "-q", "default"]