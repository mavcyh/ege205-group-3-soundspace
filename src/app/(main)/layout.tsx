import { Navbar } from './_components/layout/Navbar/Navbar';
import { Footer } from "./_components/layout/Footer/Footer";

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
      <Footer/>
    </>
  );
}