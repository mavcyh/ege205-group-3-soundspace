import { Metadata } from "next";
import classes from "./page.module.css";
import { Hero } from "@/components/Hero/Hero";

export const metadata: Metadata = {
  title: "SoundSpace | Booking",
};

export default function Home() {
  return (
    <main>
      <Hero />
    </main>
  );
}
