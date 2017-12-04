#define DEBUG false

//Await for next byte
void awaitSerial(unsigned int wait) {
  unsigned long timeBuf = millis();
  while (!(Serial.available() > 0))
  {
    if((millis() - timeBuf) > wait)
     return;
  }
  return;
}
//Clean the serial Buffer
void flushSerial() {
	while(Serial.available() > 0)
		Serial.read();
}
/*Send AT command with paramenter on a String to UART and return
 * the response*/
String sendData(String command, const int timeout, boolean debug)
{
  // Envio dos comandos AT para o modulo
  String response = "";
  Serial.print(command);
  unsigned long int time = millis();
  while ( (time + timeout) > millis())
  {
    while (Serial.available())
    {
      // The esp has data so display its output to the serial window
      char c = Serial.read(); // read the next character.
      response += c;
    }
  }
  if (debug)
  {
    Serial.print(response);
  }
  return response;
}
//Init ESP01 to be a UDP Server
void initESP()
{
	//Set multiple connections, needed for AP mode
	flushSerial();
	sendData("AT+CIPMUX=1\r\n",500,DEBUG);
	delay(1000);
	//Set Access Point Mode
	flushSerial();
	sendData("AT+CWMODE=2\r\n",500,DEBUG);
	delay(1000);
	//Set configuration for server, name, password..
	flushSerial();
	sendData("AT+CWSAP=\"Besourino01\",\"1234\",5,0\r\n",500,DEBUG);
	delay(1000);
	//Start server...
	flushSerial();
	delay(100);
	sendData("AT+CIPSERVER=1\r\n",500,DEBUG);
	delay(1000);
}
//Check if the serial connection between MCU and ESP01 is fine
bool connectionTest() {
	String ok = "";
	int i = 0;
	for (i = 0; i < 10; i++) {
		ok = sendData("AT\r\n",500,DEBUG);
		if (ok[ok.length() - 4] == 'O' &&  ok[ok.length() - 3] == 'K')
			return(true);
		delay(500);
	}
	return(false);
}
//Check if there is a incoming UDP packet, no: -1, yes: size of packet
int isThereData()
{
	char msg = 0;
	char nBytes = 0;
	char count = 1;
	int size = 0;
	if (Serial.available() > 0) {
		msg = Serial.read();
		//First time connection "Link" is on the message
		if( msg == 'L')
			for(int c = 0; c <=4; c++) {
				msg = Serial.read();
				awaitSerial(500);
		}
		//Remove non visable characters of msg
		while(msg <= 32) {
			delay(10);
			if (Serial.available() > 0)
				msg = Serial.read();
			else
				return -1;
		}
		if(msg != '+')
			return -1;

		awaitSerial(500);
		msg = Serial.read();
		if(msg != 'I')
			return -1;

		awaitSerial(500);
		msg = Serial.read();
		if(msg != 'P')
			return -1;

		awaitSerial(500);
		msg = Serial.read();
		if(msg != 'D')
			return -1;

		awaitSerial(500);
		msg = Serial.read();
		if(msg != ',')
			return -1;

		awaitSerial(500);
		Serial.read();

		awaitSerial(500);
		msg = Serial.read();
		if(msg != ',')
			return -1;

		awaitSerial(500);
		nBytes = Serial.read();
		while(nBytes != ':')
		{
		   size  *= count;
		   size  += (nBytes - '0');
		   count *= 10;
		   awaitSerial(500);
		   nBytes = Serial.read();
		}
		return size;
	}
	else
		return 0;
}

//Read UDP packet itself, and return a string of data
String readUDPacket(int size) {
	String data = "";
	char byte = 0;
	for (unsigned char n = 0; n < size; n++)
	{
		byte = Serial.read();
		data += byte;
	}
	return(data);
}
