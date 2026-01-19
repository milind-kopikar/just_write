"use client";

import React from 'react';
import { ArrowLeft, Award, TrendingUp, CheckCircle, Star } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface ReportCardProps {
  onBack: () => void;
}

export default function ReportCard({ onBack }: ReportCardProps) {
  // Dummy data for the demo
  const radarData = [
    { subject: 'Focus', A: 85, fullMark: 100 },
    { subject: 'Content', A: 70, fullMark: 100 },
    { subject: 'Organization', A: 60, fullMark: 100 },
    { subject: 'Style', A: 75, fullMark: 100 },
    { subject: 'Conventions', A: 50, fullMark: 100 },
  ];

  const barData = [
    { name: 'Pre-writing', score: 4 },
    { name: 'Drafting', score: 3 },
    { name: 'Revising', score: 2 },
    { name: 'Editing', score: 0 },
    { name: 'Publishing', score: 0 },
  ];

  return (
    <div className="bg-white rounded-3xl shadow-2xl overflow-hidden border-4 border-blue-100 animate-in fade-in zoom-in-95 duration-500">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white relative">
        <div className="absolute left-6 top-8 flex items-center space-x-4">
          <button 
            onClick={onBack}
            className="bg-white/20 hover:bg-white/30 p-2 rounded-full transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <div className="w-10 h-10 overflow-hidden rounded-lg shadow-lg border border-white/20">
            <img 
              src="/just_write_logo.jpg" 
              alt="Logo" 
              className="object-cover w-full h-full"
            />
          </div>
        </div>
        <div className="text-center">
          <div className="bg-white/20 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 backdrop-blur-sm">
            <Award size={48} className="text-yellow-300" />
          </div>
          <h2 className="text-4xl font-black tracking-tight mb-2">My Skills Report Card</h2>
          <p className="text-blue-100 font-bold text-lg opacity-90 uppercase tracking-widest">Philadelphia Grade 3 Writing Journey</p>
        </div>
      </div>

      <div className="p-8 grid md:grid-cols-2 gap-12">
        {/* Left Column: Stats & Radar Chart */}
        <div className="space-y-8">
          <div>
            <h3 className="text-2xl font-black text-gray-800 mb-6 flex items-center">
              <Sparkles className="mr-2 text-yellow-500" /> Writing Superpowers
            </h3>
            <div className="h-80 w-full bg-blue-50/50 rounded-3xl p-4 border-2 border-dashed border-blue-200">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                  <PolarGrid stroke="#94a3b8" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#1e293b', fontSize: 14, fontWeight: 'bold' }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar
                    name="Student"
                    dataKey="A"
                    stroke="#2563eb"
                    fill="#3b82f6"
                    fillOpacity={0.6}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-50 p-4 rounded-2xl border-2 border-green-100 flex items-center space-x-3">
              <div className="bg-green-500 p-3 rounded-xl text-white">
                <Star size={24} fill="white" />
              </div>
              <div>
                <p className="text-xs font-bold text-green-700 uppercase">Top Skill</p>
                <p className="text-lg font-black text-green-900">Strong Focus</p>
              </div>
            </div>
            <div className="bg-purple-50 p-4 rounded-2xl border-2 border-purple-100 flex items-center space-x-3">
              <div className="bg-purple-500 p-3 rounded-xl text-white">
                <TrendingUp size={24} />
              </div>
              <div>
                <p className="text-xs font-bold text-purple-700 uppercase">Current Level</p>
                <p className="text-lg font-black text-purple-900">Rising Star</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Progress & Milestones */}
        <div className="space-y-8">
          <div>
            <h3 className="text-2xl font-black text-gray-800 mb-6 flex items-center">
              <TrendingUp className="mr-2 text-blue-500" /> Phase Mastery
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData}>
                  <XAxis dataKey="name" tick={{ fontSize: 12, fontWeight: 'bold' }} axisLine={false} tickLine={false} />
                  <Tooltip cursor={{ fill: '#f8fafc' }} />
                  <Bar dataKey="score" fill="#2563eb" radius={[10, 10, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-black text-gray-800 mb-6 flex items-center">
              <CheckCircle className="mr-2 text-green-500" /> Goal Checklist
            </h3>
            <ul className="space-y-3">
              {[
                { label: "Pick a great topic", done: true },
                { label: "Share 3 reasons for your opinion", done: true },
                { label: "Use transition words (because, also)", done: false },
                { label: "Check all capital letters", done: false }
              ].map((goal, i) => (
                <li key={i} className={`flex items-center p-4 rounded-2xl border-2 transition-all ${goal.done ? 'bg-green-50 border-green-200 opacity-100' : 'bg-gray-50 border-gray-100 opacity-60'}`}>
                  {goal.done ? (
                    <div className="bg-green-500 rounded-full p-1 mr-4">
                      <CheckCircle size={20} className="text-white" />
                    </div>
                  ) : (
                    <div className="w-7 h-7 rounded-full border-2 border-gray-300 mr-4" />
                  )}
                  <span className={`text-lg font-bold ${goal.done ? 'text-green-900' : 'text-gray-500'}`}>{goal.label}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-gray-50 p-6 text-center border-t border-gray-100">
        <p className="text-gray-500 font-bold italic text-lg">"Keep writing, you're doing amazing! Next stop: Revising."</p>
      </div>
    </div>
  );
}

// Add Sparkles icon manually if missing from standard lucide
function Sparkles({ className, size = 24 }: { className?: string, size?: number }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      width={size} 
      height={size} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="3" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
    >
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
      <path d="M5 3v4" /><path d="M19 17v4" /><path d="M3 5h4" /><path d="M17 19h4" />
    </svg>
  );
}
