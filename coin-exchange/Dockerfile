FROM node:16-alpine3.11
WORKDIR /home/coin/
COPY app.js ./app.js
COPY index.html ./index.html
COPY package.json ./package.json
RUN npm i

ENV FLAG "we{1e1b12c8-ed85-4b2b-879d-7475febe6281@d0g3&sh1b_th3_BEST!}"
ENV ADMIN_TOKEN "d6ccfd3a4cc18807825030209caa91a71bc074bd0bef2a516f7374a3576c0595"

CMD ["node", "app.js"]