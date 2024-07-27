import { Metadata } from "next";
import classes from "./page.module.css";
import { Flex, Center, Image, Group } from "@mantine/core"
import { Hero } from "./_components/Hero/Hero";
import NextImage from 'next/image'
import logo from '@/assets/soundspace-logo.jpg'
import { BadgeCard1 } from "./_components/BadgeCard/BadgeCard1";
import { BadgeCard2 } from "./_components/BadgeCard/BadgeCard2";
import { BadgeCard3 } from "./_components/BadgeCard/BadgeCard3";

export const metadata: Metadata = {
  title: "SoundSpace | Home",
};

export default function Home() {
  return (
    <main> 
      <Hero/>
      <Flex  justify="center">
        <Image component={NextImage} src={logo} alt="logo" className={classes.image}/>
      </Flex>
      <Center> 
        <p className={classes.desc}>Welcome to SoundSpace, your premier destination for music studio rentals. 
        Whether you're a seasoned professional or an aspiring artist, our state-of-the-art facilities 
        are designed to inspire creativity and help you achieve your musical dreams. Our studios are 
        equipped with top-of-the-line instruments, cutting-edge recording technology, and a comfortable
        environment to ensure you have everything you need for a successful session. Book your time with
        us today and experience the perfect blend of innovation, comfort, and quality that sets us apart
        in the music industry.</p>
      </Center>
      <Flex className={classes.badges}>
        <Group grow align="stretch" p={'0 30px'}> 
          <BadgeCard1/>
          <BadgeCard2/>
          <BadgeCard3/>
        </Group>
      </Flex>
    </main>
  );
}
