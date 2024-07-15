import { Metadata } from "next";
import classes from "./page.module.css";
import { Flex } from "@mantine/core"
import { Hero } from "@/components/Hero/Hero";
import { Navbar } from "@/components/Navbar";
import { BadgeCard } from "@/components/BadgeCard/BadgeCard";
import { Footer } from "@/components/Footer/Footer";

export const metadata: Metadata = {
  title: "SoundSpace | Booking",
};

export default function Home() {
  return (
    <main>
      <Navbar/>
      <Hero/>
      <Flex>
        <BadgeCard/>
        <BadgeCard/>
        <BadgeCard/>
      </Flex>
      <Footer/>
    </main>
  );
}
