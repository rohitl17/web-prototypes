FROM python:3.11-slim
WORKDIR /app

# Install system deps for rendering SVGs and fonts (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV PORT=8501

EXPOSE 8501

CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"]
