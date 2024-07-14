import { Overlay, Container, Title, Button, Text } from '@mantine/core';
import classes from './Hero.module.css';

export function Hero() {
  return (
    <div className={classes.hero}>
      <Overlay
        gradient="linear-gradient(180deg, rgba(0, 0, 0, 0.25) 0%, rgba(0, 0, 0, .65) 40%)"
        opacity={1}
        zIndex={0}
      />
      <Container className={classes.container} size="md">
        <Title className={classes.title}>An affordable music studio.</Title>
        <Text className={classes.description} size="xl" mt="xl">
          Our studio is fully automated: and mantainence is only done when it has to be done, meaning that we can pass on the savings to you.
        </Text>

        <Button variant="gradient" size="xl" radius="xl" className={classes.control}>
          Book Now
        </Button>
      </Container>
    </div>
  );
}