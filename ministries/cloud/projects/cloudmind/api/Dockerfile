FROM golang:1.21-alpine AS builder

WORKDIR /app

# Установка зависимостей
COPY go.mod go.sum ./
RUN go mod download

# Копирование исходников
COPY . .

# Сборка
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o api main.go

# Финальный образ
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Копирование бинарника
COPY --from=builder /app/api .

EXPOSE 8080

CMD ["./api"]
