// Size of buffer of all sensor data and their timestamps
const size_t DATA_BUFFER_SIZE = 82;

// sensorData object and the data buffer share the same
// location in memory. Makes it easy to collect data 
// and ship it quickly.
union Data {
    struct DataStruct {
        byte beginPad[5]; // padding to easily find beginning
        byte  status;
        byte  pad1;
        long  acceleration;
        byte  pad2;
        long  velocity;
        byte  pad3;
        long  rpm;
        byte  pad4;
        long  position;
        byte  pad5;
        long  time;
        byte  pad6;
        long  battery_voltage;
        byte  pad7;
        long  battery_current;
        byte  pad8;
        long  battery_temperature;
        byte  pad9;
        long  temp1;
        byte  pad10;
        long  temp2;
        byte  pad11;
        long  temp3;
        byte  pad12;
        long  temp4;
        byte  pad13;
        long  temp5;
        byte  pad14;
        unsigned long stripe_count;
        byte  pad15;
        unsigned long pneumatics;
        byte  pad16;
    } sensorData;
    char buffer[DATA_BUFFER_SIZE];
} myData;

// run once at startup
void setup()
{
    // begin padding
    myData.sensorData.beginPad[0] = 0x41;
    myData.sensorData.beginPad[1] = 0x42;
    myData.sensorData.beginPad[2] = 0x43;
    myData.sensorData.beginPad[3] = 0x44;
    myData.sensorData.beginPad[4] = 0x45;
    myData.sensorData.pad1        = 0x00;
    myData.sensorData.pad2        = 0x00;
    myData.sensorData.pad3        = 0x00;
    myData.sensorData.pad4        = 0x00;
    myData.sensorData.pad5        = 0x00;
    myData.sensorData.pad6        = 0x00;
    myData.sensorData.pad7        = 0x00;
    myData.sensorData.pad8        = 0x00;
    myData.sensorData.pad9        = 0x00;
    myData.sensorData.pad10       = 0x00;
    myData.sensorData.pad11       = 0x00;
    myData.sensorData.pad12       = 0x00;
    myData.sensorData.pad13       = 0x00;
    myData.sensorData.pad14       = 0x00;
    myData.sensorData.pad15       = 0x00;
    myData.sensorData.pad16       = 0x00;

    // start serial
    Serial.begin(9600);
}

// runs continuously
void loop()
{
    // send the data buffer
    myData.sensorData.status = random(0,6);
    myData.sensorData.acceleration = random(-50,50);
    myData.sensorData.velocity = random(0,150);
    myData.sensorData.rpm = random(0,5603);
    myData.sensorData.position = random(0,5500);
    myData.sensorData.time = random(0,65);
    myData.sensorData.battery_voltage = random(0,16);
    myData.sensorData.battery_current = random(0,50);
    myData.sensorData.battery_temperature = random(0,150);
    myData.sensorData.temp1 = random(0,150);
    myData.sensorData.temp2 = random(0,150);
    myData.sensorData.temp3 = random(0,150);
    myData.sensorData.temp4 = random(0,150);
    myData.sensorData.temp5 = random(0,150);
    myData.sensorData.stripe_count = random(0,50);
    myData.sensorData.pneumatics = random(0,4096);

    Serial.write(myData.buffer, DATA_BUFFER_SIZE);

    // delay to give it time to send
    delay(1);
}
