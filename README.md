# Final-Project-Assignment-8916
# Rideau Canal Skateway – Real-Time Monitoring System

##  Scenario Description

The **Rideau Canal Skateway**, a world-famous attraction in Ottawa, requires continuous monitoring to ensure safe skating conditions for the public. This project, commissioned by the **National Capital Commission (NCC)**, presents a **real-time data streaming system** designed to monitor ice and weather conditions across key canal locations.  

The system simulates IoT sensors, processes real-time data using **Azure IoT Hub** and **Stream Analytics**, and stores the results in **Azure Blob Storage** for further analysis and reporting.

---

##  System Architecture
![image](https://github.com/user-attachments/assets/ff91f932-27e3-4dba-9aed-3d696255393a)




###  Data Flow:

1. Simulated IoT sensors send JSON-formatted data every 10 seconds.
2. Azure IoT Hub receives and routes the telemetry.
3. Azure Stream Analytics processes and aggregates data in 5-minute windows.
4. Processed results are saved to Azure Blob Storage in JSON/CSV format.

---

##  Implementation Details

###  IoT Sensor Simulation

- **Locations**: Dow’s Lake, Fifth Avenue, NAC
- **Parameters**:
  - `iceThickness` (cm)
  - `surfaceTemperature` (°C)
  - `snowAccumulation` (cm)
  - `externalTemperature` (°C)
- **Frequency**: Every 10 seconds
- **Payload Example**:
```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2024-11-23T12:00:00Z"
}
```
- **Language**: Python with Azure IoT SDK
- **Script Path**: `/sensor-simulation/sensor_simulation.py`

---

###  Azure IoT Hub Configuration

- Created via Azure Portal
- Device registered: `Satyam8915`
- Connection string used in Python script
- Routes messages to default endpoint for processing

---

###  Azure Stream Analytics

- **Input**: Azure IoT Hub
- **Query**:
```sql
SELECT
    location,
    System.Timestamp AS windowEnd,
    AVG(CAST(iceThickness AS float)) AS avgIceThickness,
    MAX(CAST(snowAccumulation AS float)) AS maxSnowAccumulation
INTO
    [BlobOutput]
FROM
    [IoTHubInput]
TIMESTAMP BY timestamp
GROUP BY
    TumblingWindow(minute, 5),
    location
```

- **Output**: Azure Blob Storage (JSON or CSV)

---

##  Usage Instructions

### 1. Run IoT Sensor Simulation

1. Set up a Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install azure-iot-device
   ```

2. Insert your Azure IoT device connection string into the script.

3. Run the script:
   ```bash
   python sensor_simulation.py
   ```

---

### 2. Configure Azure Services

- **Azure IoT Hub**:
  - Create a new IoT Hub.
  - Register a new device (e.g., `canalSensorDevice`).
  - Copy connection string.

- **Azure Stream Analytics Job**:
  - Set input as IoT Hub.
  - Set output to Blob Storage.
  - Use the SQL query above.

- **Azure Blob Storage**:
  - Create storage account and blob container.
  - Link as output in Stream Analytics.

---

### 3. Access Stored Data

1. Go to Azure Portal > Storage Account
2. Open blob container (`iotoutput`)
3. Browse folders by date/location
4. Download JSON/CSV files to view aggregated results

---

## Results

### Sample Output (JSON):

```json
{
  "location": "Dow's Lake",
  "windowEnd": "2025-11-07T12:05:00Z",
  "avgIceThickness": 28.3,
  "maxSnowAccumulation": 10
}
```

### Findings:

- Data is accurately grouped in 5-minute windows.
- Aggregates (average thickness, max snow) allow quick condition assessment.
- Output ready for dashboards or reports.

---

## Reflection

### Challenges Faced:

- Connecting Python simulation to IoT Hub required correct device setup and connection string.
- Timestamps in payloads were essential for correct aggregation windows.

### Solutions:

- Thorough testing of the payloads and device client.
- Timestamp debugging using IoT Hub logs and Stream Analytics diagnostics.
- Verified blob storage outputs by downloading and inspecting sample files.





