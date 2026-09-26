import { useState } from 'react';
import { Link, useLocation } from 'wouter';
import { useAuth } from '@/lib/auth';
import { 
  LayoutDashboard, 
  ScanLine, 
  Search, 
  History, 
  Stethoscope, 
  Calendar, 
  User, 
  LogOut, 
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export default function Layout({ children }: { children: React.ReactNode }) {
  const [location] = useLocation();
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', href: '/dashboard' },
    { icon: ScanLine, label: 'Skin Scan', href: '/scan' },
    { icon: Search, label: 'Disease Tips', href: '/search' },
    { icon: History, label: 'History', href: '/history' },
    { icon: Stethoscope, label: 'Doctor Consult', href: '/consult' },
    { icon: Calendar, label: 'Calendar', href: '/calendar' },
    { icon: User, label: 'Profile', href: '/profile' },
  ];

  if (!user) return <>{children}</>;

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex w-64 flex-col bg-white border-r border-slate-200 fixed h-full z-10">
        <div className="p-6 border-b border-slate-100 flex items-center gap-2">
          <div className="bg-primary/10 p-2 rounded-lg">
            <ScanLine className="h-6 w-6 text-primary" />
          </div>
          <h1 className="text-xl font-bold text-slate-900">DermaVision</h1>
        </div>
        
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive = location === item.href;
            return (
              <Link key={item.href} href={item.href}>
                <a className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 group",
                  isActive 
                    ? "bg-primary text-primary-foreground shadow-md shadow-primary/20" 
                    : "text-slate-600 hover:bg-slate-50 hover:text-primary"
                )}>
                  <item.icon className={cn("h-5 w-5", isActive ? "text-primary-foreground" : "text-slate-400 group-hover:text-primary")} />
                  {item.label}
                </a>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-100">
          <div className="flex items-center gap-3 px-4 py-3 mb-2">
            <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
              {user.name.charAt(0)}
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-semibold truncate text-slate-900">{user.name}</p>
              <p className="text-xs text-slate-500 truncate">{user.email}</p>
            </div>
          </div>
          <Button variant="outline" className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 border-red-100" onClick={logout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </aside>

      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 bg-white border-b border-slate-200 z-20 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="bg-primary/10 p-1.5 rounded-md">
            <ScanLine className="h-5 w-5 text-primary" />
          </div>
          <span className="font-bold text-lg">DermaVision</span>
        </div>
        <Button variant="ghost" size="icon" onClick={() => setMobileOpen(!mobileOpen)}>
          {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 bg-white z-10 pt-16 px-4 pb-4 flex flex-col">
          <nav className="space-y-2 flex-1">
            {navItems.map((item) => {
              const isActive = location === item.href;
              return (
                <Link key={item.href} href={item.href}>
                  <a 
                    onClick={() => setMobileOpen(false)}
                    className={cn(
                      "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all",
                      isActive 
                        ? "bg-primary text-primary-foreground" 
                        : "text-slate-600 hover:bg-slate-50"
                    )}
                  >
                    <item.icon className="h-5 w-5" />
                    {item.label}
                  </a>
                </Link>
              );
            })}
          </nav>
          <Button variant="outline" className="w-full mt-4 text-red-600 border-red-100" onClick={logout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 md:ml-64 min-h-screen p-4 md:p-8 pt-20 md:pt-8 overflow-x-hidden">
        <div className="max-w-6xl mx-auto animate-in fade-in duration-500">
          {children}
        </div>
      </main>
    </div>
  );
}
