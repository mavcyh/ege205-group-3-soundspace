import { Metadata } from "next";
import classes from "./page.module.css";
import { Title, Paper, Center, Stack, Text, Button, Group } from '@mantine/core';

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
        <Stack m="xl" style={{ width: '100%', maxWidth: 1200 }}>
          <Group grow align="stretch">
            <Paper withBorder shadow="xl" p="lg">
              <Text className={classes.subheading}>Room Status</Text>
              <Stack className={classes.status}>
                <Text className={classes.statustxt}><span style={{fontWeight: 'bold'}}>Humidity Level: </span>60%</Text>
                <Text className={classes.statustxt}><span style={{fontWeight: 'bold'}}>Door Status: </span>Closed</Text>
              </Stack>
            </Paper>
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
          <Paper withBorder shadow="xl" p="lg" className={classes.fullWidthPaper}>
            <Text className={classes.subheading}>Volume Graph</Text>
          </Paper>
        </Stack>
      </Center>
    </main>
  );
}
