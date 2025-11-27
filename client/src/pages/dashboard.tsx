import { useAuth } from '@/lib/auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ScanLine, Calendar, Activity, ArrowRight } from 'lucide-react';
import { Link } from 'wouter';

export default function Dashboard() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Hello, {user.name}</h1>
          <p className="text-slate-500 mt-1">Welcome to your skin health dashboard.</p>
        </div>
        <Link href="/scan">
          <Button size="lg" className="shadow-lg shadow-primary/25">
            <ScanLine className="mr-2 h-5 w-5" />
            New Skin Scan
          </Button>
        </Link>
      </div>

      {/* Stats / Quick Info */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="border-slate-200 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-500">Last Scan</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900">Acne - Mild</div>
            <p className="text-xs text-slate-500 mt-1">2 days ago</p>
          </CardContent>
        </Card>

        <Card className="border-slate-200 shadow-sm hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-500">Upcoming Consult</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900">Dr. Sharma</div>
            <p className="text-xs text-slate-500 mt-1">Tomorrow, 10:00 AM</p>
          </CardContent>
        </Card>

        <Card className="bg-primary text-primary-foreground border-none shadow-lg shadow-primary/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-primary-foreground/80">Health Score</CardTitle>
            <Activity className="h-4 w-4 text-primary-foreground/80" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Good</div>
            <p className="text-xs text-primary-foreground/80 mt-1">Based on recent history</p>
          </CardContent>
        </Card>
      </div>

      {/* Actions Grid */}
      <h2 className="text-xl font-semibold text-slate-900 pt-4">Quick Actions</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: "Skin Scan", desc: "Analyze your skin condition", href: "/scan", icon: ScanLine, color: "text-blue-600", bg: "bg-blue-50" },
          { title: "Consult Doctor", desc: "Book an appointment", href: "/consult", icon: Activity, color: "text-teal-600", bg: "bg-teal-50" },
          { title: "Calendar", desc: "View schedule", href: "/calendar", icon: Calendar, color: "text-purple-600", bg: "bg-purple-50" },
          { title: "History", desc: "Past records", href: "/history", icon: Activity, color: "text-orange-600", bg: "bg-orange-50" },
        ].map((item) => (
          <Link key={item.title} href={item.href}>
            <a className="block group">
              <Card className="h-full transition-all duration-200 hover:border-primary/50 hover:shadow-md border-slate-200">
                <CardContent className="p-6 flex flex-col items-start gap-4">
                  <div className={`p-3 rounded-xl ${item.bg} ${item.color} group-hover:scale-110 transition-transform`}>
                    <item.icon className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-900 group-hover:text-primary transition-colors">{item.title}</h3>
                    <p className="text-sm text-slate-500 mt-1">{item.desc}</p>
                  </div>
                  <div className="mt-auto pt-2 text-sm font-medium text-primary flex items-center opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0">
                    Open <ArrowRight className="ml-1 h-3 w-3" />
                  </div>
                </CardContent>
              </Card>
            </a>
          </Link>
        ))}
      </div>
      
      <div className="bg-slate-900 rounded-2xl p-8 text-white relative overflow-hidden">
         <div className="relative z-10 max-w-2xl">
            <h3 className="text-2xl font-bold mb-2">Daily Tip</h3>
            <p className="text-slate-300 mb-4">Remember to apply sunscreen every 2 hours when outdoors, even on cloudy days.</p>
            <Button variant="secondary">Read More Tips</Button>
         </div>
         <div className="absolute right-0 top-0 h-full w-1/3 bg-gradient-to-l from-teal-600/20 to-transparent pointer-events-none" />
      </div>
    </div>
  );
}
