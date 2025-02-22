FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# Pip Update & Install
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY bankapi .

EXPOSE 5000

# Create user
RUN useradd www
RUN chown -R www:www /app
USER www

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]