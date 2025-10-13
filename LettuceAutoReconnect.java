import io.lettuce.core.RedisClient;
import io.lettuce.core.RedisReadOnlyException;
import io.lettuce.core.RedisURI;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;

public class LettuceAutoReconnect {
    private static final String REDIS_HOST = "6427cc65-7fe6-4e41-8545-543762824412.c5km1ted03t0e8geevf0.databases.appdomain.cloud";
    private static final int REDIS_PORT = 30245;
    private static final String USERNAME = "ibm_cloud_13b1062d_838d_46eb_8e1f_a7111c388af8";
    private static final String PASSWORD = "xxxxxxxxxxxxxxxxxxx";
    private static final int RETRY_DELAY_MS = 5000;

    private static RedisClient redisClient;
    private static StatefulRedisConnection<String, String> connection;

    public static void main(String[] args) {
        connectToRedis(); // Initial connection

        while (true) {
            try {
                RedisCommands<String, String> commands = connection.sync();
                commands.set("test_key", "Hello, Redis!");
                String value = commands.get("test_key");
                System.out.println("Written to Redis: " + value);

                Thread.sleep(2000); // Sleep before next write
            } catch (RedisReadOnlyException e) {
                System.err.println("Redis is in READONLY mode! Reconnecting...");
                reconnectToRedis();
            } catch (Exception e) {
                System.err.println("Unexpected ERROR: " + e.getMessage());
                reconnectToRedis();
            }
        }
    }

    private static void connectToRedis() {
        try {
            RedisURI redisUri = RedisURI.builder()
                    .withHost(REDIS_HOST)
                    .withPort(REDIS_PORT)
                    .withAuthentication(USERNAME, PASSWORD)
                    .withSsl(true) // Ensure SSL is enabled
                    .withVerifyPeer(false) 
                    .build();

            // SslOptions sslOptions = SslOptions.builder()
            //         .jdkSslProvider()
            //         .verifyPeer(false) // Disable hostname verification
            //         .build();

            redisClient = RedisClient.create(redisUri);
            // redisClient.setOptions(redisClient.getOptions().mutation().sslOptions(sslOptions).build());

            connection = redisClient.connect();
            System.out.println("Connected to Redis: " + REDIS_HOST + ":" + REDIS_PORT);
        } catch (Exception e) {
            System.err.println("Failed to connect: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static void reconnectToRedis() {
        try {
            if (connection != null) {
                connection.close();
            }
            if (redisClient != null) {
                redisClient.shutdown();
            }
            Thread.sleep(RETRY_DELAY_MS);
            connectToRedis();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Reconnection interrupted.");
        }
    }
}
