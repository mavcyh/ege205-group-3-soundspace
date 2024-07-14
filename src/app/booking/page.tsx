import type { Metadata } from "next";
import classes from "./page.module.css";
import { Title } from '@mantine/core'

export const metadata: Metadata = {
    title: "SoundSpace | Booking",
  };

export default function Booking() {
  return (
    <main>
      <Title>This is the booking page.</Title>
    </main>
  );
}
