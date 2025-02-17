FROM node:23-alpine3.21 AS base

RUN mkdir /app
WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm
RUN pnpm i --frozen-lockfile

COPY . .

RUN pnpm run build

FROM node:23-alpine3.21 AS prod

RUN adduser -D appuser && mkdir /app && chown -R appuser /app

COPY --from=base /app/package.json /app/pnpm-lock.yaml /app/build /app/

WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser

EXPOSE 3000
CMD ["sh", "-c", "NODE_ENV=production node build"]
