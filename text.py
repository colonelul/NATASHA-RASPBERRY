import numpy as np

arr_temp = np.empty(9)
filter_data = "t0=123 t1=235 t2=12 t3=232t4=23t5=129t6=123t7=235t8=234"

print(filter_data)
for i in range(9):
    
    arr_temp[i] = filter_data[filter_data.find('t' + str(i) + '=') + 3 : filter_data.find('t' + str(i + 1))]

unsigned long t, dt;

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, 0);
  Serial.begin(9600);  // put your setup code here, to run once:

}

void loop() {
  t = millis();
  int i = 0;
  if (t >= dt) {
    String str;
    for ( byte i=0; i<9; i++)
    {
      byte xx = random(0,255);
      str = str + " t" + i + "=" + xx;
    }
    Serial.println(str);
    dt = t + 500;
  }

  if (Serial.available() > 0) {
    String incomingData = Serial.readString();
    incomingData.trim();
    String DataToSend = "Im: ";
    DataToSend = DataToSend + incomingData;
    Serial.print(DataToSend);

  }
}