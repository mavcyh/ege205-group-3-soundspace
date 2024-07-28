"use client";
import {
  Title,
  Button,
  Text,
  Paper,
  Flex,
  Grid,
  Table,
  rem,
  ScrollArea,
  Group,
  Stack,
  Divider,
  Modal,
  Alert,
  Loader,
} from "@mantine/core";
import { IconInfoCircle, IconAlertCircle } from "@tabler/icons-react";
import classes from '../page.module.css'
import { LineChart, AreaChart, BarChart } from "@mantine/charts";
import { notifications } from "@mantine/notifications";
import { useFullscreen } from "@mantine/hooks";
import { useState, useEffect, useRef } from "react";
import { connect, io } from "socket.io-client";

const socket = io("http://localhost:5000");

export function Adminfetch() {
  const icon = <IconAlertCircle />;
  const [data, setData] = useState<any>([]);
  const latestDataRef = useRef<any>(null);
  const [dataReset, setResetData] = useState<any>('');
  const latestDataRefReset = useRef<any>(null);
  const [dataW, setDataW] = useState<any>([]);
  const latestDataRefW = useRef<any>(null);
  const [dataE, setDataE] = useState<any>([]);
  const latestDataRefE = useRef<any>(null);



  const handleReset = async () => {
    try {
      const response = await fetch("http://localhost:5000/admin/reset-locker-wear", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ 'locker_id': '1' })  
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      setResetData(result);
      latestDataRefReset.current = result;
    } catch (error) {
      console.error("Error resetting locker wear:", error);
    }
  };


  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/admin/current-session-volume-data", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ start_datetime: ""}),  // Sending an empty body
        });
  
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
  
        const result = await response.json();
        setData(result);
        latestDataRef.current = result;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
  

    const fetchDataW = async () => {
      try {
        const response = await fetch("http://localhost:5000/admin/get-locker-wear", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const result = await response.json();
        setDataW(result);
        latestDataRefW.current = result;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    fetchDataW();

    const interval = setInterval(() => {
      fetchData();
      fetchDataW();
    }, 50);

    return () => {
      clearInterval(interval);
    };
  }, []); 

  useEffect(() => {
    socket.on("events", (newData) => {
      latestDataRefE.current = newData;
      setDataE(newData);
    });

    return () => {
      socket.off("events"); // Ensure to remove the correct event listener
      socket.disconnect(); // Clean up the socket connection on component unmount
    };
  }, []);

    // Assuming `socket` is defined somewhere in your component
    

  return (
    <div>
      <Paper
        p="md"
        shadow="sm"
        withBorder
        mt={24}
        radius="md"
        className={classes.gradBorder}
      >
        <Text
          fw={900}
          variant="gradient"
          gradient={{ from: "blue", to: "green", deg: 180 }}
          fz={rem(50)}
          ml={250}
        >
          Sound graph:
        </Text>
          <AreaChart
            h={350}
            w={900}
            data={data}
            dataKey="time_stamp"
            tickLine="xy"
            gridAxis="xy"
            series={[
              { name: "volume_data", color: "green.6" },
              {
                name: "volume_limit",
                color: "grape.5",
                strokeDasharray: "3 5",
              },
            ]}
            curveType="monotone"
            connectNulls
            tooltipAnimationDuration={100}
            strokeDasharray="5 25"
            fillOpacity={0.5}
            xAxisLabel="Date"
            yAxisLabel="Volume"
          />
      </Paper>

      <Paper
        p="md"
        shadow="sm"
        withBorder
        mt={24}
        radius="md"
        className={classes.gradBorder}
      >
        <Text
          fw={900}
          variant="gradient"
          gradient={{ from: "blue", to: "green", deg: 180 }}
          fz={rem(50)}
          ml={150}
        >
          API Data:
        </Text>
        <Group justify="center">
          <Text
            size="xl"
            fw={900}
            variant="gradient"
            gradient={{ from: "blue", to: "cyan", deg:90 }}>
                
                Latest F Strat Value:{dataW && dataW.wear_value && dataW.wear_value.length > 1 ? JSON.stringify(dataW.wear_value[0]) : <Loader size={20} color="lime" />}
          </Text>
          <Text
            size="xl"
            fw={900}
            variant="gradient"
            gradient={{ from: "blue", to: "cyan", deg:90 }}>
                
                Latest Event Value:{dataE}
          </Text>
          <Button
            variant="gradient"
            gradient={{ from: "blue", to: "cyan", deg: 90 }}
            leftSection={icon}
            onClick={handleReset}
          >
            Reset
          </Button>

        </Group>
      </Paper>
    </div>
  );
}

//TODO: (Non of this does actual shit yet)
// AreaChart on volume showing from 1 to 100*
// Gradient Linechart on humidity 1 to 100%
// text to show each instrument registered wear and tear 0% - 100% *
// button to reset the text specific instrument
// Alert whenever a instrument condition is poor (< 10)
// Notification to send alert across to show in admin
// additonal css to add gradient styling(rachels job)*
// All this are done on some paper affected by a typical dashboard layout using flex and grid(rachels job)*
// text counter on number of alerts that has been sent throughout 1 session,resets on the next session
// FETCH STUFF FOR DATA,leave some stuff empty just name what u want to send...
//Optional:
/*
Using NextAuth , can sign in to the gmail to go in to admin(Very messy not going to do that)
OR
Add a conditional routing that 1st asks for password in order to enter the page we want(Not that good and may subject to changes)
*/
/*
Contingency Plan:
"Push to maverick or rachel tho NOT RECOMMENDED"
"Bear thru pain in the nightless"
General ref...
Turn on far horizons skyrim theme
RESET BUTTON SETS THE VALUE To 10 again and the program keeps running
if else statement on warning when value if below a warning sent by alert in a modal is made

*/