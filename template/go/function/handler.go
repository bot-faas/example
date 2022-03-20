package function

import (
	"context"
	"handler/pkg/openapi"

	"github.com/tencent-connect/botgo/dto"
)

var api = openapi.OpenAPI()

// Handle a qqbot request
func Handle(msg *dto.WSATMessageData) (*dto.Message, error) {
	return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
		Content:          "<@!" + msg.Author.ID + ">ok",
		MsgID:            msg.ID,
		MessageReference: nil,
		Markdown:         nil,
	})
}
