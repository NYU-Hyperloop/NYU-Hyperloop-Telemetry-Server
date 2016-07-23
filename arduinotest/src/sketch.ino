
const size_t DATA_BUFFER_SIZE = 6;

union Data {
    struct DataStruct {
        char beginPad[2];
        char data1;
        char pad1;
        char data2;
        char pad2;
    } sensorData;
    char buffer[DATA_BUFFER_SIZE];
} myData;

void setup()
{
    myData.sensorData.beginPad[0] = 0x41;
    myData.sensorData.beginPad[1] = 0x42;
    myData.sensorData.data1 = 0x43;
    myData.sensorData.pad1 = 0x44;
    myData.sensorData.data2 = 0x45;
    myData.sensorData.pad2 = 0x46;

    Serial.begin(9600);
}

void loop()
{
    Serial.write(myData.buffer, DATA_BUFFER_SIZE);

    delay(100);
}
