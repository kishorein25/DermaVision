import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, Heart, Sparkles, Play, RotateCcw } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function Games() {
  const [breathingActive, setBreathingActive] = useState(false);
  const [breathingPhase, setBreathingPhase] = useState<'inhale' | 'hold' | 'exhale'>('inhale');
  const [memoryCards, setMemoryCards] = useState<number[]>([]);
  const [flippedCards, setFlippedCards] = useState<number[]>([]);
  const [matchedCards, setMatchedCards] = useState<number[]>([]);

  useEffect(() => {
    if (!breathingActive) return;

    const phases: Array<'inhale' | 'hold' | 'exhale'> = ['inhale', 'hold', 'exhale'];
    let currentPhaseIndex = 0;
    
    const interval = setInterval(() => {
      currentPhaseIndex = (currentPhaseIndex + 1) % phases.length;
      setBreathingPhase(phases[currentPhaseIndex]);
    }, 4000);

    return () => clearInterval(interval);
  }, [breathingActive]);

  const startBreathing = () => {
    setBreathingActive(true);
    setBreathingPhase('inhale');
  };

  const initMemoryGame = () => {
    const cards = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6];
    setMemoryCards(cards.sort(() => Math.random() - 0.5));
    setFlippedCards([]);
    setMatchedCards([]);
  };

  const handleCardClick = (index: number) => {
    if (flippedCards.length === 2 || flippedCards.includes(index) || matchedCards.includes(index)) {
      return;
    }

    const newFlipped = [...flippedCards, index];
    setFlippedCards(newFlipped);

    if (newFlipped.length === 2) {
      const [first, second] = newFlipped;
      if (memoryCards[first] === memoryCards[second]) {
        setMatchedCards([...matchedCards, first, second]);
        setFlippedCards([]);
      } else {
        setTimeout(() => setFlippedCards([]), 1000);
      }
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Mental Wellness Games</h1>
        <p className="text-slate-500 mt-2">Mind-free games to help reduce stress and improve mental clarity</p>
      </div>

      {/* Breathing Exercise */}
      <Card className="border-slate-200 shadow-md">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Heart className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <CardTitle>Breathing Exercise</CardTitle>
              <CardDescription>4-4-4 breathing technique for relaxation</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {!breathingActive ? (
            <Button onClick={startBreathing} className="w-full" size="lg">
              <Play className="mr-2 h-5 w-5" />
              Start Breathing Exercise
            </Button>
          ) : (
            <div className="space-y-6">
              <div className="flex flex-col items-center justify-center py-8">
                <div className={`w-32 h-32 rounded-full border-4 transition-all duration-1000 ${
                  breathingPhase === 'inhale' ? 'scale-150 border-blue-500 bg-blue-100' :
                  breathingPhase === 'hold' ? 'scale-150 border-purple-500 bg-purple-100' :
                  'scale-100 border-green-500 bg-green-100'
                }`}>
                  <div className="flex items-center justify-center h-full">
                    <span className="text-2xl font-bold">
                      {breathingPhase === 'inhale' ? 'Breathe In' :
                       breathingPhase === 'hold' ? 'Hold' : 'Breathe Out'}
                    </span>
                  </div>
                </div>
              </div>
              <Button onClick={() => setBreathingActive(false)} variant="outline" className="w-full">
                Stop Exercise
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Memory Game */}
      <Card className="border-slate-200 shadow-md">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Brain className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <CardTitle>Memory Match Game</CardTitle>
                <CardDescription>Match pairs to improve focus and concentration</CardDescription>
              </div>
            </div>
            <Button onClick={initMemoryGame} size="sm" variant="outline">
              <RotateCcw className="mr-2 h-4 w-4" />
              New Game
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {memoryCards.length === 0 ? (
            <Button onClick={initMemoryGame} className="w-full" size="lg">
              <Play className="mr-2 h-5 w-5" />
              Start Memory Game
            </Button>
          ) : (
            <>
              <div className="mb-4">
                <Progress value={(matchedCards.length / memoryCards.length) * 100} />
                <p className="text-sm text-slate-500 mt-2 text-center">
                  Matched: {matchedCards.length / 2} / {memoryCards.length / 2}
                </p>
              </div>
              <div className="grid grid-cols-4 gap-3">
                {memoryCards.map((card, index) => (
                  <button
                    key={index}
                    onClick={() => handleCardClick(index)}
                    className={`aspect-square rounded-lg text-2xl font-bold transition-all ${
                      flippedCards.includes(index) || matchedCards.includes(index)
                        ? 'bg-primary text-white'
                        : 'bg-slate-200 hover:bg-slate-300'
                    }`}
                  >
                    {flippedCards.includes(index) || matchedCards.includes(index) ? (
                      ['🌟', '💚', '🌸', '🌈', '☀️', '🌙'][card - 1]
                    ) : (
                      '?'
                    )}
                  </button>
                ))}
              </div>
              {matchedCards.length === memoryCards.length && (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg text-center">
                  <Sparkles className="h-6 w-6 text-green-600 mx-auto mb-2" />
                  <p className="text-green-800 font-semibold">Congratulations! You matched all pairs!</p>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* Quick Tips */}
      <Card className="bg-gradient-to-r from-teal-50 to-blue-50 border-teal-200">
        <CardHeader>
          <CardTitle className="text-teal-900">Benefits of Mental Wellness Games</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2 text-slate-700">
            <li className="flex items-start gap-2">
              <span className="text-teal-600">•</span>
              <span>Reduces stress and anxiety through mindful activities</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal-600">•</span>
              <span>Improves focus and concentration</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal-600">•</span>
              <span>Enhances cognitive function and memory</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal-600">•</span>
              <span>Provides a healthy break from work or study</span>
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
