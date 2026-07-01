FROM node:22-alpine AS deps
WORKDIR /app
COPY apps/web-dashboard/package.json ./
RUN npm install

FROM deps AS runtime
COPY apps/web-dashboard/ ./
EXPOSE 5173
CMD ["npm", "run", "dev"]

