import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  RouterProvider,
  createRouter,
  createRoute,
  createRootRoute,
} from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import { WebOwl } from "./pages/WebOwl";

const queryClient = new QueryClient();

const rootRoute = createRootRoute({
  component: () => (
    <>
      <QueryClientProvider client={queryClient}>
        <Outlet />
        {false ? <TanStackRouterDevtools /> : ""}
      </QueryClientProvider>
    </>
  ),
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => <WebOwl />,
});

const routeTree = rootRoute.addChildren([indexRoute]);
const router = createRouter({ routeTree });

function App() {
  return <RouterProvider router={router} />;
}

export default App;
