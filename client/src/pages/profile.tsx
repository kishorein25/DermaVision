import { useAuth } from '@/lib/auth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';

export default function Profile() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-slate-900">My Profile</h1>

      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="flex flex-row items-center gap-6">
          <Avatar className="h-24 w-24">
            <AvatarFallback className="text-2xl bg-primary/10 text-primary font-bold">
              {user.name.charAt(0)}
            </AvatarFallback>
          </Avatar>
          <div>
             <CardTitle className="text-2xl">{user.name}</CardTitle>
             <CardDescription>{user.email}</CardDescription>
             <Badge className="mt-2">Patient</Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label>Full Name</Label>
                <Input defaultValue={user.name} readOnly className="bg-slate-50" />
              </div>
              <div className="space-y-2">
                <Label>Email</Label>
                <Input defaultValue={user.email} readOnly className="bg-slate-50" />
              </div>
              <div className="space-y-2">
                <Label>Age</Label>
                <Input defaultValue={user.age} readOnly className="bg-slate-50" />
              </div>
              <div className="space-y-2">
                <Label>Gender</Label>
                <Input defaultValue={user.gender} readOnly className="bg-slate-50" />
              </div>
              <div className="space-y-2">
                <Label>City</Label>
                <Input defaultValue={user.city} readOnly className="bg-slate-50" />
              </div>
              <div className="space-y-2">
                <Label>Country</Label>
                <Input defaultValue={user.country} readOnly className="bg-slate-50" />
              </div>
           </div>
           <div className="flex justify-end">
              <Button>Edit Profile</Button>
           </div>
        </CardContent>
      </Card>
    </div>
  );

  function Badge({ children, className }: { children: React.ReactNode, className?: string }) {
      return <span className={`inline-flex items-center rounded-full border border-transparent bg-primary px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 text-primary-foreground hover:bg-primary/80 ${className}`}>{children}</span>
  }
}
