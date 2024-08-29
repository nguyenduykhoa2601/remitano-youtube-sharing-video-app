FROM node:16.0.0 AS build-stage

# Set working directory
WORKDIR /app

COPY package*.json ./

# RUN export NODE_OPTIONS=--openssl-legacy-provider
COPY . .
RUN npm config set legacy-peer-deps true
RUN npm install
RUN npm run build

# 2. For Nginx setup
FROM nginx as production-stage
RUN mkdir /app
RUN cd /app
RUN ls
COPY --from=build-stage /app/dist /app 



ENTRYPOINT ["nginx", "-g", "daemon off;"]
