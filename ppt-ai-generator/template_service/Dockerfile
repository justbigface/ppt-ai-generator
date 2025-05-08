FROM node:20-alpine
WORKDIR /app
COPY template_service/package*.json ./
RUN npm install --production
COPY template_service /app
CMD ["node", "main.js"]
