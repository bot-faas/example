FROM golang:1.16-alpine3.14 as build

ARG GOOS=linux
ARG GOARCH=amd64
ARG GOPROXY="https://goproxy.cn,direct"

WORKDIR /bot-faas

COPY . .

RUN chmod +x ./function/build_script && \
    ./function/build_script

RUN go build -o handler .

FROM alpine:3.14

WORKDIR /bot-faas

COPY --from=build /bot-faas/handler .

RUN chmod +x handler

CMD ["./handler"]
