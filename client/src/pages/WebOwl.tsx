import { HStack } from '@chakra-ui/react'
import { OwlBox } from '../components/OwlBox'
import { OwlValue, format_date, format_number } from '../components/OwlValue'

export function WebOwl() {
  return (
    <HStack spacing={4}>
      <OwlBox bg="tan" header="Test Data">
        <OwlValue label="Time" field="TIME" formatter={format_date} />
        <OwlValue label="Frame" field="frame" formatter={String} />
        <OwlValue label="Noise" field="NOISE" formatter={format_number(2)} />
        <OwlValue label="Steppy" field="STEPPY" formatter={format_number(2)} />
      </OwlBox>
    </HStack>
  )
}


