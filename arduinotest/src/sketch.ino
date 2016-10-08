
// Size of buffer of all sensor data and their timestamps
const size_t DATA_BUFFER_SIZE = 60;

// sensorData object and the data buffer share the same
// location in memory. Makes it easy to collect data 
// and ship it quickly.
union Data {
    struct DataStruct {
        byte beginPad[5]; // padding to easily find beginning
        float yaw;
        byte  pad1;
        float pitch;
        byte  pad2;
        float roll;
        byte  pad3;
        float acceleration;
        byte  pad4;
        float velocity;
        byte  pad5;
        long  rpm;
        byte  pad6;
        long  position;
        byte  pad7;
        float temperature_inside;
        byte  pad8;
        float temperature_outside;
        byte  pad9;
        float temperature_electronics;
        byte  pad10;
        long time_remaining;
        byte  pad11;
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

    // start serial
    Serial.begin(9600);
}

// runs continuously
void loop()
{
    // send the data buffer
    myData.sensorData.yaw = random(0,360);
    myData.sensorData.pitch = random(-90,90);
    myData.sensorData.roll = random(-90,90);
    myData.sensorData.acceleration = random(-50,50);
    myData.sensorData.velocity = random(0,150);
    myData.sensorData.rpm = random(0,5603);
    myData.sensorData.position = random(0,5500);
    myData.sensorData.temperature_inside = random(0,150);
    myData.sensorData.temperature_outside = random(0,150);
    myData.sensorData.temperature_electronics = random(0,150);
    myData.sensorData.time_remaining = random(0,65);

    Serial.write(myData.buffer, DATA_BUFFER_SIZE);

    // delay to give it time to send
    delay(100);
}
