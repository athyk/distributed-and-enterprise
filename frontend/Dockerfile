FROM node:23-alpine3.21 AS base

RUN mkdir /app
WORKDIR /app

RUN rm -rf node_modules && rm -rf build
COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm
RUN pnpm i --no-frozen-lockfile

COPY . .

RUN pnpm run build

FROM node:23-alpine3.21 AS prod

RUN adduser -D appuser && mkdir /app && chown -R appuser /app

COPY --from=base /app /app

WORKDIR /app
COPY --chown=appuser:appuser . .
RUN rm -rf .git .github .venv docs backend unihub_project

USER appuser

EXPOSE 3000
CMD ["sh", "-c", "NODE_ENV=production node build"]