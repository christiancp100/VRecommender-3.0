FROM node:lts

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

CMD [ "npm", "run", "serve" ]
