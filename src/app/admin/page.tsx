import { Metadata } from "next";
import classes from "./page.module.css";
import { Title } from '@mantine/core';

export const metadata: Metadata = {
  title: "SoundSpace | Admin Dashboard",
};

export default function AdminDashboard() {
  return (
    <main>
      <Title>This is the admin dashboard page.</Title>
    </main>
  );
}