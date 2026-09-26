import { Switch, Route, useLocation } from "wouter";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";
import { Toaster } from "@/components/ui/toaster";
import { AuthProvider, useAuth } from "@/lib/auth";
import Layout from "@/components/Layout";
import { Suspense, lazy } from "react";
import { Loader2 } from "lucide-react";

// Lazy Load Pages for Performance
const AuthPage = lazy(() => import("@/pages/auth"));
const Dashboard = lazy(() => import("@/pages/dashboard"));
const SkinScan = lazy(() => import("@/pages/skin-scan"));
const SearchTips = lazy(() => import("@/pages/search-tips"));
const History = lazy(() => import("@/pages/history"));
const Consult = lazy(() => import("@/pages/consult"));
const CalendarPage = lazy(() => import("@/pages/calendar"));
const Profile = lazy(() => import("@/pages/profile"));
const NotFound = lazy(() => import("@/pages/not-found"));

function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
    </div>
  );
}

function ProtectedRoute({ component: Component, ...rest }: any) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Suspense fallback={<PageLoader />}><AuthPage /></Suspense>;
  }

  return (
    <Layout>
      <Suspense fallback={<PageLoader />}>
        <Component {...rest} />
      </Suspense>
    </Layout>
  );
}

function Router() {
  return (
    <Switch>
      <Route path="/auth">
        <Suspense fallback={<PageLoader />}><AuthPage /></Suspense>
      </Route>
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
          return isAuthenticated ? 
            <ProtectedRoute component={Dashboard} /> : 
            <Suspense fallback={<PageLoader />}><AuthPage /></Suspense>;
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
