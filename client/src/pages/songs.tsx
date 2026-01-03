import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Music, Play, Pause, Volume2, Brain, Moon, Zap, Heart } from 'lucide-react';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';

import { LucideIcon } from 'lucide-react';

interface BinauralTrack {
  id: number;
  name: string;
  description: string;
  frequency: string;
  benefits: string[];
  category: 'focus' | 'relaxation' | 'sleep' | 'meditation';
  duration: string;
  icon: LucideIcon;
  color: string;
  bgColor: string;
}

export default function Songs() {
  const [currentTrack, setCurrentTrack] = useState<BinauralTrack | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState([70]);

  const tracks: BinauralTrack[] = [
    {
      id: 1,
      name: 'Deep Focus',
      description: 'Beta waves for concentration and productivity',
      frequency: '40 Hz',
      benefits: ['Improved concentration', 'Enhanced cognitive performance', 'Better problem-solving'],
      category: 'focus',
      duration: '30 min',
      icon: Brain,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      id: 2,
      name: 'Creative Flow',
      description: 'Alpha waves for creativity and learning',
      frequency: '10 Hz',
      benefits: ['Enhanced creativity', 'Improved learning', 'Relaxed alertness'],
      category: 'focus',
      duration: '25 min',
      icon: Zap,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      id: 3,
      name: 'Calm Mind',
      description: 'Theta waves for deep relaxation',
      frequency: '6 Hz',
      benefits: ['Stress reduction', 'Emotional balance', 'Deep relaxation'],
      category: 'relaxation',
      duration: '20 min',
      icon: Heart,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      id: 4,
      name: 'Peaceful Meditation',
      description: 'Theta waves for meditation and mindfulness',
      frequency: '7.83 Hz',
      benefits: ['Enhanced meditation', 'Mental clarity', 'Inner peace'],
      category: 'meditation',
      duration: '45 min',
      icon: Heart,
      color: 'text-teal-600',
      bgColor: 'bg-teal-50'
    },
    {
      id: 5,
      name: 'Deep Sleep',
      description: 'Delta waves for restful sleep',
      frequency: '2 Hz',
      benefits: ['Better sleep quality', 'Deep rest', 'Physical recovery'],
      category: 'sleep',
      duration: '60 min',
      icon: Moon,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50'
    },
    {
      id: 6,
      name: 'Power Nap',
      description: 'Theta-Delta transition for quick rest',
      frequency: '4 Hz',
      benefits: ['Quick refreshment', 'Energy boost', 'Mental reset'],
      category: 'sleep',
      duration: '15 min',
      icon: Moon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    }
  ];

  const handlePlayPause = (track: BinauralTrack) => {
    if (currentTrack?.id === track.id) {
      setIsPlaying(!isPlaying);
    } else {
      setCurrentTrack(track);
      setIsPlaying(true);
    }
  };

  const categories = [
    { name: 'All', value: 'all' },
    { name: 'Focus', value: 'focus' },
    { name: 'Relaxation', value: 'relaxation' },
    { name: 'Sleep', value: 'sleep' },
    { name: 'Meditation', value: 'meditation' }
  ];

  const [selectedCategory, setSelectedCategory] = useState('all');
  const filteredTracks = selectedCategory === 'all' 
    ? tracks 
    : tracks.filter(t => t.category === selectedCategory);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Binaural Beats</h1>
        <p className="text-slate-500 mt-2">Scientifically designed sound frequencies for mental wellness</p>
      </div>

      {/* Current Player */}
      {currentTrack && (
        <Card className="border-slate-200 shadow-lg bg-gradient-to-r from-slate-900 to-slate-800 text-white">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4 mb-6">
              <div className={`p-4 ${currentTrack.bgColor} rounded-xl`}>
                <currentTrack.icon className={`h-8 w-8 ${currentTrack.color}`} />
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-bold">{currentTrack.name}</h3>
                <p className="text-slate-300">{currentTrack.description}</p>
                <div className="flex gap-2 mt-2">
                  <Badge variant="secondary">{currentTrack.frequency}</Badge>
                  <Badge variant="secondary">{currentTrack.duration}</Badge>
                </div>
              </div>
              <Button
                size="lg"
                variant="secondary"
                className="rounded-full w-16 h-16"
                onClick={() => setIsPlaying(!isPlaying)}
              >
                {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6 ml-1" />}
              </Button>
            </div>

            <div className="space-y-4">
              {/* Progress Bar */}
              <div className="space-y-2">
                <Slider value={[30]} max={100} className="w-full" />
                <div className="flex justify-between text-sm text-slate-400">
                  <span>5:30</span>
                  <span>{currentTrack.duration}</span>
                </div>
              </div>

              {/* Volume Control */}
              <div className="flex items-center gap-3">
                <Volume2 className="h-4 w-4 text-slate-400" />
                <Slider
                  value={volume}
                  onValueChange={setVolume}
                  max={100}
                  step={1}
                  className="w-32"
                />
                <span className="text-sm text-slate-400 w-12">{volume[0]}%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        {categories.map((cat) => (
          <Button
            key={cat.value}
            variant={selectedCategory === cat.value ? 'default' : 'outline'}
            onClick={() => setSelectedCategory(cat.value)}
            size="sm"
          >
            {cat.name}
          </Button>
        ))}
      </div>

      {/* Tracks Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTracks.map((track) => (
          <Card key={track.id} className="border-slate-200 hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className={`p-3 ${track.bgColor} rounded-lg`}>
                  <track.icon className={`h-6 w-6 ${track.color}`} />
                </div>
                <Button
                  size="sm"
                  variant={currentTrack?.id === track.id && isPlaying ? 'default' : 'outline'}
                  className="rounded-full"
                  onClick={() => handlePlayPause(track)}
                >
                  {currentTrack?.id === track.id && isPlaying ? (
                    <Pause className="h-4 w-4" />
                  ) : (
                    <Play className="h-4 w-4 ml-0.5" />
                  )}
                </Button>
              </div>
              <CardTitle className="text-lg mt-4">{track.name}</CardTitle>
              <CardDescription>{track.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-3">
                <Badge variant="outline" className="text-xs">
                  {track.frequency}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  {track.duration}
                </Badge>
              </div>
              <div className="space-y-1">
                <p className="text-sm font-semibold text-slate-700">Benefits:</p>
                <ul className="text-sm text-slate-600 space-y-1">
                  {track.benefits.map((benefit, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-primary">•</span>
                      <span>{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Info Section */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardHeader>
          <div className="flex items-center gap-3">
            <Music className="h-6 w-6 text-blue-600" />
            <CardTitle className="text-blue-900">What are Binaural Beats?</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-3 text-slate-700">
          <p>
            Binaural beats are an auditory illusion created when two slightly different frequencies are played in each ear. 
            Your brain perceives a third tone - the binaural beat - which can influence brainwave patterns.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div className="bg-white p-4 rounded-lg border border-blue-200">
              <h4 className="font-semibold text-blue-900 mb-2">How to Use</h4>
              <ul className="space-y-1 text-sm">
                <li>• Use headphones for best results</li>
                <li>• Find a quiet, comfortable space</li>
                <li>• Listen for at least 15-30 minutes</li>
                <li>• Keep volume at comfortable level</li>
              </ul>
            </div>
            <div className="bg-white p-4 rounded-lg border border-purple-200">
              <h4 className="font-semibold text-purple-900 mb-2">Best For</h4>
              <ul className="space-y-1 text-sm">
                <li>• Students studying for exams</li>
                <li>• Professionals needing focus</li>
                <li>• Anyone seeking relaxation</li>
                <li>• Improving sleep quality</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
