The [Gateway Application](BLE-Gateway/BLE-Gateway-Python-Application/) is comprised of 3 python files: ***deviceManager.py***, ***d2cMsgSender.py*** and ***uartCentralGW.py***.		
     
- [deviceManager.py](BLE-Gateway/BLE-Gateway-Python-Application/deviceManager.py) is used to add a device to the ***Hub***. This is just a modified version (i.e. modified so that it works on Python 3.6.3) of the example here... [https://azure.microsoft.com/en-us/resources/samples/iot-hub-python-get-started/](https://azure.microsoft.com/en-us/resources/samples/iot-hub-python-get-started/).				
- [d2cMsgSender.py](BLE-Gateway/BLE-Gateway-Python-Application/d2cMsgSender.py) is used to generate the SAS Token. This is just a modified version (i.e. modified so that it works on Python 3.6.3) of the example here... [https://azure.microsoft.com/en-us/resources/samples/iot-hub-python-get-started/](https://azure.microsoft.com/en-us/resources/samples/iot-hub-python-get-started/).				
- [uartCentralGW.py](BLE-Gateway/BLE-Gateway-Python-Application/uartCentralGW.py) is the main application file. It's based on the example here... [https://kevinsaye.wordpress.com/2016/09/16/connect-to-azure-iot-hub-from-python/](https://kevinsaye.wordpress.com/2016/09/16/connect-to-azure-iot-hub-from-python/)

**Prerequisites:**		
 
- [Python 3.6.3](https://www.python.org/ftp/python/3.6.3/python-3.6.3.exe) is installed
- Install requests library (pip install requests)
- Install paho-mqtt library (pip install paho-mqtt)
- Install pyserial library (pip install pyserial)
- [Download the Baltimore Cyber Trust Root Certificate](https://ssl-tools.net/certificates/d4de20d05e66fc53fe1a50882c78db2852cae474.pem).
- Modify ***uartCentralGW.py*** so that ***BaltimoreCyberTrustRootCER*** path is set to the path where you stored the certificate
- Modify ***uartCentralGW.py*** so that ***connectionString*** is set to your ***Hub's Connection String***

**Usage:**		  
uartCentralGW.py `<serial port>` `<devicename>`   
`serial port`:  Serial port to use (e.g. COM8, use Windows Device Manager to determine port number)   
`devicename`: name of device (e.g. Sensor1) that will be added to the ***Hub***

When launched, the ***Gateway Application*** will send the scan command to the ***BLE UART Central Device***. The ***BLE UART Central Device*** will then scan for a ***Sensor*** that supports the ***Nordic UART Service***. If it successfully connects with the ***Sensor***, the ***Gateway Application*** will add the name of sensor to the ***Hub***, create a MQTT Client, connect to the ***Hub***, and then start sending temperature measurements to the ***Hub***.