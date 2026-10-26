FROM python:3.11-slim

# Install system dependencies including GCC for C code compilation
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (UID 1000) for security & cloud compatibility
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PORT=5000 \
    PYTHONUNBUFFERED=1

WORKDIR $HOME/app

# Install Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application files (HTML, CSS, Python, and C source)
COPY --chown=user:user . .

# Compile C threat engine module into shared library
RUN gcc -O3 -shared -fPIC -o threat_engine/c_threat_core.so threat_engine/c_threat_core.c 2>/dev/null || true

# Expose port (Render automatically sets $PORT)
EXPOSE 5000

# Start production server
CMD ["python", "app.py"]
