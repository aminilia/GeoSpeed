FROM node:22-alpine
WORKDIR /app
COPY apps/auto-headunit-simulator/package.json ./
RUN npm install
COPY apps/auto-headunit-simulator/ ./
EXPOSE 5174
CMD ["npm", "run", "dev"]

