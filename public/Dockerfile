FROM python:3.9-slim

WORKDIR /public

COPY index.html /public

EXPOSE 80

CMD ["python", "-m", "http.server", "80"]
