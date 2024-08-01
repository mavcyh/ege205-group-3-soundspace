import { Metadata } from 'next';
import { Dashboard } from './_components/Dashboard/Dashboard'

export const metadata: Metadata = {
  title: "SoundSpace | Dashboard",
};

export default function AdminDashboard() { 
  return (
    <>
      <Dashboard />
    </>
  );
}