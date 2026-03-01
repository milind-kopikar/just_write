"use client";

import React, { useState } from 'react';
import PhaseTabs from '@/components/PhaseTabs';
import ReportCard from '@/components/ReportCard';
import UserNav from '@/components/shared/UserNav';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';
import { BookOpen, MessageCircle, PenTool, ChevronRight } from 'lucide-react';

// ── Landing page shown to unauthenticated visitors ──────────────────────────
function LandingPage() {
  const steps = [
    {
      icon: <BookOpen className="w-8 h-8 text-blue-600" />,
      phase: 'I Do',
      title: 'Watch & Learn',
      description:
        'Watch a short lesson video and review the writing rubric so you know exactly what great writing looks like.',
    },
    {
      icon: <MessageCircle className="w-8 h-8 text-purple-600" />,
      phase: 'We Do',
      title: 'Practice Together',
      description:
        'Chat with your AI writing coach. It asks guiding questions and helps you build your ideas — without giving away the answers.',
    },
    {
      icon: <PenTool className="w-8 h-8 text-green-600" />,
      phase: 'You Do',
      title: 'Write & Get Feedback',
      description:
        'Write independently, then submit your piece for instant feedback scored to the PSSA rubric. See your strengths and growth goals.',
    },
  ];

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Nav */}
      <header className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center shadow-md">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 overflow-hidden rounded-lg bg-white p-0.5 shadow-inner">
            <img
              src="/just_write_logo.jpg"
              alt="Kopi Write Logo"
              className="object-cover w-full h-full rounded"
            />
          </div>
          <span className="text-2xl font-black tracking-tight">Kopi Write</span>
        </div>
        <div className="flex items-center space-x-3">
          <Link
            href="/auth/login"
            className="text-white font-semibold hover:text-blue-200 transition-colors text-sm"
          >
            Sign In
          </Link>
          <Link
            href="/auth/register"
            className="bg-white text-blue-600 font-bold px-4 py-2 rounded-lg hover:bg-blue-50 transition-colors text-sm"
          >
            Get Started Free
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="flex-1 flex flex-col items-center justify-center text-center px-6 py-20 bg-gradient-to-b from-blue-50 to-white">
        <h1 className="text-5xl font-black text-gray-900 leading-tight mb-4">
          Every student has a<br />
          <span className="text-blue-600">story to tell.</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-xl mb-10">
          Kopi Write is an AI-powered writing tutor for Grades 3–5. It guides students
          step-by-step from blank page to polished piece — with instant, rubric-aligned feedback.
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            href="/auth/register"
            className="flex items-center justify-center gap-2 bg-blue-600 text-white font-bold px-8 py-3 rounded-xl hover:bg-blue-700 transition-colors text-lg shadow-md"
          >
            Start Writing <ChevronRight className="w-5 h-5" />
          </Link>
          <Link
            href="/auth/login"
            className="flex items-center justify-center gap-2 border-2 border-blue-600 text-blue-600 font-bold px-8 py-3 rounded-xl hover:bg-blue-50 transition-colors text-lg"
          >
            Sign In
          </Link>
        </div>
      </section>

      {/* How it works */}
      <section className="bg-white px-6 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-black text-center text-gray-900 mb-2">How it works</h2>
          <p className="text-center text-gray-500 mb-12">Three simple phases. One great piece of writing.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step, i) => (
              <div
                key={step.phase}
                className="flex flex-col items-center text-center p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="w-16 h-16 rounded-full bg-gray-50 flex items-center justify-center mb-4 shadow-inner">
                  {step.icon}
                </div>
                <span className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-1">
                  Step {i + 1}
                </span>
                <h3 className="text-lg font-black text-gray-900 mb-1">{step.phase} — {step.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Video demo */}
      <section className="bg-gray-50 px-6 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-black text-gray-900 mb-2">See it in action</h2>
          <p className="text-gray-500 mb-10">Watch how Kopi Write guides a student from idea to finished piece.</p>
          <div className="relative w-full rounded-2xl overflow-hidden shadow-xl" style={{ paddingBottom: '56.25%' }}>
            <iframe
              className="absolute inset-0 w-full h-full"
              src="https://www.youtube.com/embed/OxQ7juEHNo4"
              title="How Kopi Write works"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-blue-600 text-white text-center px-6 py-14">
        <h2 className="text-3xl font-black mb-3">Ready to become a better writer?</h2>
        <p className="text-blue-200 mb-8 text-lg">It's free to get started. No credit card needed.</p>
        <Link
          href="/auth/register"
          className="inline-flex items-center gap-2 bg-white text-blue-600 font-black px-10 py-3 rounded-xl hover:bg-blue-50 transition-colors text-lg shadow-md"
        >
          Create Your Account <ChevronRight className="w-5 h-5" />
        </Link>
      </section>

      <footer className="py-6 text-center text-gray-400 text-sm bg-white">
        Kopi Write AI Tutor — Empowering Every Writer
      </footer>
    </div>
  );
}

// ── Dashboard shown to authenticated users ───────────────────────────────────
export default function Home() {
  const { user, isLoading } = useAuth();
  const [topic, setTopic] = useState('Narrative');
  const [currentPhase, setCurrentPhase] = useState('Pre-writing');
  const [showReport, setShowReport] = useState(false);

  const topics = ['Narrative', 'Informational', 'Persuasive'];
  const phases = ['Pre-writing', 'Drafting', 'Revising', 'Editing', 'Publishing'];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Not logged in → show landing page
  if (!user) {
    return <LandingPage />;
  }

  // Logged in → show the writing tutor dashboard
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-xl flex justify-between items-center z-20">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 relative overflow-hidden rounded-lg shadow-inner bg-white p-0.5">
            <img
              src="/just_write_logo.jpg"
              alt="Kopi Write Logo"
              className="object-cover w-full h-full rounded"
            />
          </div>
          <h1 className="text-3xl font-black font-sans tracking-tight">Kopi Write</h1>
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
        Kopi Write AI Tutor — Empowering Every Writer
      </footer>
    </div>
  );
}
