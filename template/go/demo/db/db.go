package function

import (
	"context"
	"fmt"
	"handler/pkg/db" // 此处引入数据库组件
	"handler/pkg/openapi"

	"github.com/tencent-connect/botgo/dto"
	"go.mongodb.org/mongo-driver/mongo"
)

var mongodb *mongo.Database
var api = openapi.OpenAPI()

func init() {
	var err error
	mongodb, err = db.MongoDB()
	if err != nil {
		panic(err)
	}
}

// Handle a qqbot request
func Handle(msg *dto.WSATMessageData) (*dto.Message, error) {
	count := struct {
		UID   string `json:"uid"`
		Count int64  `json:"count"`
	}{UID: msg.Author.ID, Count: 1}
	if err := mongodb.Collection("count").FindOne(context.Background(), map[string]string{"uid": msg.Author.ID}).Decode(&count); err != nil {
		if err == mongo.ErrNoDocuments {
			if _, err := mongodb.Collection("count").InsertOne(context.Background(), &count); err != nil {
				fmt.Printf("insert failed: %v", err)
			}
		}
		count.Count = 1
	} else {
		_, err := mongodb.Collection("count").UpdateOne(context.Background(), map[string]string{"uid": msg.Author.ID}, map[string]interface{}{
			"$inc": map[string]interface{}{
				"count": 1,
			},
		})
		if err != nil {
			fmt.Printf("update failed: %v", err)
		}
		count.Count += 1
	}
	return api.PostMessage(context.Background(), msg.ChannelID, &dto.MessageToCreate{
		Content:          fmt.Sprintf("<@!%s>这是第%d条消息", msg.Author.ID, count.Count),
		MsgID:            msg.ID,
		MessageReference: nil,
		Markdown:         nil,
	})
}
