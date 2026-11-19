FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements-vector.txt ./
ARG INSTALL_VECTOR=false
RUN pip install --no-cache-dir -r requirements.txt && if [ "$INSTALL_VECTOR" = "true" ]; then pip install --no-cache-dir -r requirements-vector.txt; fi
COPY app/ app/
COPY scripts/ scripts/
COPY data/ data/
COPY rag_docs/ rag_docs/
RUN mkdir -p runtime
CMD ["sh","-c","python scripts/seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
