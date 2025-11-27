import { useState } from 'react';
import { MOCK_DOCTORS, Doctor } from '@/lib/mockData';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Video, MessageSquare, Star, MapPin, Send, ArrowLeft } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

export default function Consult() {
  const [activeChat, setActiveChat] = useState<Doctor | null>(null);
  const { toast } = useToast();
  const [bookingDate, setBookingDate] = useState("");
  const [bookingTime, setBookingTime] = useState("");

  const handleBook = () => {
    toast({
      title: "Appointment Requested",
      description: `Booking request sent for ${bookingDate} at ${bookingTime}.`,
    });
  };

  if (activeChat) {
    return (
      <div className="h-[calc(100vh-140px)] flex flex-col bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center gap-3 bg-slate-50">
          <Button variant="ghost" size="icon" onClick={() => setActiveChat(null)}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <Avatar>
            <AvatarImage src={activeChat.image} />
            <AvatarFallback>{activeChat.name.charAt(0)}</AvatarFallback>
          </Avatar>
          <div>
            <h3 className="font-semibold text-slate-900">{activeChat.name}</h3>
            <p className="text-xs text-slate-500 flex items-center">
              <span className="h-2 w-2 bg-green-500 rounded-full mr-1" /> Online
            </p>
          </div>
        </div>
        
        <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-slate-50/30">
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 text-slate-800 p-3 rounded-2xl rounded-tl-none max-w-[80%] shadow-sm">
              Hello! I'm {activeChat.name}. How can I help you with your skin concerns today?
            </div>
          </div>
          <div className="flex justify-end">
            <div className="bg-primary text-primary-foreground p-3 rounded-2xl rounded-tr-none max-w-[80%] shadow-sm">
              Hi Doctor, I have some redness on my face.
            </div>
          </div>
          <div className="flex justify-start">
             <div className="bg-white border border-slate-200 text-slate-800 p-3 rounded-2xl rounded-tl-none max-w-[80%] shadow-sm">
              I see. Could you please share a photo of the affected area? You can use the Skin Scan feature to capture it first.
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-slate-100 bg-white">
          <form className="flex gap-2" onSubmit={(e) => { e.preventDefault(); (e.target as HTMLFormElement).reset(); }}>
            <Input placeholder="Type a message..." className="flex-1" />
            <Button type="submit" size="icon">
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Consult a Dermatologist</h1>
        <p className="text-slate-500">Connect with top specialists for personalized advice.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {MOCK_DOCTORS.map((doctor) => (
          <Card key={doctor.id} className="overflow-hidden hover:shadow-md transition-shadow border-slate-200">
            <div className="h-24 bg-gradient-to-r from-teal-50 to-blue-50" />
            <div className="px-6 -mt-12 flex justify-between items-end">
              <Avatar className="h-24 w-24 border-4 border-white shadow-sm">
                <AvatarImage src={doctor.image} className="object-cover" />
                <AvatarFallback>{doctor.name.charAt(0)}</AvatarFallback>
              </Avatar>
              <Badge variant="secondary" className="mb-2 flex items-center gap-1">
                <Star className="h-3 w-3 fill-yellow-500 text-yellow-500" /> {doctor.rating}
              </Badge>
            </div>
            
            <CardHeader className="pt-4">
              <h3 className="text-xl font-bold text-slate-900">{doctor.name}</h3>
              <p className="text-sm font-medium text-primary">{doctor.specialization}</p>
              <div className="flex items-center gap-4 text-sm text-slate-500 mt-2">
                 <span className="flex items-center gap-1"><MapPin className="h-3 w-3" /> {doctor.location}</span>
                 <span>{doctor.experience} exp.</span>
              </div>
            </CardHeader>
            
            <CardFooter className="grid grid-cols-2 gap-3 border-t border-slate-100 bg-slate-50/50 p-4">
              <Button variant="outline" onClick={() => setActiveChat(doctor)}>
                <MessageSquare className="mr-2 h-4 w-4" /> Chat
              </Button>
              
              <Dialog>
                <DialogTrigger asChild>
                  <Button>
                    <Video className="mr-2 h-4 w-4" /> Book
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Book Video Consultation</DialogTitle>
                    <DialogDescription>Schedule a session with {doctor.name}</DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid gap-2">
                      <Label>Select Date</Label>
                      <Input type="date" onChange={(e) => setBookingDate(e.target.value)} />
                    </div>
                    <div className="grid gap-2">
                      <Label>Select Time</Label>
                      <Input type="time" onChange={(e) => setBookingTime(e.target.value)} />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button onClick={handleBook}>Confirm Booking</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
