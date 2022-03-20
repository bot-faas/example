module handler

go 1.16

replace handler/function => ./function

require (
	github.com/gin-gonic/gin v1.7.7
	github.com/golang/glog v1.0.0
	github.com/tencent-connect/botgo v0.0.0-20220216092122-03f91049a261
	go.mongodb.org/mongo-driver v1.8.4
)
