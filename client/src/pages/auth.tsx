import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScanLine, ArrowRight, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import generatedImage from '@assets/generated_images/clean_medical_technology_background_with_teal_abstract_shapes.png';

// --- Schemas ---
const loginSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(1, "Password is required"),
});

const signupSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  age: z.string().min(1, "Age is required"),
  gender: z.string().min(1, "Gender is required"),
  email: z.string().email("Invalid email address"),
  phone: z.string().min(10, "Phone number must be at least 10 digits"),
  city: z.string().min(2, "City is required"),
  country: z.string().min(2, "Country is required"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export default function AuthPage() {
  const { login } = useAuth();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);

  // --- Login Form ---
  const loginForm = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
  });

  const onLogin = async (data: z.infer<typeof loginSchema>) => {
    setIsLoading(true);
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock login - for demo, just logs in with dummy user if email is present
    login({
      id: "123",
      name: "Jane Doe",
      email: data.email,
      age: "28",
      gender: "Female",
      city: "New York",
      country: "USA"
    });
    
    setIsLoading(false);
    toast({
      title: "Welcome back",
      description: "Successfully logged in to DermaVision",
    });
  };

  // --- Signup Form ---
  const signupForm = useForm<z.infer<typeof signupSchema>>({
    resolver: zodResolver(signupSchema),
  });

  const onSignup = async (data: z.infer<typeof signupSchema>) => {
    setIsLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    login({
      id: "456",
      name: data.name,
      email: data.email,
      age: data.age,
      gender: data.gender,
      city: data.city,
      country: data.country
    });
    
    setIsLoading(false);
    toast({
      title: "Account created",
      description: "Welcome to DermaVision!",
    });
  };

  return (
    <div className="min-h-screen w-full flex">
      {/* Left Side - Hero Image */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-slate-900">
        <div className="absolute inset-0 z-0">
            <img 
                src={generatedImage} 
                alt="Medical Technology Background" 
                className="w-full h-full object-cover opacity-80"
            />
        </div>
        <div className="absolute inset-0 bg-gradient-to-t from-teal-900/90 to-transparent z-10" />
        <div className="relative z-20 flex flex-col justify-between p-12 text-white h-full w-full">
          <div className="flex items-center gap-2">
            <div className="bg-white/20 backdrop-blur-md p-2 rounded-lg">
              <ScanLine className="h-8 w-8" />
            </div>
            <span className="text-2xl font-bold tracking-tight">DermaVision</span>
          </div>
          
          <div className="space-y-6 max-w-lg">
            <h1 className="text-5xl font-bold leading-tight">
              Advanced Skin Health Analysis
            </h1>
            <p className="text-lg text-slate-200">
              Monitor your skin health with AI-powered analysis and connect with certified dermatologists instantly.
            </p>
          </div>
          
          <div className="text-sm text-slate-300">
            © 2025 DermaVision Health Tech. All rights reserved.
          </div>
        </div>
      </div>

      {/* Right Side - Auth Forms */}
      <div className="flex-1 flex items-center justify-center p-4 bg-slate-50">
        <div className="w-full max-w-md animate-in slide-in-from-right-8 duration-500">
          <div className="mb-8 text-center lg:hidden">
            <div className="flex items-center justify-center gap-2 mb-4">
               <div className="bg-primary/10 p-2 rounded-lg">
                 <ScanLine className="h-8 w-8 text-primary" />
               </div>
               <span className="text-2xl font-bold text-slate-900">DermaVision</span>
            </div>
            <h1 className="text-2xl font-bold">Welcome</h1>
            <p className="text-muted-foreground">Sign in to access your dashboard</p>
          </div>

          <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-4 h-12">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="signup">Sign Up</TabsTrigger>
            </TabsList>

            {/* LOGIN TAB */}
            <TabsContent value="login">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle>Login</CardTitle>
                  <CardDescription>Enter your credentials to access your account</CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={loginForm.handleSubmit(onLogin)} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input id="email" type="email" placeholder="patient@example.com" {...loginForm.register("email")} />
                      {loginForm.formState.errors.email && <p className="text-xs text-red-500">{loginForm.formState.errors.email.message}</p>}
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">Password</Label>
                      <Input id="password" type="password" {...loginForm.register("password")} />
                      {loginForm.formState.errors.password && <p className="text-xs text-red-500">{loginForm.formState.errors.password.message}</p>}
                    </div>
                    <Button type="submit" className="w-full h-11 text-base" disabled={isLoading}>
                      {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Sign In"}
                    </Button>
                  </form>
                </CardContent>
                <CardFooter className="flex justify-center pb-6">
                  <Button variant="link" className="text-sm text-muted-foreground">Forgot password?</Button>
                </CardFooter>
              </Card>
            </TabsContent>

            {/* SIGNUP TAB */}
            <TabsContent value="signup">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle>Create Account</CardTitle>
                  <CardDescription>Enter your details to get started</CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={signupForm.handleSubmit(onSignup)} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Full Name</Label>
                      <Input id="name" placeholder="John Doe" {...signupForm.register("name")} />
                      {signupForm.formState.errors.name && <p className="text-xs text-red-500">{signupForm.formState.errors.name.message}</p>}
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="age">Age</Label>
                        <Input id="age" type="number" {...signupForm.register("age")} />
                        {signupForm.formState.errors.age && <p className="text-xs text-red-500">{signupForm.formState.errors.age.message}</p>}
                      </div>
                      <div className="space-y-2">
                         <Label htmlFor="gender">Gender</Label>
                         <select 
                           className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                           {...signupForm.register("gender")}
                         >
                           <option value="">Select</option>
                           <option value="Male">Male</option>
                           <option value="Female">Female</option>
                           <option value="Other">Other</option>
                         </select>
                         {signupForm.formState.errors.gender && <p className="text-xs text-red-500">{signupForm.formState.errors.gender.message}</p>}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="su-email">Email</Label>
                      <Input id="su-email" type="email" {...signupForm.register("email")} />
                       {signupForm.formState.errors.email && <p className="text-xs text-red-500">{signupForm.formState.errors.email.message}</p>}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="phone">Phone</Label>
                      <Input id="phone" type="tel" {...signupForm.register("phone")} />
                       {signupForm.formState.errors.phone && <p className="text-xs text-red-500">{signupForm.formState.errors.phone.message}</p>}
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="city">City</Label>
                          <Input id="city" {...signupForm.register("city")} />
                           {signupForm.formState.errors.city && <p className="text-xs text-red-500">{signupForm.formState.errors.city.message}</p>}
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="country">Country</Label>
                          <Input id="country" {...signupForm.register("country")} />
                           {signupForm.formState.errors.country && <p className="text-xs text-red-500">{signupForm.formState.errors.country.message}</p>}
                        </div>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="su-password">Password</Label>
                      <Input id="su-password" type="password" {...signupForm.register("password")} />
                       {signupForm.formState.errors.password && <p className="text-xs text-red-500">{signupForm.formState.errors.password.message}</p>}
                    </div>

                    <Button type="submit" className="w-full h-11 mt-2" disabled={isLoading}>
                      {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Create Account"}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
