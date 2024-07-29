import React from 'react'
import { Center, Paper, Title } from "@mantine/core"
import { Passwordinput } from "./_components/Passwordinput/Passwordinput";
import classes from "./page.module.css"

export default function AdminPassword() {
    return(
        <>
            <Title className={classes.title}>Master Password</Title>
            <Center>
                <Paper withBorder shadow="md" radius="md" className={classes.paper}>
                    <Passwordinput/>
                </Paper>
            </Center>    
        </>  
    );
}