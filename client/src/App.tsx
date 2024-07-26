import React from 'react'
import { HStack, VStack, SimpleGrid, Heading, Text } from '@chakra-ui/react'
import { useQuery, QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Outlet, RouterProvider, createRouter, createRoute, createRootRoute } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

const queryClient = new QueryClient()

const rootRoute = createRootRoute({
  component: () => (
    <>
      <QueryClientProvider client={queryClient}>
        <Outlet />
        {false ? <TanStackRouterDevtools /> : ""}
      </QueryClientProvider>
    </>
  ),
})

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => <WebCowl />,
})

const routeTree = rootRoute.addChildren([indexRoute])
const router = createRouter({ routeTree })

function App() {
  return <RouterProvider router={router} />
}

function WebCowl() {
  return (
    <HStack spacing={4}>
      <DataBox bg="tan" header="Test Data">
        <Value label="Time" field="TIME" formatter={format_date} />
        <Value label="Frame" field="frame" formatter={String} />
        <Value label="Noise" field="NOISE" formatter={format_number(2)} />
        <Value label="Steppy" field="STEPPY" formatter={format_number(2)} />
      </DataBox>
    </HStack>
  )
}

function DataBox({ bg, header, children }: {bg: string, header: string, children?: React.ReactNode}) {
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

function format_date(value: number) {
  return (new Date(value * 1000)).toLocaleString()
}

function format_number(decimals: number, options = {}) {
  return (val: number) => val.toLocaleString(
    undefined,
    { minimumFractionDigits: decimals, maximumFractionDigits: decimals, ...options }
  )
}

const format_default = (val: number) => String(val)

function Value({ label, field, formatter=format_default}: {label: string, field: string, formatter: Function}) {
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

export default App
