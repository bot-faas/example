package db

import (
	"context"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func MongoDB() (*mongo.Database, error) {
	cli, err := mongo.Connect(context.Background(), options.Client().ApplyURI(os.Getenv("BOT_FAAS_MONGODB_URI")))
	if err != nil {
		return nil, err
	}
	return cli.Database(os.Getenv("BOT_FAAS_MONGODB_DBNAME")), nil
}
