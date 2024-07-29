import { Metadata } from "next";
import classes from "./page.module.css";
import { Title, Paper, Center, Stack, Text, Button, Group, Flex } from '@mantine/core';
import DoorStatus from "./_components/DoorStatus/DoorStatus";

export const metadata: Metadata = {
  title: "SoundSpace | Dashboard",
};

export default function AdminDashboard() { 
  return (
    <main>
      <Center>
        <Title my={50}>Admin Dashboard</Title>
      </Center>
      <Center>
        <Stack mb={50} style={{ width: '100%', maxWidth: 1200 }}>
          <Paper withBorder shadow="xl" p="lg">
            <Flex justify="space-between">
              <Text className={classes.subheading}>Room Status</Text>
              <DoorStatus/>
            </Flex>
            <Stack className={classes.graphContainer}>
              <Text className={classes.graphheading}>Humidity Graph</Text>
              <Text className={classes.graphheading}>Volume Graph</Text>
            </Stack>     
          </Paper>
          <Group grow align="stretch">
            <Paper withBorder shadow="xl" p="lg">
              <Text className={classes.subheading}>Locker 1</Text>
              <Text className={classes.instrumentname}>Fender Stratocaster</Text>
              <Text className={classes.weardesc}>wear value:</Text>
              <Text className={classes.wearvalue}>70%</Text>
              <Button fullWidth>Reset</Button>
            </Paper>
            <Paper withBorder shadow="xl" p="lg" className={classes.paper}>
              <Text className={classes.subheading}>Locker 2</Text>
              <Text className={classes.instrumentname}>Ibanez SR300E</Text>
              <Text className={classes.weardesc}>wear value:</Text>
              <Text className={classes.wearvalue}> 70%</Text>
              <Button fullWidth>Reset</Button>
            </Paper>
          </Group>
        </Stack>
      </Center>
    </main>
  );
}
