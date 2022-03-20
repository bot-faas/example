package main

import (
	"encoding/json"
	"handler/function"
	"net/http"
	"reflect"

	"github.com/gin-gonic/gin"
	"github.com/golang/glog"
)

type BotHandleRequest struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
	Data string `json:"data,omitempty"`
}

func main() {
	handleFunc := reflect.ValueOf(function.Handle)
	handleFuncType := reflect.TypeOf(function.Handle)
	param := handleFuncType.In(0)

	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()
	r.POST("handle", func(c *gin.Context) {
		paramData := reflect.New(param.Elem())
		d := &BotHandleRequest{}
		if err := c.BindJSON(d); err != nil {
			c.JSON(http.StatusBadRequest, BotHandleRequest{Code: 1000, Msg: err.Error()})
			return
		}
		i := paramData.Interface()
		if err := json.Unmarshal([]byte(d.Data), i); err != nil {
			c.JSON(http.StatusBadGateway, BotHandleRequest{Code: 1001, Msg: err.Error()})
			return
		}
		ret := handleFunc.Call([]reflect.Value{reflect.ValueOf(i)})
		if len(ret) != 2 {
			c.JSON(http.StatusBadRequest, BotHandleRequest{Code: 1002, Msg: "unknown"})
			return
		}
		if err, ok := ret[1].Interface().(error); ok && err != nil {
			c.JSON(http.StatusBadGateway, BotHandleRequest{Code: 1003, Msg: err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{
			"code": 0, "msg": "ok", "data": ret[0].Interface(),
		})
	})
	err := r.Run(":8080")
	if err != nil {
		glog.Fatalf("run watch service failed: %v", err)
	}
}
