"use client"
import { Button, Checkbox, Group, TextInput, Container, Title, PasswordInput, Anchor, Paper, Center } from '@mantine/core';
import { useForm } from '@mantine/form';

export default function signIn() {
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
        username: '',
        email: '',
        password: '',
        termsOfService: false,
    },

    validate: {
        username: (value) => (value ? null : 'Username is required'),
        email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
        password: (value) => (value.length >= 8 ? null : 'Password must be at least 8 characters long'),
    }
  })

  return (
    <>       
        <Container size={500} mt={150} mb={220}>
            <Center>
                <Title size='h3'>Sign in</Title>
            </Center>
            
            <Paper withBorder shadow="md" p={30} mt={30} radius="md">
                <form onSubmit={form.onSubmit((values) => console.log(values))}>

                <TextInput
                    withAsterisk
                    label="Username"
                    placeholder="Your username"
                    key={form.key('username')}
                    required
                    {...form.getInputProps('username')}
                /> 

                <TextInput
                    label="Email"
                    placeholder="you@example.com"
                    required
                    mt="md"
                    {...form.getInputProps('email')}
                />

                <PasswordInput
                    label="Password"
                    placeholder="Your password"
                    required
                    mt="md"
                    {...form.getInputProps('password')}
                />
                <Group justify='flex-end' mt="lg">
                    <Anchor href="#" size="sm">
                        Forgot password?
                    </Anchor>
                </Group>

                <Checkbox
                    mt="md"
                    label="I agree to terms and conditions"
                    key={form.key('termsOfService')}
                    color='orange'
                    required
                    {...form.getInputProps('termsOfService', { type: 'checkbox' })}
                />

                <Group justify="flex-end" mt="md">
                    <Button type="submit" color='orange'>Submit</Button>
                </Group>
                </form>
            </Paper>
        </Container>    
    </> 
  )
}