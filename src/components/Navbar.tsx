import React from 'react'
import { Button, Group, Flex, Box, Image, createTheme, MantineProvider } from '@mantine/core'
import logo from "../assets/soundspace-logo.jpg"
import notifBell from '../assets/notifBell.png'
import NextImage from 'next/image'

const theme = createTheme({
  fontFamily: 'Open Sans, sans-serif',
});

export const Navbar = () => {

  return (
    <>
      <MantineProvider theme={theme}>
        <Box style={{borderBottom: '3px solid rgb(49, 49, 49) ', backgroundColor: 'white'}}>
          <Flex style={{height:'60px', padding:'2px'}}
              justify={'space-between'}
              wrap='wrap'>
            <Image component={NextImage} src={logo} alt='logo' h={50} fit='contain' w="auto" style={{paddingTop: '8px', paddingLeft:'20px'}}/>
            <Group style={{paddingRight: '50px'}}>
              <Button 
              variant="transparent" color="orange" size="md" component='a' href='/' 
              >Home</Button>
              <Button variant="transparent" color="orange" size="md" component='a' href='/about' 
              >About</Button>
              <Button variant="transparent" color="orange" size="md" component='a' href='/bookings' 
              >Bookings</Button>
              {/* <Button variant="transparent" color="orange" size="md" component='a' href='/admin' 
              >Dashboard</Button> */}
            </Group>     

            <Group>
              <Image component={NextImage} src={notifBell} alt='notifBell' h={20}/>      
              <Button variant="transparent" color="black" size="md" component='a' href='/signin' 
              >Sign In</Button>
            </Group>
          </Flex>
        </Box>
      </MantineProvider>    
    </>   
)}
