'use client'

import config from '@/config'
import { Button } from '@mantine/core'

export default function TestButton({ children, apiAddress }: { children: string, apiAddress: string }) {
    const testButtonClick = (apiAddress: string) => {
        fetch(`http://${config.apiServerIp}:5000/api/test/${apiAddress}`, {
          method: 'POST',
        })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
      }
    return (
        <Button onClick={() => testButtonClick(apiAddress)}>
            {children}
        </Button>
    )
}