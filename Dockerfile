FROM python:3.11-slim AS base

# Prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY i18n.py .
COPY kronos_dashboard.py .
COPY kronos_numpy/ ./kronos_numpy/
COPY download_models.py .
COPY fetch_btc_data.py .
COPY eval_btc_prediction.py .
COPY gen_word_plan.py .

# Create model cache directory
RUN mkdir -p /app/model_cache

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Download models at startup if not present, then launch Streamlit
CMD ["sh", "-c", "if [ ! -d /app/model_cache/models--NeoQuasar--Kronos-mini ]; then python download_models.py; fi && streamlit run kronos_dashboard.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true"]
