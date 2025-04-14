# fe/Dockerfile

FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# Serve using a simple static server
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
