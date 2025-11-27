import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Search, ChevronRight, AlertCircle } from 'lucide-react';
import { DISEASE_TIPS, DiseaseTip } from '@/lib/mockData';

export default function SearchTips() {
  const [query, setQuery] = useState('');
  const [selectedDisease, setSelectedDisease] = useState<DiseaseTip | null>(null);

  const filteredDiseases = Object.values(DISEASE_TIPS).filter(d => 
    d.name.toLowerCase().includes(query.toLowerCase()) || 
    d.description.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <div className="text-center max-w-2xl mx-auto space-y-4">
        <h1 className="text-3xl font-bold text-slate-900">Disease Knowledge Base</h1>
        <p className="text-slate-500">Search for skin conditions to find causes, treatments, and care tips.</p>
        
        <div className="relative">
          <Search className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
          <Input 
            className="pl-10 h-12 text-lg bg-white shadow-sm border-slate-200" 
            placeholder="Search e.g. Acne, Eczema..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
      </div>

      {selectedDisease ? (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
          <Button variant="ghost" onClick={() => setSelectedDisease(null)} className="mb-4 hover:bg-slate-100">
            ← Back to Search results
          </Button>
          
          <Card className="border-t-4 border-t-primary overflow-hidden">
            <div className="bg-slate-50 p-6 border-b border-slate-100">
                <h2 className="text-3xl font-bold text-slate-900 mb-2">{selectedDisease.name}</h2>
                <p className="text-lg text-slate-600">{selectedDisease.description}</p>
            </div>
            
            <CardContent className="p-6 grid gap-8">
              <section>
                <h3 className="text-lg font-semibold text-slate-900 mb-3 flex items-center">
                  <div className="h-2 w-2 rounded-full bg-red-400 mr-2" /> Common Causes
                </h3>
                <div className="flex flex-wrap gap-2">
                  {selectedDisease.causes.map((cause, idx) => (
                    <Badge key={idx} variant="secondary" className="px-3 py-1 text-sm font-normal">
                      {cause}
                    </Badge>
                  ))}
                </div>
              </section>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-blue-50/50 p-5 rounded-xl border border-blue-100">
                  <h3 className="text-lg font-semibold text-blue-900 mb-3">Tips for Men</h3>
                  <ul className="space-y-2">
                    {selectedDisease.tipsMen.map((tip, idx) => (
                      <li key={idx} className="flex items-start text-sm text-blue-800">
                        <span className="mr-2 mt-1.5 h-1.5 w-1.5 rounded-full bg-blue-400 flex-shrink-0" />
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-pink-50/50 p-5 rounded-xl border border-pink-100">
                  <h3 className="text-lg font-semibold text-pink-900 mb-3">Tips for Women</h3>
                  <ul className="space-y-2">
                    {selectedDisease.tipsWomen.map((tip, idx) => (
                      <li key={idx} className="flex items-start text-sm text-pink-800">
                         <span className="mr-2 mt-1.5 h-1.5 w-1.5 rounded-full bg-pink-400 flex-shrink-0" />
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="bg-amber-50 p-4 rounded-lg border border-amber-200 flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-amber-600 mt-0.5 flex-shrink-0" />
                <div>
                  <h4 className="font-semibold text-amber-900">When to see a doctor</h4>
                  <p className="text-sm text-amber-800 mt-1">{selectedDisease.whenToSeeDoctor}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDiseases.length > 0 ? (
            filteredDiseases.map((disease) => (
              <Card 
                key={disease.id} 
                className="group hover:shadow-md hover:border-primary/30 transition-all cursor-pointer"
                onClick={() => setSelectedDisease(disease)}
              >
                <CardHeader>
                  <CardTitle className="group-hover:text-primary transition-colors">{disease.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-500 line-clamp-3 mb-4">{disease.description}</p>
                  <div className="flex items-center text-sm text-primary font-medium">
                    Read More <ChevronRight className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="col-span-full text-center py-12 text-slate-400">
              No diseases found matching "{query}"
            </div>
          )}
        </div>
      )}
    </div>
  );
}
