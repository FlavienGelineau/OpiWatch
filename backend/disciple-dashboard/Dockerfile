FROM node:10

# Create app directory
WORKDIR /usr/src/disciple-app-dashboard

ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

# Install dependencies
RUN npm install

# Bundle app source
COPY . .

EXPOSE 8080
CMD [ "npm", "start" ]