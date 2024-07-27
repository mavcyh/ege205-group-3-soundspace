import React from 'react'
import { Flex, Image, Box, Button, Group } from '@mantine/core'
import NextImage from 'next/image'
import logo from "@/assets/soundspace-logo.jpg"
import classes from "./Navbar.module.css"

export const Navbar = () => {
  return (
    <>
        <Box className={classes.Navbar}>
            <Flex justify='space-between'>
                <Image component={NextImage} src={logo} alt='logo' className={classes.logo}/>
                <Group className={classes.buttonsgroup}>
                    <Button className={classes.buttons} component='a' href='/admin'>Dashboard</Button>
                    <Button className={classes.buttons} component='a' href='/admin/custombooking'>Custom Booking</Button>
                    <Button className={classes.buttons} component='a' href='/admin/masterpassword'>Master Password</Button>
                </Group>
            </Flex>
        </Box>
    </>
  )
}

