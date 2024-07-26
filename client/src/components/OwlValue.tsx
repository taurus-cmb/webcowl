import { Text } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'

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

export function OwlValue({ label, field, formatter = format_default }: { label: string, field: string, formatter: Function }) {
  // const queryClient = useQueryClient();
  const { isLoading, isError, data, error } = useQuery({
    queryKey: ["api_test"],
    queryFn: async () => {
      const response = await fetch("/api/test")
      if (!response.ok) {
        throw new Error("Could not get test data")
      }
      return response.json()
    },
    refetchInterval: 500,
  });

  return (
    <>
      <Text>{label}</Text>
      <Text>
        {isLoading ? "Loading..." : isError ? "Error: " + error : formatter(data[field])}
      </Text>
    </>
  )
}


