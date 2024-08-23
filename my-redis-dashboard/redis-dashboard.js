const redis = require('redis');
const RedisPool = require('node-redis-pool');
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');
const fs = require('fs');

// Create a Redis connection pool
const pool = new RedisPool({
    name: 'redisPool',
    redis,
    url: 'rediss://ibm_cloud_dc5af8d9_80ce_4a67_b3da_185ec8d49e60:a19703f40f02e07a4dc364d69c420523d29e8e8fc14fb58665d719aaa310a0d9@c3834e0d-be16-43f2-9bed-158a371eb3ea.ckol8aqd0p52cs1p0cog.dev.databases.appdomain.cloud:30837/0',
    ssl: {
        ca: fs.readFileSync("/Users/sanjeevchoubey/Downloads/15ec077f-064a-4eb3-a95c-edf1d9905001")
    },
    max_clients: 10,
    perform_checks: false
});

async function fetchRedisInfo() {
    return new Promise((resolve, reject) => {
        pool.acquire('redis', (err, client) => {
            if (err) {
                reject(`Error acquiring Redis client: ${err}`);
            } else {
                client.info((err, info) => {
                    pool.release('redis', client);
                    if (err) {
                        reject(`Error fetching Redis info: ${err}`);
                    } else {
                        const infoObject = parseRedisInfo(info);
                        resolve(infoObject);
                    }
                });
            }
        });
    });
}

function parseRedisInfo(info) {
    const lines = info.split('\r\n');
    const data = {};
    lines.forEach(line => {
        const parts = line.split(':');
        if (parts[1]) {
            data[parts[0]] = isNaN(parts[1]) ? parts[1] : Number(parts[1]);
        }
    });
    return data;
}

async function createDashboard(info) {
    if (!info) {
        console.log("Cannot create dashboard. Redis info is not available.");
        return;
    }

    const width = 800; // width of the chart
    const height = 600; // height of the chart
    const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

    const memoryData = {
        used_memory: info.used_memory,
        used_memory_rss: info.used_memory_rss,
        used_memory_peak: info.used_memory_peak,
        used_memory_lua: info.used_memory_lua
    };

    const commandsProcessed = {
        total_commands_processed: info.total_commands_processed,
        instantaneous_ops_per_sec: info.instantaneous_ops_per_sec
    };

    const connectedClients = {
        connected_clients: info.connected_clients,
        maxclients: info.maxclients
    };

    const config = {
        type: 'bar',
        data: {
            labels: Object.keys(memoryData),
            datasets: [{
                label: 'Memory Usage',
                data: Object.values(memoryData),
                backgroundColor: ['blue', 'green', 'red', 'orange']
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Memory Usage'
            }
        }
    };

    const imageBuffer = await chartJSNodeCanvas.renderToBuffer(config);
    fs.writeFileSync('memory_usage_chart.png', imageBuffer);

    config.data.labels = Object.keys(commandsProcessed);
    config.data.datasets[0].label = 'Commands Processed';
    config.data.datasets[0].data = Object.values(commandsProcessed);
    config.data.datasets[0].backgroundColor = ['purple', 'cyan'];

    const imageBuffer2 = await chartJSNodeCanvas.renderToBuffer(config);
    fs.writeFileSync('commands_processed_chart.png', imageBuffer2);

    config.data.labels = Object.keys(connectedClients);
    config.data.datasets[0].label = 'Connected Clients';
    config.data.datasets[0].data = Object.values(connectedClients);

    const imageBuffer3 = await chartJSNodeCanvas.renderToBuffer(config);
    fs.writeFileSync('connected_clients_chart.png', imageBuffer3);

    console.log("Charts created: memory_usage_chart.png, commands_processed_chart.png, connected_clients_chart.png");
}

(async () => {
    try {
        const info = await fetchRedisInfo();
        await createDashboard(info);
    } catch (e) {
        console.error(e);
    }
})();
