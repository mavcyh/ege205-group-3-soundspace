"use client"
import { useForm } from '@mantine/form';
import { PasswordInput, Flex, Button, Alert, Paper, Grid } from '@mantine/core';
import classes from "./Passwordinput.module.css";
import { useState,useEffect,useRef } from 'react';
import { IconAlertCircle } from '@tabler/icons-react';
import config from '@/config';


type FormValues = {
    password: string;
  };

export function Passwordinput() {
    const form = useForm({
      mode: 'uncontrolled',
      initialValues: {
          password: '',
      },
      validate: {
          password: (value) => (/^\d{6}$/.test(value) ? null : 'Password must be a 6 digit number.'),
      }
    })
    const [success, setSuccess] = useState<boolean | null>(null);

    const handleSubmit = async (values: FormValues) => {
        try {
        const response = await fetch(`http://${config.apiServerIp}:5000/admin/change-master-password`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ new_master_password: values.password }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
            
        }
        else if (response.ok) {
            setSuccess(true);
          }

        const data = await response.json();
        console.log('Success:', data);
        } catch (error) {
        console.error('Error:', error);
        }
    };

    return(
        <form onSubmit={form.onSubmit(handleSubmit)}>
            <PasswordInput
                className={classes.password}
                label="Set Master Password"
                placeholder="Enter new master password"
                size='lg'
                required
                {...form.getInputProps('password')}
            />
            {success &&
                <Alert icon={<IconAlertCircle size={16} />} title="Password Change Success!" color="green">
                    Your password has been successfully changed.
              </Alert>
            }
                 
            
            <Flex justify="flex-end">
                <Button type="submit" className={classes.button}>Confirm</Button>
            </Flex>
        </form>
)}