"use client";

import React, { useState } from 'react';
import { Send, FileText, CheckCircle, BarChart2, Youtube, HelpCircle, PenTool } from 'lucide-react';
import PhaseTabs from '@/components/PhaseTabs';
import ReportCard from '@/components/ReportCard';
import UserNav from '@/components/shared/UserNav';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [topic, setTopic] = useState('Narrative');
  const [currentPhase, setCurrentPhase] = useState('Pre-writing');
  const [showReport, setShowReport] = useState(false);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/auth/login');
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const topics = ['Narrative', 'Informational', 'Persuasive'];
  const phases = ['Pre-writing', 'Drafting', 'Revising', 'Editing', 'Publishing'];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-xl flex justify-between items-center z-20">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 relative overflow-hidden rounded-lg shadow-inner bg-white p-0.5">
            <img 
              src="/just_write_logo.jpg" 
              alt="Just Write Logo" 
              className="object-cover w-full h-full rounded"
            />
          </div>
          <h1 className="text-3xl font-black font-sans tracking-tight">Just Write</h1>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="flex flex-col">
            <label className="text-[10px] font-bold uppercase tracking-widest opacity-80">Writing Topic</label>
            <select 
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="bg-blue-700 border border-blue-500 text-white font-bold rounded px-2 py-1 focus:ring-2 focus:ring-blue-300 outline-none cursor-pointer text-sm"
            >
              {topics.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          
          <UserNav onShowReport={() => setShowReport(true)} />
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-6xl mx-auto w-full p-4 md:p-6">
        {showReport ? (
          <ReportCard onBack={() => setShowReport(false)} />
        ) : (
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            {/* Phase Navigation */}
            <div className="flex border-b overflow-x-auto">
              {phases.map((p) => (
                <button
                  key={p}
                  onClick={() => setCurrentPhase(p)}
                  className={`flex-1 py-4 px-2 text-center font-bold transition-all whitespace-nowrap ${
                    currentPhase === p 
                      ? 'text-blue-600 border-b-4 border-blue-600 bg-blue-50' 
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>

            {/* Phase Content */}
            <div className="p-6">
              <PhaseTabs phase={currentPhase} topic={topic} />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="p-4 text-center text-gray-500 text-sm">
        Just Write AI Tutor - Empowering Every Writer
      </footer>
    </div>
  );
}
