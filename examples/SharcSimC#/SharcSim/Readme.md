# Sharc Simulator
This is built using .NET8.0 to simulate a SHARC connecting to a broker and publishing payloads

## NOTE: This cannot simulate all SHARC payloads currently and only is available for MQTT

## Tutorial
1. Enter a "SHARC" ID, you can make this whatever you want.
2. Enter your broker connection string following broker_ip:port format.
   1. Example: wss.sharc.tech:9001
3. Select an option from the list
   1. Simulate PNP Part Count 1-X: Allows you to simulate a part count coming in on S0
   2. Simulate NPN Part Count 1-X: Allows you to simulate a part count coming in on S1
   3. Simulate Voltage: Allows you to simulate 0-10 volts coming in on S2
   4. Simulate Amperage: Allows you to simulate 4-20 mA coming in on S3
   7. Simulate Reboot: Allows you to simulate a SHARC rebooting
   8. Send all 'SHARC' settings: Will publish all information about the SHARC that one would normally publish
   9. Exit: Exits the program
4. That's it you are now simulating a SHARC!

## Steps to Build
1. Clone this repo
2. Ensure that you have .NET8.0 installed
3. CD into the repo
4. CD into SharcSim
5. Run command `dotnet build`
6. Locate the build folder and run the executable file

## Use Cases
1. You are waiting on your SHARC device and want to start integrating before it arrives
2. You want to see what information the SHARC contains
3. You want to see the capabilities of a SHARC before purchasing