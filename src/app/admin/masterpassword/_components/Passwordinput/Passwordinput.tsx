"use client"
import { useForm } from '@mantine/form';
import { PasswordInput, Flex, Button } from '@mantine/core';
import classes from "./Passwordinput.module.css"

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
    return(
        <form onSubmit={form.onSubmit((values) => console.log(values))}>
            <PasswordInput
                className={classes.password}
                label="Set Master Password"
                placeholder="Enter master password"
                size='lg'
                required
                {...form.getInputProps('password')}
            />
            <Flex justify="flex-end">
                <Button type="submit" className={classes.button}>Confirm</Button>
            </Flex>
        </form>       
)}