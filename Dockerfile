FROM python:3.11-slim

# Instalamos OpenTimestamps y dependencias necesarias
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Clonamos el repositorio de OpenTimestamps
RUN git clone https://github.com/opentimestamps/opentimestamps-client.git /ots
WORKDIR /ots
RUN python3 setup.py install

# Creamos carpeta de trabajo y copiamos archivos
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Exponemos el puerto para Flask
EXPOSE 5000

# Ejecutamos la app
CMD ["python", "main.py"]
