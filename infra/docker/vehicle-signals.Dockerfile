FROM python:3.12-slim
WORKDIR /app
COPY services/vehicle-signals-python/pyproject.toml ./
RUN pip install --no-cache-dir fastapi==0.115.6 pydantic==2.10.4 "uvicorn[standard]==0.34.0"
COPY services/vehicle-signals-python/src ./src
COPY simulations ./simulations
ENV PYTHONPATH=/app/src
EXPOSE 8010
CMD ["uvicorn", "geospeed_vehicle.app:app", "--host", "0.0.0.0", "--port", "8010"]

