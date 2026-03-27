#!/bin/sh
# Debug: find python
echo "Looking for python..."
ls -la /usr/local/bin/python* 2>/dev/null || echo "No python in /usr/local/bin"
ls -la /usr/bin/python* 2>/dev/null || echo "No python in /usr/bin"
which python3 2>/dev/null || echo "python3 not on PATH"
which python 2>/dev/null || echo "python not on PATH"
echo "PATH=$PATH"
echo "Looking for /app/vendor..."
ls /app/vendor/bin/ 2>/dev/null | head -20 || echo "No /app/vendor/bin"

# Set paths
export PYTHONPATH=/app/vendor:/app:${PYTHONPATH:-}
export PATH=/app/vendor/bin:${PATH:-/usr/local/bin:/usr/bin:/bin}

# Try multiple python paths
if command -v python3 >/dev/null 2>&1; then
    exec python3 -m streamlit run /app/main.py --server.port 8080 --server.address 0.0.0.0 --server.headless true --server.enableCORS false
elif [ -f /usr/local/bin/python3.11 ]; then
    exec /usr/local/bin/python3.11 -m streamlit run /app/main.py --server.port 8080 --server.address 0.0.0.0 --server.headless true --server.enableCORS false
else
    echo "ERROR: Cannot find python interpreter!"
    find / -name "python*" -type f 2>/dev/null | head -20
    exit 1
fi
