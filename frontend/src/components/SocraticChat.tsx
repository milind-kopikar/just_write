"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Sparkles } from 'lucide-react';
import axios from 'axios';import { API_BASE_URL } from '@/utils/api';
interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface SocraticChatProps {
  topic: string;
  phase: string;
  prompt?: string;
  videoId?: string;  // I-Do video ID — used to pull the lesson transcript for coaching
}

export default function SocraticChat({ topic, phase, prompt, videoId }: SocraticChatProps) {
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'assistant', 
      content: prompt 
        ? `Hi! I'm your writing coach. I see you're working on the prompt: "${prompt}". Let's work on the ${phase} for your ${topic} writing together. How can I help you get started?`
        : `Hi! I'm your writing coach. Let's work on the ${phase} for your ${topic} writing together. What's one thing you want to write about?` 
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsLoading(true);

    try {
      // Use the local API endpoint (adjust URL if needed)
      const response = await axios.post(`${API_BASE_URL}/tutor/chat`, {
        message: userMsg,
        history: messages.map(m => ({ role: m.role, content: m.content })),
        topic: topic,
        prompt: prompt,
        video_id: videoId ?? null,
      });

      setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
    } catch (error: any) {
      console.error("Chat error:", error);
      let errorMsg = "Sorry, I'm having a little trouble thinking. Can you try again?";
      
      if (axios.isAxiosError(error) && error.response) {
        if (error.response.status === 503) {
          errorMsg = "AI service unavailable: invalid or revoked API key. Please rotate your GOOGLE_API_KEY.";
        } else if (error.response.status === 429) {
          errorMsg = "The writing coach is a bit busy right now (Quota Limit). Please wait about 30 seconds and try again!";
        } else if (error.response.data?.detail) {
          errorMsg = `Server error: ${error.response.data.detail}`;
        }
      }
      
      setMessages(prev => [...prev, { role: 'assistant', content: errorMsg }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[85%] space-x-2 ${m.role === 'user' ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${m.role === 'user' ? 'bg-blue-100' : 'bg-green-100'}`}>
                {m.role === 'user' ? <User size={18} className="text-blue-600" /> : <Bot size={18} className="text-green-600" />}
              </div>
              <div className={`p-4 rounded-2xl shadow-sm ${
                m.role === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-none' 
                  : 'bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200'
              }`}>
                <p className="text-lg font-medium leading-relaxed">{m.content}</p>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 flex items-center space-x-2">
              <Sparkles size={18} className="text-green-500 animate-pulse" />
              <span className="text-gray-400 font-bold italic">Coach is thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t-2 border-gray-100 bg-gray-50">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message here..."
            className="flex-1 p-4 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none transition-all text-lg font-medium"
          />
          <button
            onClick={handleSend}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-xl shadow-lg transition-transform active:scale-95 disabled:opacity-50"
          >
            <Send size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}
