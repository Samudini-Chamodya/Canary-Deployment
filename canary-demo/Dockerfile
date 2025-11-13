FROM python:3.9-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
# Set default version
ARG VERSION=v1
ENV VERSION=${VERSION}
EXPOSE 8080
CMD ["python", "app.py"]