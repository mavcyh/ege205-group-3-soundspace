import { Metadata } from "next";
import classes from "./page.module.css";
import { Flex } from "@mantine/core"
import { Hero } from "@/app/(main)/_components/Hero/Hero";
import { BadgeCard1 } from "@/app/(main)/_components/BadgeCard/BadgeCard1";
import { BadgeCard2 } from "@/app/(main)/_components/BadgeCard/BadgeCard2";
import { BadgeCard3 } from "@/app/_components/BadgeCard/BadgeCard3";

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
