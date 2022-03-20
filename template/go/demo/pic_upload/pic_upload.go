package function

import (
	"bytes"
	"context"
	"fmt"
	"handler/pkg/openapi"
	"io"
	"net/http"

	"github.com/tencent-connect/botgo/dto"
)

var api = openapi.OpenAPI()

// Handle a qqbot request
// 请将"bot.icodef.com/api/v1/open/guild/pic"加入qq机器人管理的消息URL配置
func Handle(msg *dto.WSATMessageData) (*dto.Message, error) {
	resp, err := http.Get("https://bbs.tampermonkey.net.cn/uc_server/avatar.php?uid=4&size=big&ts=1")
	if err != nil {
		return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
			Content: fmt.Sprintf("<@!%s>图片发送失败: %v", msg.Author.ID, err),
			MsgID:   msg.ID,
		})
	}
	buf := bytes.NewBuffer(nil)
	defer resp.Body.Close()
	if _, err := io.Copy(buf, resp.Body); err != nil {
		return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
			Content: fmt.Sprintf("<@!%s>图片发送失败: %v", msg.Author.ID, err),
			MsgID:   msg.ID,
		})
	}
	pic, err := openapi.UploadPic("test.png", buf)
	if err != nil {
		return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
			Content: fmt.Sprintf("<@!%s>图片发送失败: %v", msg.Author.ID, err),
			MsgID:   msg.ID,
		})
	}
	if pic.Code == 0 {
		return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
			Image: pic.Data.Url,
			MsgID: msg.ID,
		})
	}
	return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
		Content: fmt.Sprintf("<@!%s>图片发送失败: %v", msg.Author.ID, pic.Msg),
		MsgID:   msg.ID,
	})
}
