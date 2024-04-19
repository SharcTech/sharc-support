using System;
using System.Text;
using System.Threading.Tasks;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Client.Options;

namespace SharcSim
{
    public class Sharc
    {
        public string SharcID = "SharcTest";
        public string BrokerConnection = "wss.sharc.tech:9001";

        public async Task<(string SharcID, string BrokerConnection)> SharcMenu()
        {
            while (string.IsNullOrEmpty(SharcID))
            {
                Console.Clear();
                Console.Write("Please enter a 'SHARC' ID: ");
                SharcID = Console.ReadLine() ?? "";
            }

            while (string.IsNullOrEmpty(BrokerConnection))
            {
                Console.Clear();
                Console.Write("Please enter Broker Information: ");
                // Console.WriteLine("Follow BrokerAddress:Port Format.");
                BrokerConnection = Console.ReadLine() ?? "";
            }

            return (SharcID, BrokerConnection);
        }

        public async Task EstablishConnection(string sharc, string broker)
        {
            Console.WriteLine($"Connecting to {broker}.");
            var factory = new MqttFactory();
            var mqttClient = factory.CreateMqttClient();
            var options = new MqttClientOptionsBuilder()
                .WithWebSocketServer(broker)
                .Build();
            mqttClient.UseConnectedHandler(async e =>
            {
                Console.Clear();
                Console.WriteLine("Succesfully Connected.");
                await ChooseMessage(mqttClient);
            });
            await mqttClient.ConnectAsync(options, CancellationToken.None);
        }

        public async Task ChooseMessage(IMqttClient mqttClient)
        {
            string choice = "";
            bool keepRunning = true;
            do
            {
                while (string.IsNullOrEmpty(choice))
                {
                    Console.Clear();
                    Console.WriteLine("Please select an option");
                    Console.WriteLine("1) Simulate PNP Part Count 1-X");
                    Console.WriteLine("2) Simulate NPN Part Count 1-X");
                    Console.WriteLine("3) Simulate Random Voltage");
                    Console.WriteLine("4) Simulate Random Amperage");
                    Console.WriteLine("7) Simulate Reboot");
                    Console.WriteLine("8) Send all 'SHARC' settings");
                    Console.WriteLine("9) Exit");
                    choice = Console.ReadLine();
                }

                if (choice == "1")
                {
                    int x;
                    Console.Clear();
                    Console.WriteLine("How many parts do you want to simulate?");
                    while (!int.TryParse(Console.ReadLine(), out x))
                    {
                        Console.Clear();
                        Console.WriteLine("Invalid input. Please enter a valid integer.");
                        Console.WriteLine("How many parts do you want to simulate?");
                    }

                    int i;
                    for (i = 1; i <= x; i++)
                    {
                        var message = new MqttApplicationMessageBuilder()
                            .WithTopic($"sharc/{SharcID}/evt/io/s0")
                            .WithPayload($"{{\"seq\":1,\"v\":{{\"s0\":{{\"v\": {i}, \"u\": \"count\"}}}}}}")
                            .Build();
                        Console.Clear();
                        Console.WriteLine($"Sending part {i}.");
                        await mqttClient.PublishAsync(message, CancellationToken.None);
                        await Task.Delay(500);
                    }

                    bool goBack = false;
                    while (!goBack)
                    {
                        string readGoBack = "";
                        Console.Clear();
                        Console.WriteLine("Success! Enter 9 to go back to menu.");
                        readGoBack = Console.ReadLine();
                        if (readGoBack == "9")
                        {
                            goBack = true;
                            choice = "";
                        }
                    }
                }
                else if (choice == "2")
                {
                    int x;
                    Console.Clear();
                    Console.WriteLine("How many parts do you want to simulate?");
                    while (!int.TryParse(Console.ReadLine(), out x))
                    {
                        Console.Clear();
                        Console.WriteLine("Invalid input. Please enter a valid integer.");
                        Console.WriteLine("How many parts do you want to simulate?");
                    }

                    int i;
                    for (i = 1; i <= x; i++)
                    {
                        var message = new MqttApplicationMessageBuilder()
                            .WithTopic($"sharc/{SharcID}/evt/io/s1")
                            .WithPayload($"{{\"seq\":1,\"v\":{{\"s1\":{{\"v\": {i}, \"u\": \"count\"}}}}}}")
                            .Build();
                        Console.Clear();
                        Console.WriteLine($"Sending part {i}.");
                        await mqttClient.PublishAsync(message, CancellationToken.None);
                        await Task.Delay(500);
                    }

                    bool goBack = false;
                    while (!goBack)
                    {
                        string readGoBack = "";
                        Console.Clear();
                        Console.WriteLine("Success! Enter 9 to go back to menu.");
                        readGoBack = Console.ReadLine();
                        if (readGoBack == "9")
                        {
                            goBack = true;
                            choice = "";
                        }
                    }
                }
                else if (choice == "3")
                {
                    bool goBack = false;
                    Console.Clear();
                    Console.WriteLine("Simulating Voltage! Enter 9 to stop and go back to menu.");
                    Task.Run(async () =>
                    {
                        while (!goBack)
                        {
                            Random random = new Random();
                            double randomNumber = random.NextDouble() * 10;
                            var message = new MqttApplicationMessageBuilder()
                                .WithTopic($"sharc/{SharcID}/evt/io/s2")
                                .WithPayload(
                                    $"{{\"seq\":1,\"v\":{{\"s2\":{{\"v\":{Math.Round(randomNumber, 2)},\"u\":\"v\"}}}}}}")
                                .Build();
                            await mqttClient.PublishAsync(message, CancellationToken.None);
                            await Task.Delay(2000);
                        }
                    });
                    while (!goBack)
                    {
                        string readGoBack = Console.ReadLine();
                        if (readGoBack == "9")
                        {
                            goBack = true;
                            choice = "";
                        }
                    }
                }
                else if (choice == "4")
                {
                    bool goBack = false;
                    Console.Clear();
                    Console.WriteLine("Simulating Amperage! Enter 9 to stop and go back to menu.");
                    Task.Run(async () =>
                    {
                        while (!goBack)
                        {
                            Random random = new Random();
                            double randomNumber = random.NextDouble() * (20 - 4) + 4;
                            var message = new MqttApplicationMessageBuilder()
                                .WithTopic($"sharc/{SharcID}/evt/io/s3")
                                .WithPayload(
                                    $"{{\"seq\":1,\"v\":{{\"s3\":{{\"v\":{Math.Round(randomNumber, 2)},\"u\":\"mA\"}}}}}}")
                                .Build();
                            await mqttClient.PublishAsync(message, CancellationToken.None);
                            await Task.Delay(2000);
                        }
                    });
                    while (!goBack)
                    {
                        string readGoBack = Console.ReadLine();
                        if (readGoBack == "9")
                        {
                            goBack = true;
                            choice = "";
                        }
                    }
                }
                else if (choice == "7")
                {
                    var turnOff = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/avail")
                        .WithPayload("{\"seq\": 6, \"v\": false}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine($"Sending avail false as {SharcID}.");
                    await mqttClient.PublishAsync(turnOff, CancellationToken.None);
                    await Task.Delay(3000);
                    Console.Clear();
                    Console.WriteLine($"Sending avail true as {SharcID}.");
                    var turnOn = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/avail")
                        .WithPayload("{\"seq\": 6, \"v\": true}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine("Success");
                    await mqttClient.PublishAsync(turnOn, CancellationToken.None);
                    bool goBack = false;
                    while (!goBack)
                    {
                        string readGoBack = "";
                        Console.Clear();
                        Console.WriteLine("Success! Enter 9 to go back to menu.");
                        readGoBack = Console.ReadLine();
                        if (readGoBack == "9")
                        {
                            goBack = true;
                            choice = "";
                        }
                    }
                }
                else if (choice == "8")
                {
                    Console.Clear();
                    Console.WriteLine($"Sending /evt/io messages.");
                    var s0 = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/io/s0")
                        .WithPayload($"{{\"seq\":1,\"v\":{{\"s0\":{{\"v\": 1, \"u\": \"count\"}}}}}}")
                        .Build();
                    await mqttClient.PublishAsync(s0, CancellationToken.None);
                    var s1 = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/io/s1")
                        .WithPayload($"{{\"seq\":1,\"v\":{{\"s1\":{{\"v\": 1, \"u\": \"count\"}}}}}}")
                        .Build();
                    await mqttClient.PublishAsync(s1, CancellationToken.None);
                    var s2 = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/io/s2")
                        .WithPayload($"{{\"seq\":1,\"v\":{{\"s2\":{{\"v\":1,\"u\":\"v\"}}}}}}")
                        .Build();
                    await mqttClient.PublishAsync(s2, CancellationToken.None);
                    var s3 = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/io/s3")
                        .WithPayload($"{{\"seq\":1,\"v\":{{\"s3\":{{\"v\":4,\"u\":\"mA\"}}}}}}")
                        .Build();
                    await mqttClient.PublishAsync(s3, CancellationToken.None);
                    var ver = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/ver")
                        .WithPayload(
                            $"{{\"seq\": 7, \"v\": {{\"serial\": \"{SharcID}\", \"sw\": \"DEV/FROZEN\", \"hw\": \"105\", \"fw\": \"cb6c2a3\", \"model\": \"SHARC\", \"mfg\": \"Frenzy Engineering\"}}}}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine($"Sending /evt/ver message.");
                    await mqttClient.PublishAsync(ver, CancellationToken.None);
                    var rc = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/rc")
                        .WithPayload(
                            $"{{\"seq\": 8, \"v\": {{\"watchdog_reset\": 1, \"power_on\": 23, \"deep_sleep\": 0, \"soft_reset\": 0, \"hard_reset\": 25}}}}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine($"Sending /evt/rc message.");
                    await mqttClient.PublishAsync(rc, CancellationToken.None);
                    var net = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/net")
                        .WithPayload(
                            $"{{\"seq\": 9, \"v\": {{\"dns\": \"192.168.0.1\", \"mask\": \"255.255.255.0\", \"mac\": \"{SharcID}\", \"quality\": 100, \"ip\": \"192.168.0.99\", \"type\": \"LAN\", \"static\": false, \"gw\": \"192.168.0.1\"}}}}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine($"Sending /evt/net message.");
                    await mqttClient.PublishAsync(net, CancellationToken.None);
                    var mqttSettings = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/mqtt")
                        .WithPayload(
                            "{\"seq\": 10, \"v\": {\"user\": \"\", \"anonymous\": true, \"pass\": \"\", \"address\": \"192.168.0.1\", \"port\": 1883}}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine($"Sending /evt/mqtt message.");
                    await mqttClient.PublishAsync(mqttSettings, CancellationToken.None);
                    var user = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/user")
                        .WithPayload("{\"seq\": 1, \"v\": {\"since_boot_s\": 30}}")
                        .Build();
                    Console.Clear();
                    Console.WriteLine($"Sending /evt/user message.");
                    await mqttClient.PublishAsync(mqttSettings, CancellationToken.None);
                    bool goBack = false;
                    while (!goBack)
                    {
                        string readGoBack = "";
                        Console.Clear();
                        Console.WriteLine("Success! Enter 9 to go back to menu.");
                        readGoBack = Console.ReadLine();
                        if (readGoBack == "9")
                        {
                            goBack = true;
                            choice = "";
                        }
                    }
                }
                else if (choice == "9")
                {
                    var turnOff = new MqttApplicationMessageBuilder()
                        .WithTopic($"sharc/{SharcID}/evt/avail")
                        .WithPayload("{\"seq\": 6, \"v\": false}")
                        .Build();
                    Console.Clear();
                    // Console.WriteLine($"Sending avail false as {SharcID}.");
                    await mqttClient.PublishAsync(turnOff, CancellationToken.None);
                    keepRunning = false;
                }
            } while (keepRunning);
        }
    }

    class Program
    {
        static async Task Main(string[] args)
        {
            Sharc sharc = new Sharc();
            var result = await sharc.SharcMenu();
            await sharc.EstablishConnection(result.SharcID, result.BrokerConnection);
        }
    }
}