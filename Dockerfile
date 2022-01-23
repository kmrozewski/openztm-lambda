FROM public.ecr.aws/lambda/python:3.9-arm64

ARG LAMBDA_FUNCTION
COPY functions/$LAMBDA_FUNCTION ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["app.handler"]
