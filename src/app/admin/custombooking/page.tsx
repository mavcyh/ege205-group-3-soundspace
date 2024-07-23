import { Metadata } from "next";
import React from 'react'
import { Stack, Center, Paper, Button, Flex, Title } from "@mantine/core"
import { Datetimepicker } from "./_components/Datetimepicker/Datetimepicker";
import classes from "./page.module.css"

export const metadata: Metadata = {
    title: "SoundSpace | Admin Custom Booking",
  };

export default function AdminPassword() {
    return(
        <>
            <Title className={classes.title}>Custom Booking</Title>
            <Center>
                <Paper withBorder shadow="md" radius="md" className={classes.paper}>
                    <Stack>
                        <form>
                            <Datetimepicker label="Start Datetime"/>
                            <Datetimepicker label="End Datetime"/>
                            <Flex justify="flex-end">
                                <Button type="submit" className={classes.button}>Book</Button>
                            </Flex>
                        </form>  
                    </Stack>
                </Paper>
            </Center>  
        </>    
    );
}