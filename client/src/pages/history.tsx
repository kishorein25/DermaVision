import { MOCK_HISTORY } from '@/lib/mockData';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { format } from 'date-fns';
import { AlertTriangle, Calendar, Activity } from 'lucide-react';

export default function History() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Scan History</h1>
        <p className="text-slate-500">Review your past skin analysis records.</p>
      </div>

      <Card className="border-slate-200 shadow-sm">
        <CardHeader>
           <CardTitle>Past Records</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-slate-100 overflow-hidden">
            <table className="w-full text-sm text-left">
              <thead className="bg-slate-50 text-slate-500 font-medium border-b border-slate-100">
                <tr>
                  <th className="px-6 py-4">Date & Time</th>
                  <th className="px-6 py-4">Detected Condition</th>
                  <th className="px-6 py-4">Severity</th>
                  <th className="px-6 py-4 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {MOCK_HISTORY.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                         <Calendar className="h-4 w-4 text-slate-400" />
                         {format(new Date(item.date), "PPP p")}
                      </div>
                    </td>
                    <td className="px-6 py-4 font-medium text-slate-900">
                      {item.prediction}
                    </td>
                    <td className="px-6 py-4">
                      <Badge 
                        variant="outline" 
                        className={
                          item.severity === "Severe" ? "bg-red-50 text-red-700 border-red-200" :
                          item.severity === "Moderate" ? "bg-yellow-50 text-yellow-700 border-yellow-200" :
                          "bg-green-50 text-green-700 border-green-200"
                        }
                      >
                        {item.severity}
                      </Badge>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="text-xs text-slate-400 flex items-center justify-end gap-1">
                        <AlertTriangle className="h-3 w-3" /> AI Simulation
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {MOCK_HISTORY.length === 0 && (
               <div className="p-8 text-center text-slate-500">No history found.</div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
