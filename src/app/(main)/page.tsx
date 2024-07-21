import { Metadata } from "next";
import classes from "./page.module.css";
import { Flex } from "@mantine/core"
import { Hero } from "./_components/Hero/Hero";
import { BadgeCard1 } from "./_components/BadgeCard/BadgeCard1";
import { BadgeCard2 } from "./_components/BadgeCard/BadgeCard2";
import { BadgeCard3 } from "./_components/BadgeCard/BadgeCard3";
import { relative } from "path";

export const metadata: Metadata = {
  title: "SoundSpace | Home",
};

export default function Home() {
  return (
    <main> 
      <Hero/>
      <Flex style={{width: '100%'}} justify="space-around">
        <BadgeCard1/>
        <BadgeCard2/>
        <BadgeCard3/>
      </Flex>
    </main>
  );
}
