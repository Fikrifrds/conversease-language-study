FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
COPY apps/web/package.json ./apps/web/package.json
COPY packages/shared/package.json ./packages/shared/package.json
RUN npm install

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}
ARG NEXT_STANDALONE=true
ENV NEXT_STANDALONE=${NEXT_STANDALONE}
RUN npm run build --workspace apps/web

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}
COPY --from=builder /app/apps/web/public ./apps/web/public
COPY --from=builder /app/apps/web/.next/standalone ./
COPY --from=builder /app/apps/web/.next/static ./apps/web/.next/static
EXPOSE 3000
CMD ["node", "apps/web/server.js"]
