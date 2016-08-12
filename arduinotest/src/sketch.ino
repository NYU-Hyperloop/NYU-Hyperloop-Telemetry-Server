
// Size of buffer of all sensor data and their timestamps
const size_t DATA_BUFFER_SIZE = 10;

// sensorData object and the data buffer share the same
// location in memory. Makes it easy to collect data 
// and ship it quickly.
union Data {
    struct DataStruct {
        byte beginPad[2]; // padding to easily find beginning
        int data1;
        byte pad1;
        float data2;
        byte pad2;
    } sensorData;
    char buffer[DATA_BUFFER_SIZE];
} myData;

// run once at startup
void setup()
{
    // set dummy values
    myData.sensorData.beginPad[0] = 0x41;
    myData.sensorData.beginPad[1] = 0x42;
    myData.sensorData.data1 = 500;
    myData.sensorData.pad1 = 0x43;
    myData.sensorData.data2 = 2016.08;
    myData.sensorData.pad2 = 0x44;

    // start serial
    Serial.begin(9600);
}

// runs continuously
void loop()
{
    // send the data buffer
    Serial.write(myData.buffer, DATA_BUFFER_SIZE);

    // delay to give it time to send
    delay(100);
}
