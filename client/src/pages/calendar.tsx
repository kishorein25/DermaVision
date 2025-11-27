import { useState } from 'react';
import { DayPicker } from 'react-day-picker';
import 'react-day-picker/dist/style.css';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MOCK_HISTORY, MOCK_DOCTORS } from '@/lib/mockData';
import { Calendar as CalendarIcon, Clock, User } from 'lucide-react';
import { format } from 'date-fns';

export default function CalendarPage() {
  const [selected, setSelected] = useState<Date | undefined>(new Date());

  const appointments = [
    { id: 1, doctorId: 1, date: new Date(new Date().setDate(new Date().getDate() + 1)), time: "10:00 AM", status: "Confirmed" },
    { id: 2, doctorId: 2, date: new Date(new Date().setDate(new Date().getDate() - 5)), time: "2:00 PM", status: "Completed" }
  ];

  return (
    <div className="space-y-8">
       <div>
        <h1 className="text-3xl font-bold text-slate-900">Schedule</h1>
        <p className="text-slate-500">Manage your appointments and track your history.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-1 border-slate-200 shadow-sm">
          <CardContent className="p-4 flex justify-center">
             <DayPicker
                mode="single"
                selected={selected}
                onSelect={setSelected}
                className="border-0"
                modifiersClassNames={{
                  selected: 'bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground focus:bg-primary focus:text-primary-foreground',
                  today: 'font-bold text-primary'
                }}
             />
          </CardContent>
        </Card>

        <Card className="lg:col-span-2 border-slate-200 shadow-sm">
           <CardHeader>
             <CardTitle>Events for {selected ? format(selected, 'MMMM do, yyyy') : 'Selected Date'}</CardTitle>
           </CardHeader>
           <CardContent className="space-y-4">
             {appointments.filter(apt => selected && apt.date.toDateString() === selected.toDateString()).length > 0 ? (
                appointments
                  .filter(apt => selected && apt.date.toDateString() === selected.toDateString())
                  .map(apt => {
                    const doctor = MOCK_DOCTORS.find(d => d.id === apt.doctorId);
                    return (
                      <div key={apt.id} className="flex items-center justify-between p-4 rounded-lg border border-slate-100 bg-slate-50 hover:border-primary/20 transition-colors">
                        <div className="flex items-center gap-4">
                          <div className="bg-white p-2 rounded-full shadow-sm">
                            <User className="h-5 w-5 text-slate-500" />
                          </div>
                          <div>
                            <h4 className="font-semibold text-slate-900">{doctor?.name}</h4>
                            <div className="flex items-center gap-3 text-sm text-slate-500 mt-1">
                               <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> {apt.time}</span>
                               <span className="flex items-center gap-1"><CalendarIcon className="h-3 w-3" /> Video Consult</span>
                            </div>
                          </div>
                        </div>
                        <Badge variant={apt.status === "Confirmed" ? "default" : "secondary"}>{apt.status}</Badge>
                      </div>
                    );
                  })
             ) : (
               <div className="text-center py-12 text-slate-400 border-2 border-dashed border-slate-100 rounded-xl">
                 No appointments scheduled for this day.
               </div>
             )}

             <div className="mt-8 pt-8 border-t border-slate-100">
                <h3 className="font-semibold text-slate-900 mb-4">All Upcoming</h3>
                <div className="space-y-3">
                    {appointments.filter(a => a.date > new Date()).map(apt => {
                        const doctor = MOCK_DOCTORS.find(d => d.id === apt.doctorId);
                         return (
                            <div key={apt.id} className="flex items-center gap-4 p-3 hover:bg-slate-50 rounded-lg transition-colors">
                                <div className="h-10 w-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600 font-bold text-xs flex-col leading-none">
                                    <span>{format(apt.date, 'dd')}</span>
                                    <span className="text-[10px] uppercase">{format(apt.date, 'MMM')}</span>
                                </div>
                                <div>
                                    <p className="font-medium text-slate-900">{doctor?.name}</p>
                                    <p className="text-xs text-slate-500">{apt.time} • Video Call</p>
                                </div>
                            </div>
                         )
                    })}
                </div>
             </div>
           </CardContent>
        </Card>
      </div>
    </div>
  );
}
