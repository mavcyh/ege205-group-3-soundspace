import { Metadata } from 'next';
import classes from './page.module.css';
import { Dashboard } from './_components/Dashboard/Dashboard'
import { Title } from '@mantine/core';

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