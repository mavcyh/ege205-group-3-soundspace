"use client"
import { Navbar } from "@/components/Navbar";
import { Container, Title, Text, Image, Center, Flex, Group } from '@mantine/core'
import aboutUsGuitar from '../../assets/aboutus-guitar.jpg'
import NextImage from 'next/image'
import { Footer } from "@/components/Footer/Footer";

export default function About() {
    return(
        <>
            <Navbar/>
            <Container mt={10} >
                <Center>
                    <Title size="h3" mt={40}>About Us</Title>
                </Center>
                <Text mt={10} style={{textAlign: 'center'}}>
                    We are a premier music studio rental service dedicated to providing musicians,
                    producers, and artists with the best possible environment to create and produce music.
                    Founded in 2024, SoundSpace was established by Maverick Chin with a passion for 
                    music and a vision to provide top-notch facilities for music production. Over the years,
                    we have grown to become a trusted name in the industry.
                </Text> 
                    <Center>
                        <Title size="h3" mt={40} mb={10}>Our Mission</Title>
                    </Center>
                    <Group mt={5}>
                        <Image component={NextImage} src={aboutUsGuitar} alt='aboutUsGuitar' 
                        h={300} ml={315} fit='contain' w="auto" style={{paddingTop: '8px', borderRadius: '1000px'}}/>
                    </Group>
                    <Group>
                        <Text style={{textAlign: 'center'}} mt={30}>
                            At SoundSpace, our mission is to provide a premier music studio experience that
                            empowers musicians, producers, and artists to achieve their creative vision. We 
                            are dedicated to offering state-of-the-art facilities equipped with the latest 
                            technology, ensuring exceptional sound quality and versatility for every project.
                            Committed to fostering a supportive and inspiring environment, we prioritize 
                            innovation, professionalism, and community engagement. Whether you're recording
                            your next album, rehearsing with your band, or mastering your tracks, we strive 
                            to be your trusted partner in musical excellence. Join us at SoundSpace and 
                            elevate your music to new heights.
                        </Text> 
                    </Group>
            </Container>
            <Footer/>
        </>
    );
}
