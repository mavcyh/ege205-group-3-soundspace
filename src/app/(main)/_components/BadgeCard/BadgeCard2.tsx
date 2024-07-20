"use client"
import { Card, Image, Text, Group, Badge, Button } from '@mantine/core';
import classes from './BadgeCard.module.css';
import NextImage from 'next/image'
import musicInstruments from '@/assets/home-musicInstruments.jpg'


const data = {
  image:
    musicInstruments,
  title: 'Comfortable Environment',
  country: 'Well maintained',
  description:
    "Enjoy a clean and welcoming atmosphere, with a wide selection of musical instruments. Enhanced soundproofing ensures a quiet, private space free from external noise, while thoughtfully designed interiors with inspiring decor fuel your creativity. Additionally, you'll have access to amenities like a lounge area, refreshments, and high-speed internet, making your time in the studio as pleasant and productive as possible.",
  badges: [
    { emoji: '👍', label: 'Comfort' },
    { emoji: '🙆‍♀️', label: 'Clean' },
  ],
};

export function BadgeCard2() {
  const { image, title, description, country, badges } = data;
  const features = badges.map((badge) => (
    <Badge variant="light" key={badge.label} leftSection={badge.emoji}>
      {badge.label}
    </Badge>
  ));

  return (
    <Card withBorder radius="md" p="md" mt={30} className={classes.card} style={{width: '32%'}}>
      <Card.Section>
        <Image component={NextImage} src={image} alt={title} height={180} />
      </Card.Section>

      <Card.Section className={classes.section} mt="md">
        <Group justify="apart">
          <Text fz="lg" fw={500}>
            {title}
          </Text>
          <Badge size="sm" variant="light">
            {country}
          </Badge>
        </Group>
        <Text fz="sm" mt="xs" className={classes.description}>
          {description}
        </Text>
      </Card.Section>

      <Card.Section className={classes.section}>
        <Text mt="md" className={classes.label} c="dimmed">
          
        </Text>
        <Group gap={7} mt={5}>
          {features}
        </Group>
      </Card.Section>

      <Group mt="xs">
        <Button radius="md" style={{ flex: 1 }} color='dark' component='a' href='/bookings'>
          Book now!
        </Button>
      </Group>
    </Card>
  );
}