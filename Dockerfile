# imagem base do Python
FROM python:3.11-slim

# diretório de trabalho
WORKDIR /app

# Copia arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expoe porta
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "app.py"]