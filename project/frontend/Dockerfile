# ---------- Stage 1: Build frontend ----------
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# ---------- Stage 2: Serve built files ----------
FROM nginx:alpine

# Copy Vite build output to Nginx's web root
COPY --from=build /app/dist /usr/share/nginx/html

# (Optional but nice) – reduce noisy logs
RUN sed -i 's/access_log .*/access_log \/dev\/stdout;/g' /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
