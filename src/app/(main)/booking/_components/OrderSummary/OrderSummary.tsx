import { useForm } from "@mantine/form";
import { Paper, Divider, Button, Text, Center, Title, List, TextInput } from "@mantine/core";
import classes from './OrderSummary.module.css';

interface Instrument {
  locker_id: string,
  instrument_name: string,
  price_per_hour: number
}

export const OrderSummary = ({selectedChips, selectedInstruments}:
  { selectedChips: {startChip: Date | null, endChip: Date | null},
    selectedInstruments: Instrument[]}) => {

const form = useForm({
  mode: 'uncontrolled',
  initialValues: {
      email: '',
  },

  validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
  }
})

  return (
    <Paper withBorder shadow="xl" pb={30} pt={30} mt={15} pos='relative'
    style={{ width: '500px', height: '710px', borderColor: 'orange' }}
    radius="md"
    >
      <Center><Title size='h4' mt={10}>Order Summary</Title></Center>
      <List className={classes.list}>
          {selectedInstruments.map((selectedInstrument) => (
              <>
                  <List.Item key={selectedInstrument.locker_id} className={classes.id}>{selectedInstrument.instrument_name}</List.Item>
                  <List.Item key={selectedInstrument.price_per_hour} className={classes.price}>${selectedInstrument.price_per_hour.toFixed(2)}/hour</List.Item>
              </>
          ))}
      </List>
      <Divider className={classes.divider} my={20}/>
      <form onSubmit={form.onSubmit((values) => console.log(values))}>
          <Button className={classes.book} type="submit" color='blue'>Book</Button>
      </form> 
      <Text className={classes.total}>
        <span style={{fontWeight: 'bold'}}>Total:</span>
        ${selectedInstruments.reduce((acc, selectedInstrument) => acc + selectedInstrument.price_per_hour, 0).toFixed(2)}
      </Text>
      <Center>
        <TextInput
        className={classes.email}
        size='md'
        label="Email"
        placeholder="you@example.com"
        required
        mt="md"
        {...form.getInputProps('email')}
        />   
      </Center>  
    </Paper>
  )
}