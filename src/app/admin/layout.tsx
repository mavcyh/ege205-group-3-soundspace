import { Metadata } from "next";
import { Navbar } from "./_components/layout/Navbar/Navbar";

export const metadata: Metadata = {
  title: "SoundSpace | Admin",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Navbar/>
      <main>
        {children}
      </main>
    </>
  );
}