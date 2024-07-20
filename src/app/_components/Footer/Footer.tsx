"use client"
import { Anchor, Group, ActionIcon, rem, Text, Box } from '@mantine/core'
import { IconBrandTwitter, IconBrandYoutube, IconBrandInstagram} from '@tabler/icons-react'
import classes from './Footer.module.css'
import Link from 'next/link'

const links = [
  { link: '/', label: 'Contact' },
  { link: '/about', label: 'About' },
  { link: '/bookings', label: 'Bookings' },
  { link: '/', label: 'Features' },    
  { link: '/', label: 'Dashboard' },
];

export function Footer() {
  const items = links.map((link) => (
    <Anchor
      component={Link}
      c="dimmed"
      key={link.label}
      href={link.link}
      lh={1}
      onClick={(event) => event.preventDefault()}
      size="sm"
    >
      {link.label}
    </Anchor>
  ));

  return (
    <footer className={classes.footer}>
      <Box className={classes.inner}>
        <Text size='sm' style={{color: 'grey'}}>
            © {new Date().getFullYear()} SoundSpace. All rights reserved.
        </Text>
        <Group className={classes.links} mr={115}>{items}</Group>

        <Group gap="xs" justify="flex-end" wrap="nowrap">
          <ActionIcon size="lg" variant="default" radius="xl">
            <IconBrandTwitter style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
          </ActionIcon>
          <ActionIcon size="lg" variant="default" radius="xl">
            <IconBrandYoutube style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
          </ActionIcon>
          <ActionIcon size="lg" variant="default" radius="xl">
            <IconBrandInstagram style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
          </ActionIcon>
        </Group>
      </Box>
    </footer>
  );
}