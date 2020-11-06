import network
from umqtt.robust import MQTTClient 
import machine 
import time 
import dht
import ubinascii

from captive_portal import CaptivePortal

def deep_sleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  machine.deepsleep()

print("\n\n****Starting")

portal = CaptivePortal()
portal.start()

client_id = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(client_id=client_id, 
                    server="io.adafruit.com", user="andrew1977", password="aio_ynCC15LVE80vwXMiOlrE7alFF8iX", port=1883) 
client.connect()

d = dht.DHT22(machine.Pin(14))
try:
    d.measure()
except OSError as e:
    print("DHT measure error:")
    print(str(e))
else:

    t=d.temperature()
    h=d.humidity()

    print(t)
    print(h)

    client.publish(topic="andrew1977/feeds/dht22-temp", msg=str(t), qos=1)
    client.publish(topic="andrew1977/feeds/humidity", msg=str(h), qos=1)

#put the device to sleep, but leave enough time to manually stop the script
print("waiting to sleep")
time.sleep(5)
print("sleeping")
deep_sleep(300000)
