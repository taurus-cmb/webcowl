import { Text, Tr, Td } from '@chakra-ui/react'
import { useSharedData } from '../contexts/SharedDataProvider'

export function format_date(value: number) {
  return (new Date(value * 1000)).toLocaleString()
}

export function format_number(decimals: number, options = {}) {
  return (val: number) => val.toLocaleString(
    undefined,
    { minimumFractionDigits: decimals, maximumFractionDigits: decimals, ...options }
  )
}

const format_default = (val: number) => String(val)

function format_undefined_wrapper(val: number, formatter: Function) {
  if (val === undefined) {
    return "undefined"
  } else {
    return formatter(val)
  }
}

export function OwlValue({ label, field, formatter = format_default }: { label: string, field: string, formatter: Function }) {
  const { isLoading, isError, data } = useSharedData(field);

  return (
    <Tr>
      <Td p={1}><Text>{label}</Text></Td>
      <Td p={1}><Text>
        {isLoading ? "Loading..." : isError ? "Error..." : format_undefined_wrapper(data[field], formatter)}
      </Text></Td>
    </Tr>
  )
}


