# Imagem oficial do Playwright para Python, com os navegadores (Chromium,
# Firefox, WebKit) e suas dependências de sistema já instalados. A tag da
# imagem precisa acompanhar a versão do pacote "playwright" no requirements.txt.
FROM mcr.microsoft.com/playwright/python:v1.63.0-noble

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HEADLESS=true

CMD ["pytest", "-n", "auto", "--html=reports/report.html", "--self-contained-html"]
