'use client'
import { Flex, Stack, Paper, Center, Text, Group, Container, ScrollArea } from '@mantine/core';
import { IconAlertTriangle, IconAlertCircle, IconAlertSquareRounded } from '@tabler/icons-react'
import { AreaChart } from '@mantine/charts';
import { useState, useEffect } from 'react';
import classes from './Dashboard.module.css'
import { InstrumentData } from '../InstrumentData/InstrumentData';
import config from '@/config';

export function Dashboard() {
  // Consider setting useState default values to data fetched at the SERVER side: pass down props into Dashboard and use them here.
  const [volumeData, setVolumeData] = useState<{ time_stamp: string, volume_limit: number, volume_data: number }[]>([]);

  const [humidityData, setHumidityData] = useState<{ time_stamp: string, humidity_data: number }[]>([]);

  const [roomData, setRoomData] = useState<
  { room_door_status: 'CLOSED' | 'OPENED' | 'BROKEN INTO',
    instrument_data: {locker_id: string, instrument_name: string, wear_value:number, price_per_hour: number, usage: boolean}[],
    loitering_detected: boolean
    item_dropped: boolean
   }
  >({ room_door_status: 'CLOSED',
      instrument_data: [],
      loitering_detected: false,
      item_dropped: false
   })

   const [eventData, setEventData] = useState<{ timestamp: string, event_name: string, severity: number }[]>([]);

   const handleResetWear = async (lockerId: string) => {
    try {
      await fetch(`http://${config.apiServerIp}:5000/admin/reset-locker-wear`, {
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
        const humidityDataResponse : any = await fetch(`http://${config.apiServerIp}:5000/admin/humidity-data`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const newHumidityData : { time_stamp: string, humidity_data: number }[] = await humidityDataResponse.json();
        setHumidityData(newHumidityData);
        
        // Getting room data
        const roomDataResponse : any = await fetch(`http://${config.apiServerIp}:5000/admin/get-room-data`, {
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
        const volumeDataResponse : any = await fetch(`http://${config.apiServerIp}:5000/admin/session-volume-data`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ start_datetime: ""})
        });
        const newVolumeData : {time_stamp: string, volume_limit: number, volume_data: number}[] = await volumeDataResponse.json();
        setVolumeData(newVolumeData);

        // Getting event data
        const eventDataResponse : any = await fetch(`http://${config.apiServerIp}:5000/admin/get-events`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const newEventData: {
          timestamp: string,
          event_name: string,
          severity: number
        }[] = await eventDataResponse.json();
        setEventData(newEventData);
      }
      catch (error) {
        console.log(`Error connecting to API: ${error}`);
      }
    }

    const interval = setInterval(() => {
      fetchDashboardData();
    }, 1000)

    return () => {
      clearInterval(interval);
    };

  }, [])

  return (
    <Center>
      <Flex justify={'center'} align={'stretch'} pt={30}>
        <Container>
          <Stack mb={'-md'}>
            <Paper withBorder shadow="xl" p="lg">
              <Flex justify="space-between">
                <Text className={classes.subheading}>Room Status</Text>
                <Text style={{fontSize: '20px', fontWeight: 'bold'}}>
                  <span>Door Status: </span>
                  <span style={{color: roomData.room_door_status == 'BROKEN INTO' ? 'red' :
                                      roomData.room_door_status == 'OPENED' ? 'orange':
                                      'green'}}>
                    { roomData.room_door_status }
                  </span>
                  </Text>
              </Flex>
              <Stack className={classes.graphContainer}>
                <Text className={classes.graphheading}>Humidity Graph</Text>
                <AreaChart
                  pr={30}
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
                  yAxisProps={{domain: ['dataMin - 10', 'dataMax + 10']}}
                />
                <Text className={classes.graphheading}>Volume Graph</Text>
                {volumeData.length == 0 ? <Center><Text c={'gray'}>No Session Active</Text></Center>:
                <AreaChart
                  pr={30}
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
                  usage={instrument.usage}
                  instrument_name={instrument.instrument_name}
                  wear_value={instrument.wear_value}
                  onReset={handleResetWear}  // Pass the reset handler here
                />
              )}
            </Group>
          </Stack>
        </Container>
        <Container>
          <Paper withBorder shadow='xl' p="lg" h={'100%'}>
            <Text className={classes.subheading}>Events</Text>
            <ScrollArea m={10} bd={'xs'} miw={300}>
              {eventData.map(event => 
                <Container 
                className={event.severity == 2 ? classes.severity2: event.severity == 1 ? classes.severity1: classes.severity0}>
                  <Group className={classes.eventStack} justify="space-between"> 
                    <Group>
                      {event.severity == 2 ? <IconAlertTriangle/> :
                      event.severity == 1 ? <IconAlertSquareRounded/>:
                      <IconAlertCircle/>}
                      <text>{event.event_name}</text>
                    </Group>
                    <text>{event.timestamp}</text>
                  </Group>
                </Container>
              )}
            </ScrollArea>
          </Paper>
        </Container>
      </Flex>
    </Center>
  )
}