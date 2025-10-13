import io.lettuce.core.RedisClient;
import io.lettuce.core.RedisReadOnlyException;
import io.lettuce.core.RedisURI;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;

public class LettuceContinuousWrite {
    public static void main(String[] args) {
        // Replace with your master Redis host and port
        String redisHost = "6427cc65-7fe6-4e41-8545-543762824412.c5km1ted03t0e8geevf0.databases.appdomain.cloud";  // Change to your Redis master
        int redisPort = 30245;            // Master port
        String USERNAME = "ibm_cloud_13b1062d_838d_46eb_8e1f_a7111c388af8";
        String PASSWORD = "xxxxxxxxxxxxxxxxxxx";

        RedisURI redisURI = RedisURI.builder()
                .withHost(redisHost)
                .withPort(redisPort)
                .withAuthentication(USERNAME, PASSWORD) 
                .withSsl(true)
                .withVerifyPeer(false) 
                .withTimeout(java.time.Duration.ofSeconds(10))
                .build();

        RedisClient redisClient = RedisClient.create(redisURI);
        StatefulRedisConnection<String, String> connection = redisClient.connect();
        RedisCommands<String, String> commands = connection.sync();

        System.out.println("Starting continuous write to Redis...");

        while (true) {
            try {
                commands.set("test_key", "Hello, Redis!");
                String value = commands.get("test_key");
                System.out.println("Written to Redis: " + value);

                // Sleep for 2 seconds before next write
                Thread.sleep(2000);
            } catch (RedisReadOnlyException e) {
                System.err.println("ERROR: Redis is in READONLY mode! Failing over?");
                e.printStackTrace();
            } catch (Exception e) {
                System.err.println("Unexpected ERROR: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }
}
