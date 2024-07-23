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
        <TimeValue label="Time" field="TIME" />
        <Value label="Frame" field="frame" />
        <Value label="Noise" field="NOISE" />
        <Value label="Steppy" field="STEPPY" />
      </DataBox>
    </HStack>
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
function Value({ label, field }) {
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
        {isLoading ? "Loading..." : isError ? "Error: " + error : data[field]}
      </Text>
    </>
  )
}

function TimeValue({ label, field }) {
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
        {isLoading ? "Loading..." : isError ? "Error: " + error
          : (new Date(data[field] * 1000)).toLocaleString()}
      </Text>
    </>
  )
}

export default App
