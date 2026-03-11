FROM node:20-alpine AS builder

WORKDIR /frontend

COPY package.json package-lock.json tsconfig.json ./
RUN npm ci

COPY ts ./ts
COPY public ./public
RUN npm run build:frontend

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /frontend/public /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
