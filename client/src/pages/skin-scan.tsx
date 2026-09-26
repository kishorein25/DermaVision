import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Camera, Upload, RefreshCw, AlertTriangle, CheckCircle, Info, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const CONDITIONS = [
  { name: "Acne Vulgaris", severity: "Moderate", suggestion: "Use a mild cleanser containing salicylic acid. Avoid touching your face." },
  { name: "Eczema", severity: "Mild", suggestion: "Keep skin moisturized. Avoid harsh soaps. Apply hydrocortisone cream if itchy." },
  { name: "Psoriasis", severity: "Severe", suggestion: "Consult a dermatologist immediately. Do not scratch." },
  { name: "Melasma", severity: "Mild", suggestion: "Use high SPF sunscreen daily. Avoid direct sun exposure." },
];

export default function SkinScan() {
  const [image, setImage] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<typeof CONDITIONS[0] | null>(null);
  const webcamRef = useRef<Webcam>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setImage(imageSrc);
      analyzeImage();
    }
  }, [webcamRef]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result as string);
        analyzeImage();
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = async () => {
    setAnalyzing(true);
    setResult(null);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    const randomCondition = CONDITIONS[Math.floor(Math.random() * CONDITIONS.length)];
    setResult(randomCondition);
    setAnalyzing(false);
    
    toast({
      title: "Analysis Complete",
      description: "AI has generated a preliminary report.",
    });
  };

  const reset = () => {
    setImage(null);
    setResult(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-slate-900">Skin Analysis</h1>
        <p className="text-slate-500">Upload a photo or use your camera to get an instant AI assessment.</p>
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Input */}
        <div className="lg:col-span-2 space-y-6">
          {!image ? (
            <Card className="overflow-hidden border-slate-200 shadow-md">
              <Tabs defaultValue="upload" className="w-full">
                <div className="border-b border-slate-100 bg-slate-50/50 px-6 py-2">
                  <TabsList className="grid w-full grid-cols-2 max-w-[400px]">
                    <TabsTrigger value="upload">Upload Photo</TabsTrigger>
                    <TabsTrigger value="camera">Live Camera</TabsTrigger>
                  </TabsList>
                </div>
                
                <div className="p-6 min-h-[400px] flex flex-col items-center justify-center bg-slate-50/30">
                  <TabsContent value="upload" className="w-full flex flex-col items-center space-y-4 mt-0">
                    <div 
                      className="w-full h-64 border-2 border-dashed border-slate-300 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:bg-slate-50 transition-colors"
                      onClick={() => fileInputRef.current?.click()}
                    >
                      <Upload className="h-10 w-10 text-slate-400 mb-2" />
                      <p className="text-sm font-medium text-slate-600">Click to upload or drag and drop</p>
                      <p className="text-xs text-slate-400">JPG, PNG up to 5MB</p>
                      <input 
                        type="file" 
                        ref={fileInputRef} 
                        className="hidden" 
                        accept="image/*"
                        onChange={handleFileUpload}
                      />
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="camera" className="w-full flex flex-col items-center space-y-4 mt-0">
                    <div className="relative w-full bg-black rounded-xl overflow-hidden aspect-video">
                      <Webcam
                        audio={false}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <Button onClick={capture} className="w-full max-w-xs">
                      <Camera className="mr-2 h-4 w-4" /> Capture Photo
                    </Button>
                  </TabsContent>
                </div>
              </Tabs>
            </Card>
          ) : (
            <Card className="overflow-hidden border-slate-200 shadow-md">
              <div className="relative aspect-video bg-black">
                <img src={image} alt="Scanned skin" className="w-full h-full object-contain" />
                {analyzing && (
                  <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center text-white">
                    <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
                    <p className="text-lg font-medium animate-pulse">Analyzing skin texture...</p>
                    <p className="text-sm text-slate-400 mt-2">Comparing with medical database...</p>
                  </div>
                )}
              </div>
              <div className="p-4 flex justify-between items-center bg-slate-50 border-t border-slate-100">
                <span className="text-sm text-slate-500">Image captured successfully</span>
                <Button variant="outline" onClick={reset} disabled={analyzing}>
                  <RefreshCw className="mr-2 h-4 w-4" /> Retake
                </Button>
              </div>
            </Card>
          )}
        </div>

        {/* Right Column: Results */}
        <div className="space-y-6">
           {result ? (
             <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-700">
               <Card className="border-l-4 border-l-primary shadow-lg">
                 <CardHeader>
                   <div className="flex items-center justify-between">
                     <CardTitle>Analysis Result</CardTitle>
                     <Badge variant={result.severity === "Severe" ? "destructive" : "secondary"}>
                       {result.severity}
                     </Badge>
                   </div>
                   <CardDescription>Based on visual analysis</CardDescription>
                 </CardHeader>
                 <CardContent className="space-y-4">
                   <div>
                     <h3 className="text-2xl font-bold text-slate-900">{result.name}</h3>
                     <p className="text-sm text-slate-500">Confidence: 94%</p>
                   </div>
                   
                   <div className="space-y-2">
                     <h4 className="font-semibold text-sm text-slate-900 flex items-center">
                       <CheckCircle className="h-4 w-4 mr-2 text-green-500" /> 
                       Suggested Actions
                     </h4>
                     <p className="text-sm text-slate-600 bg-slate-50 p-3 rounded-md border border-slate-100">
                       {result.suggestion}
                     </p>
                   </div>
                 </CardContent>
                 <CardFooter>
                   <Button className="w-full" onClick={() => window.location.href = '/consult'}>
                     Consult a Doctor
                   </Button>
                 </CardFooter>
               </Card>

               <Alert variant="destructive" className="bg-red-50 border-red-200 text-red-800">
                 <AlertTriangle className="h-4 w-4" />
                 <AlertTitle>Disclaimer</AlertTitle>
                 <AlertDescription>
                   This is an AI simulation, NOT a medical diagnosis. Please consult a certified dermatologist for accurate advice.
                 </AlertDescription>
               </Alert>
             </div>
           ) : (
             <div className="h-full flex flex-col items-center justify-center p-8 text-center space-y-4 text-slate-400 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/50">
               <Info className="h-12 w-12 opacity-20" />
               <p>Upload or capture an image to see analysis results here.</p>
             </div>
           )}
        </div>
      </div>
    </div>
  );
}
