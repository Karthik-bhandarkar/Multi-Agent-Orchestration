# ---------- Stage 1: Builder ----------
FROM python:3.10-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .
RUN pip install --no-cache-dir --user -e .

# ---------- Stage 2: Runtime ----------
FROM python:3.10-slim AS runtime

RUN groupadd -g 1001 edupulse && \
    useradd -u 1001 -g edupulse -m -s /bin/bash edupulse

WORKDIR /app

COPY --from=builder /root/.local /home/edupulse/.local
COPY --from=builder /build /app

ENV PATH=/home/edupulse/.local/bin:$PATH
ENV PYTHONPATH=/app

RUN chown -R edupulse:edupulse /app

USER edupulse

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
