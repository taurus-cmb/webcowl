import { useState } from 'react'
import './App.css'
import { HStack, VStack, SimpleGrid, Heading, Text } from '@chakra-ui/react'
import { useQuery, useQueryClient, QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
  const [count, setCount] = useState(0)

  return (
    <QueryClientProvider client={queryClient}>
      <HStack spacing={4}>
        <DataBox bg="tan" header="Test Data">
          <Value label="Time" value="Mon May 25, 2025 10:25:31" />
          <Value label="Frame" value={2191} />
          <Value label="Noise" value={1.32} />
          <Value label="Steppy" value={22.98} />
        </DataBox>
      </HStack>
    </QueryClientProvider>
  )
}

// FIXME types
function DataBox({ bg, header, children }) {
  // TODO maybe build around Table instead?
  return (
    <VStack bg={bg} p={4} spacing={1}>
      <Heading as="h3" size="m">{header}</Heading>
      <SimpleGrid columns={2} columnGap={4}>
        {children}
      </SimpleGrid>
    </VStack>
  )
}

// FIXME types
function Value({ label, value }) {
  //const queryClient = useQueryClient();
  //const query = useQuery({queryKey: "test", queryFn=getTestData});
  
  return (
    <>
      <Text>{label}</Text>
      <Text>{value}</Text>
    </>
  )
}

export default App
