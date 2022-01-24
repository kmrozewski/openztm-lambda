# Define function directory
ARG LAMBDA_FUNCTION
ARG FUNCTION_DIR="/function"

FROM python:3.9-buster as build-image

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy function code
COPY functions/${LAMBDA_FUNCTION} ${FUNCTION_DIR}
COPY requirements.txt .

# Install dependencies and the runtime interface client (ric)
RUN pip3 install -r requirements.txt --target ${FUNCTION_DIR}
RUN pip3 install --target ${FUNCTION_DIR} awslambdaric


# Multi-stage build: grab a fresh copy of the base image
FROM python:3.9-alpine
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]