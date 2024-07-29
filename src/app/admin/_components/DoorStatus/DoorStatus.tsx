// "use client"
import { useState } from "react";
import { Text } from "@mantine/core"

export default function DoorStatus() {
    // const [doorStatus, setDoorStatus] = useState("Closed");
    var doorStatus = "Closed";
    return(
        <Text style={{fontSize: '20px', fontWeight: 'bold'}}>
            <span>Door Status: </span>
            <span style={{color: doorStatus === "Closed" ? "red" : "green"}}>{doorStatus}</span>
        </Text>
    );
}