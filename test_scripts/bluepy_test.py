from bluepy import btle
 
print("Connecting...")
dev = btle.Peripheral("40:06:a0:95:00:be")
 
print("Services...")
for svc in dev.services:
    print(str(svc))
#print(dev.rssi)
