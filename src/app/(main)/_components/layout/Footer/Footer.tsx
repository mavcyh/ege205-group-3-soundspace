"use client"
import { Text } from '@mantine/core'
import classes from './Footer.module.css'

export function Footer() {
  return (
    <footer className={classes.footer}>
      <Text size='sm' style={{color: 'grey'}}>
        © {new Date().getFullYear()} SoundSpace. All rights reserved.
      </Text>
    </footer>
  );
}