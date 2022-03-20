package openapi

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"net/textproto"
	url2 "net/url"
	"os"
	"strconv"

	"github.com/tencent-connect/botgo"
	"github.com/tencent-connect/botgo/openapi"

	token2 "github.com/tencent-connect/botgo/token"
)

func OpenAPI() openapi.OpenAPI {
	appToken, sandbox := os.Getenv("APP_TOKEN"), false
	appId, _ := strconv.ParseInt(os.Getenv("APP_ID"), 10, 64)
	if os.Getenv("SANDBOX_BOT") == "true" {
		sandbox = true
	}
	token := token2.BotToken(uint64(appId), appToken)
	var api openapi.OpenAPI
	if sandbox {
		api = botgo.NewSandboxOpenAPI(token)
	} else {
		api = botgo.NewOpenAPI(token)
	}
	return api
}

type UploadPicResponse struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
	Data struct {
		ID  string `json:"id"`
		Url string `json:"url"`
	} `json:"data"`
}

func UploadPic(name string, file io.Reader) (*UploadPicResponse, error) {
	url := os.Getenv("HOME_URL") + "/api/v1/open/guild/pic"
	method := "POST"

	payload := &bytes.Buffer{}
	writer := multipart.NewWriter(payload)
	h := make(textproto.MIMEHeader)
	h.Set("Content-Disposition",
		fmt.Sprintf(`form-data; name="%s"; filename="%s"`,
			url2.QueryEscape("pic"), url2.QueryEscape(name)))
	h.Set("Content-Type", "image/png")
	part, err := writer.CreatePart(h)
	if err != nil {
		return nil, err
	}
	if _, err := io.Copy(part, file); err != nil {
		return nil, err
	}
	err = writer.Close()
	if err != nil {
		return nil, err
	}
	client := &http.Client{}
	req, err := http.NewRequest(method, url, payload)
	if err != nil {
		return nil, err
	}
	sandbox := "0"
	if os.Getenv("SANDBOX_BOT") == "true" {
		sandbox = "1"
	}
	req.Header.Add("X-AppId", os.Getenv("APP_ID"))
	req.Header.Add("X-Sandbox", sandbox)
	req.Header.Add("X-AppToken", os.Getenv("APP_TOKEN"))

	req.Header.Set("Content-Type", writer.FormDataContentType())
	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		return nil, err
	}
	ret := &UploadPicResponse{}
	if err := json.Unmarshal(body, ret); err != nil {
		return nil, err
	}
	return ret, nil
}
