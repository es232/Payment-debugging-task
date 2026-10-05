FROM python:3.10-slim

WORKDIR /app

COPY environment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying source files to establish a baseline in the image
COPY environment/app.py .
COPY tests/ tests/

CMD ["pytest", "tests/test_outputs.py", "-v"]
