import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import '@mantine/core/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/charts/styles.css';
import '@mantine/notifications/styles.css';
import { ColorSchemeScript, MantineProvider } from '@mantine/core';
import { customTheme } from '@/app/customTheme';
const inter = Inter({ subsets: ["latin"] });
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer/Footer";

export const metadata: Metadata = {
  title: "SoundSpace",
  description: "EGE205-Group-3",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <ColorSchemeScript />
      </head>
      <body className={inter.className}>
        <MantineProvider theme={customTheme}>
          <Navbar/>
          {children}
          <Footer/>
        </MantineProvider>
      </body>
    </html>
  );
}