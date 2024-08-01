'use client'
import { Flex, Stack, Paper, Center, Text, Group, Button, Title } from '@mantine/core';
import { AreaChart } from '@mantine/charts';
import { useState, useEffect } from 'react';
import classes from './Dashboard.module.css'
import { InstrumentData } from '../InstrumentData/InstrumentData';

export function Dashboard() {
  // Consider setting useState default values to data fetched at the SERVER side: pass down props into Dashboard and use them here.
  const [volumeData, setVolumeData] = useState<{ time_stamp: string, volume_limit: number, volume_data: number }[]>([]);

  const [humidityData, setHumidityData] = useState<{ time_stamp: string, humidity_data: number }[]>([]);

  const [instrumentData, setInstrumentData] = useState<
  { locker_id: string, instrument_name: string, wear_value: number }[]
  >([]);

  const [roomData, setRoomData] = useState<
  { room_door_status: 'CLOSED' | 'OPENED' | 'BROKEN INTO',
    instrument_data: {locker_id: string, instrument_name: string, wear_value:number, price_per_hour: number, usage: boolean}[],
    loitering_detected: boolean
    item_dropped: boolean
   }
  >({ room_door_status: 'CLOSED',
    instrument_data: [{locker_id: '1', instrument_name: 'Fender Stratocaster', wear_value: 50, price_per_hour: 2.5, usage: false},
                      {locker_id: '2', instrument_name: 'Ibanez SR300E', wear_value: 70, price_per_hour: 1.5, usage: false}],
      loitering_detected: false,
      item_dropped: false
   })

   const handleResetWear = async (lockerId: string) => {
    try {
      await fetch("http://localhost:5000/admin/reset-locker-wear", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ locker_id: lockerId }),
      });
    } catch (error) {
      console.error(`Error resetting locker wear: ${error}`);
    }
  };

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        // Getting humidity data
        const humidityDataResponse : any = await fetch("http://localhost:5000/admin/humidity-data", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const newHumidityData = await humidityDataResponse.json();
        setHumidityData(newHumidityData);
        
        // Getting room data
        const roomDataResponse : any = await fetch("http://localhost:5000/admin/get-room-data", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const newRoomData: {
          room_door_status: 'CLOSED' | 'OPENED' | 'BROKEN INTO',
          instrument_data: { locker_id: string, instrument_name: string, wear_value: number, price_per_hour: number, usage: boolean }[],
          loitering_detected: boolean
          item_dropped: boolean
        } = await roomDataResponse.json();
        setRoomData(newRoomData);
        
        // Getting volume data
        const volumeDataResponse : any = await fetch("http://localhost:5000/admin/session-volume-data", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ start_datetime: ""})
        });
        const newVolumeData = await volumeDataResponse.json();
        setVolumeData(newVolumeData);
      }
      catch (error) {
        console.log(`Error connecting to API: ${error}`);
      }
    }

    const interval = setInterval(() => {
      fetchDashboardData();
    }, 1000)

    // DEBUGGING, SETTING PRE-DEFINED VALUES!
    setInstrumentData([{ locker_id: '1', instrument_name: 'Fender Stratocaster', wear_value: 50 },
                       { locker_id: '2', instrument_name: 'Ibanez SR300E', wear_value: 70 }
    ])

    return () => {
      clearInterval(interval);
    };

  }, [])

  return (
    <Flex justify={'center'} pt={30}>
      <Center>
        <Stack mb={50} style={{ flex: 1 }}>
          <Paper withBorder shadow="xl" p="lg">
            <Flex justify="space-between">
              <Text className={classes.subheading}>Room Status</Text>
              <Text style={{fontSize: '20px', fontWeight: 'bold'}}>
                <span>Door Status: </span>
                <span style={{color: roomData.room_door_status == 'BROKEN INTO' ? 'red' :
                                     roomData.room_door_status == 'OPENED' ? 'orange':
                                     'green'}}>
                  {roomData.room_door_status }
                </span>
                </Text>
            </Flex>
            <Stack className={classes.graphContainer}>
              <Text className={classes.graphheading}>Humidity Graph</Text>
              <AreaChart
                h={350}
                w={900}
                data={humidityData}
                dataKey="time_stamp"
                series={[
                  { name: "humidity_data", color: "blue.6" }
                ]}
                connectNulls
                withDots={false}
                xAxisLabel="Time"
                yAxisLabel="Humidity (%)"
                yAxisProps={{domain: ['50', 'dataMax + 10']}}
              />
              <Text className={classes.graphheading}>Volume Graph</Text>
              {volumeData.length == 0 ? <Text>No Session Active</Text> :
              <AreaChart
                h={350}
                w={900}
                data={volumeData}
                dataKey="time_stamp"
                tickLine="xy"
                gridAxis="xy"
                series={[
                  { name: "volume_data", color: "green.6" },
                  {
                    name: "volume_limit",
                    color: "red",
                    strokeDasharray: "3 5",
                  }
                ]}
                connectNulls
                withDots={false}
                xAxisLabel="Time"
                yAxisLabel="Volume Level"
              />
              }
              
            </Stack>     
          </Paper>
          <Group grow align="stretch">
            {roomData.instrument_data.map((instrument) =>
              <InstrumentData
                key={instrument.locker_id}  // Adding a key for better performance
                locker_id={instrument.locker_id}
                instrument_name={instrument.instrument_name}
                wear_value={instrument.wear_value}
                onReset={handleResetWear}  // Pass the reset handler here
              />
            )}
          </Group>
        </Stack>
      </Center>
    </Flex>
  )
}