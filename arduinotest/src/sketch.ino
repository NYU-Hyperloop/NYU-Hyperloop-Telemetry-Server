
// Size of buffer of all sensor data and their timestamps
const size_t DATA_BUFFER_SIZE = 6;

// sensorData object and the data buffer share the same
// location in memory. Makes it easy to collect data 
// and ship it quickly.
union Data {
    struct DataStruct {
        char beginPad[2]; // padding to easily find beginning
        char data1;
        char pad1;
        char data2;
        char pad2;
    } sensorData;
    char buffer[DATA_BUFFER_SIZE];
} myData;

// run once at startup
void setup()
{
    // set dummy values
    myData.sensorData.beginPad[0] = 0x41;
    myData.sensorData.beginPad[1] = 0x42;
    myData.sensorData.data1 = 0x43;
    myData.sensorData.pad1 = 0x44;
    myData.sensorData.data2 = 0x45;
    myData.sensorData.pad2 = 0x46;

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
