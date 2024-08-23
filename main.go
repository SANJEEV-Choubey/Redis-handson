package connection

import (
	"context"
	"crypto/tls"
	"fmt"
	"os/user"
	"time"

	"github.com/go-redis/redis/v8"
	gv "github.com/hashicorp/go-version"
)

var redisTestData = map[string]string{
	"muffin_types":     "bran oatmeal blueberry",
	"best_muffin_type": "bran",
}

// RedisClient implement the DBClient interface.
type RedisClient struct {
	dbClient *redis.Client
}

type Connection struct {
	user             string
	password         string
	host             string
	port             string
	ssl_ca_certs     string
	db               int
	decode_responses bool
}

type connections map[string]interface{}

// Close used to close the connection.
func (r *RedisClient) Close() error {
	if r.dbClient != nil {
		return r.dbClient.Close()
	}
	return nil
}

// Connect used to connect to the instance.
func (r *RedisClient) Connect(connections []*tests.Connection, tlsConfig *tls.Config, username, password, version string, allowFailure bool) (interface{}, error) {
	if len(connections) == 0 {
		return nil, fmt.Errorf("no connection exists")
	}

	redisVersion, err := gv.NewVersion(version)
	if err != nil {
		return nil, err
	}

	v6, err := gv.NewVersion("6.0.0")
	if err != nil {
		return nil, err
	}

	if redisVersion.LessThan(v6) {
		username = ""
	}

	// if coming from canNotConnectToInstance, stop after first failure
	maxRetries := 5
	if allowFailure {
		maxRetries = 0
	}
	r.dbClient = redis.NewClient(&redis.Options{
		Username:    username,
		Addr:        fmt.Sprintf("%s:%d", connections[0].Hostname, connections[0].Port),
		Password:    password,
		DB:          0,
		TLSConfig:   tlsConfig,
		DialTimeout: 20 * time.Second,
		MaxRetries:  maxRetries,
	})

	_, err = r.dbClient.Ping(context.Background()).Result()
	return r.dbClient, err
}

// WriteData write some data to the instance.
func (r *RedisClient) WriteData() error {

	for key, value := range redisTestData {
		if err := r.dbClient.Set(context.Background(), key, value, 0).Err(); err != nil {
			return err
		}
	}

	return nil
}

// VerifyData verify the existence of the data we wrote.
func (r *RedisClient) VerifyData(_ tests.InstanceType) (bool, error) {

	for key, value := range redisTestData {
		val, err := r.dbClient.Get(context.Background(), key).Result()
		if err != nil {
			return false, err
		}

		if value != val {
			return false, fmt.Errorf("failed to verify the data")
		}
	}

	return true, nil
}

// VerifyUpdatedResource used to verify that database is aware of updated resources after a scale.
func (r *RedisClient) VerifyUpdatedResource(args tests.DatabaseTestArgs) error {
	return nil
}

func (r *RedisClient) GetPitrTimestamp() (string, error) {
	// not implemented
	return "", nil
}

func main() {
c:= connections["skc"]{
	"user":"admin",
	"passowrd":
}

}
