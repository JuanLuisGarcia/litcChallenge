# CREATE A MULTISTAGE WITH A BUILDER AND A RUNNER
FROM python:3.10-alpine as builder

WORKDIR /app

RUN pip3 install --upgrade build

COPY . /app

# THIS STEP GENERATE ON /app/dist A whl FILE
RUN python3 -m build

FROM python:3.10-alpine as runner

ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:5000", "api:app"]

EXPOSE 5000

RUN addgroup -S docker && \
    adduser -S --shell /bin/bash --ingroup docker docker

RUN apk update && pip install gunicorn

# COPY AND INSTALL whl FILE FROM BUILDER
COPY --from=builder /app/dist/*.whl ./
RUN pip install *.whl

USER docker

