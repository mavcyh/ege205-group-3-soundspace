import { Navbar } from "@/app/_components/Navbar/Navbar";
import { Footer } from "@/app/_components/Footer/Footer";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      <Navbar/>
        {children}
      <Footer/>
    </>
  );
}