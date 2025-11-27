import { Switch, Route, useLocation } from "wouter";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";
import { Toaster } from "@/components/ui/toaster";
import { AuthProvider, useAuth } from "@/lib/auth";
import Layout from "@/components/Layout";

// Pages
import AuthPage from "@/pages/auth";
import Dashboard from "@/pages/dashboard";
import SkinScan from "@/pages/skin-scan";
import SearchTips from "@/pages/search-tips";
import History from "@/pages/history";
import Consult from "@/pages/consult";
import CalendarPage from "@/pages/calendar";
import Profile from "@/pages/profile";
import NotFound from "@/pages/not-found";

function ProtectedRoute({ component: Component, ...rest }: any) {
  const { isAuthenticated } = useAuth();
  const [, setLocation] = useLocation();

  if (!isAuthenticated) {
    // In a real app, we'd redirect here, but to avoid flickers on refresh during dev
    // we can just show the auth page or return null and let useEffect handle it
    // For now, let's render AuthPage if not authenticated for simplicity
    return <AuthPage />;
  }

  return (
    <Layout>
      <Component {...rest} />
    </Layout>
  );
}

function Router() {
  return (
    <Switch>
      <Route path="/auth" component={AuthPage} />
      <Route path="/dashboard">
        {() => <ProtectedRoute component={Dashboard} />}
      </Route>
      <Route path="/scan">
        {() => <ProtectedRoute component={SkinScan} />}
      </Route>
      <Route path="/search">
        {() => <ProtectedRoute component={SearchTips} />}
      </Route>
      <Route path="/history">
        {() => <ProtectedRoute component={History} />}
      </Route>
      <Route path="/consult">
        {() => <ProtectedRoute component={Consult} />}
      </Route>
      <Route path="/calendar">
        {() => <ProtectedRoute component={CalendarPage} />}
      </Route>
      <Route path="/profile">
        {() => <ProtectedRoute component={Profile} />}
      </Route>
      
      {/* Default Route */}
      <Route path="/">
        {() => {
          const { isAuthenticated } = useAuth();
          return isAuthenticated ? <ProtectedRoute component={Dashboard} /> : <AuthPage />;
        }}
      </Route>

      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router />
        <Toaster />
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
