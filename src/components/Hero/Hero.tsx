import cx from 'clsx';
import { Title, Text, Container, Button, Overlay } from '@mantine/core';
import classes from './Hero.module.css';

export function Hero() {
  return (
    <div className={classes.wrapper}>
      <Overlay color="#000" opacity={0.65} zIndex={1} />

      <div className={classes.inner}>
        <Title className={classes.title}>
          Professional Music Studio Rentals{' '}
        </Title>

        <Container size={640}>
          <Text size="lg" className={classes.description}>
            Your perfect space for recording, rehearsing, and producing music.
          </Text>
        </Container>

        <div className={classes.controls}>
          <Button className={classes.control} color='orange' variant="white" size="lg" component='a' href='/bookings'> 
            Book now!
          </Button>
          <Button className={cx(classes.control, classes.secondaryControl)} size="lg" component='a' href='/about'>
            About us
          </Button>
        </div>
      </div>
    </div>
  );
}