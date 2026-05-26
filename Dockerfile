# ==========================================
# Zero Hour Assault - Headless Server Engine
# ==========================================

# Use the official lightweight Python 3.12 slim image
FROM python:3.12-slim

# Set system-level environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/server

# Set working directory inside the container
WORKDIR /app/server

# Install headless server-specific dependencies directly
# (This avoids building client-side wxPython/Pygame wheels which fail on headless Linux slim images)
RUN pip install --no-cache-dir \
    websockets>=12.0 \
    PyNaCl>=1.5.0 \
    requests>=2.31.0 \
    psutil>=5.9.8

# Copy only the server directory into the container
COPY ./server /app/server

# Pre-create standard directories for persistent data storage
RUN mkdir -p /app/server/chars /app/server/logs

# Expose the default WebSocket server port (dynamic local/hosted)
EXPOSE 10000

# Start the high-performance WebSocket server
CMD ["python", "zhaserver.py"]
