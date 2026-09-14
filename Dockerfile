FROM node:18-slim

RUN apt-get update && apt-get install -y ffmpeg wget python3 python3-pip && \
    pip3 install --break-system-packages gdown && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 10000

CMD ["node", "server.js"]
