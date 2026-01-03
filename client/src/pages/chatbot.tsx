import { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageCircle, Send, Bot, User, Sparkles } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';

interface Message {
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'bot',
      content: "Hello! I'm your mental wellness companion. I'm here to help you explore and understand your feelings. Whether you're a student dealing with academic stress or a professional managing work pressure, feel free to share what's on your mind. How are you feeling today?",
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const generateResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    // Feeling keywords
    if (lowerMessage.includes('stressed') || lowerMessage.includes('stress')) {
      return "I understand you're feeling stressed. Stress is a common response to challenging situations. Can you tell me more about what's causing this stress? Is it related to work, studies, or personal matters?";
    }
    
    if (lowerMessage.includes('anxious') || lowerMessage.includes('anxiety') || lowerMessage.includes('worried')) {
      return "Anxiety can be overwhelming. Remember that it's okay to feel this way. For students and professionals alike, anxiety often stems from uncertainty or pressure. Try taking deep breaths - inhale for 4 counts, hold for 4, exhale for 4. What specific situation is making you feel anxious?";
    }
    
    if (lowerMessage.includes('sad') || lowerMessage.includes('depressed') || lowerMessage.includes('down')) {
      return "I hear you, and your feelings are valid. It takes courage to acknowledge when we're feeling down. Sometimes talking about it helps. Would you like to share what's been bothering you? Remember, seeking support is a sign of strength.";
    }
    
    if (lowerMessage.includes('overwhelm') || lowerMessage.includes('too much')) {
      return "Feeling overwhelmed is a sign that you're dealing with a lot. For professionals and students, it's important to break tasks into smaller, manageable pieces. Have you tried making a priority list? What's the biggest challenge you're facing right now?";
    }
    
    // Work/Study related
    if (lowerMessage.includes('work') || lowerMessage.includes('job') || lowerMessage.includes('office')) {
      return "Work-related stress is very common among professionals. It's important to maintain work-life balance. Have you been able to take breaks during your workday? Setting boundaries and taking time for self-care can make a significant difference.";
    }
    
    if (lowerMessage.includes('exam') || lowerMessage.includes('study') || lowerMessage.includes('student') || lowerMessage.includes('school') || lowerMessage.includes('college')) {
      return "Academic pressure can be intense for students. Remember that your worth isn't defined by grades alone. Have you tried studying in shorter, focused sessions with breaks in between? Also, don't hesitate to reach out to classmates or professors for support.";
    }
    
    // Positive feelings
    if (lowerMessage.includes('good') || lowerMessage.includes('great') || lowerMessage.includes('happy') || lowerMessage.includes('better')) {
      return "That's wonderful to hear! It's great that you're experiencing positive feelings. What's been going well for you? Celebrating these moments, no matter how small, is important for mental wellness.";
    }
    
    // Coping strategies
    if (lowerMessage.includes('help') || lowerMessage.includes('cope') || lowerMessage.includes('manage')) {
      return "Here are some evidence-based coping strategies: 1) Practice mindfulness and meditation, 2) Engage in regular physical exercise, 3) Maintain a consistent sleep schedule, 4) Talk to trusted friends or family, 5) Try our binaural songs for relaxation. Which of these would you like to explore further?";
    }
    
    // Default responses
    const responses = [
      "Thank you for sharing that with me. Can you tell me more about how this makes you feel?",
      "I appreciate you opening up. Your feelings are important. What do you think might help you feel better?",
      "That sounds challenging. How has this been affecting your daily life - whether at work, school, or personally?",
      "I'm here to listen. Would you like to explore some coping strategies, or would you prefer to talk more about what you're experiencing?",
      "Your mental health matters. Whether you're juggling work deadlines or academic pressures, remember that taking care of yourself is not selfish - it's necessary."
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSend = () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages([...messages, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate bot thinking
    setTimeout(() => {
      const botResponse: Message = {
        role: 'bot',
        content: generateResponse(inputValue),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000 + Math.random() * 1000);
  };

  const quickResponses = [
    "I'm feeling stressed",
    "I'm anxious about work/study",
    "I need coping strategies",
    "I'm feeling overwhelmed"
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Mental Health Chatbot</h1>
        <p className="text-slate-500 mt-2">A safe space to explore and express your feelings</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="border-blue-200 bg-blue-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <User className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-blue-900">For Professionals</h3>
                <p className="text-sm text-blue-700">Work stress & balance</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-purple-200 bg-purple-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Sparkles className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-purple-900">For Students</h3>
                <p className="text-sm text-purple-700">Academic support</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-green-200 bg-green-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <MessageCircle className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-green-900">24/7 Support</h3>
                <p className="text-sm text-green-700">Always here to listen</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border-slate-200 shadow-lg">
        <CardHeader className="border-b">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Bot className="h-6 w-6 text-primary" />
            </div>
            <div>
              <CardTitle>Wellness Companion</CardTitle>
              <CardDescription>Feeling Exposure & Mental Health Support</CardDescription>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="p-0">
          <ScrollArea className="h-[400px] p-4" ref={scrollRef}>
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {message.role === 'bot' && (
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Bot className="h-4 w-4 text-primary" />
                    </div>
                  )}
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-slate-100 text-slate-900'
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    <span className="text-xs opacity-70 mt-1 block">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  {message.role === 'user' && (
                    <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0">
                      <User className="h-4 w-4 text-white" />
                    </div>
                  )}
                </div>
              ))}
              {isTyping && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-primary" />
                  </div>
                  <div className="bg-slate-100 rounded-lg p-3">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                      <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                      <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="border-t p-4 space-y-3">
            <div className="flex flex-wrap gap-2">
              {quickResponses.map((response, index) => (
                <Badge
                  key={index}
                  variant="outline"
                  className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
                  onClick={() => setInputValue(response)}
                >
                  {response}
                </Badge>
              ))}
            </div>
            
            <div className="flex gap-2">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Share your feelings..."
                className="flex-1"
              />
              <Button onClick={handleSend} disabled={!inputValue.trim()}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-blue-900">Important Note</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-slate-700">
            This chatbot provides emotional support and coping strategies, but it's not a replacement for professional mental health care. 
            If you're experiencing severe distress or crisis, please contact a mental health professional or crisis hotline immediately.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
