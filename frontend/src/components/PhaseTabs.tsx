"use client";

import React, { useState } from 'react';
import { Youtube, HelpCircle, PenTool, ChevronDown, ChevronUp, FileText, CheckCircle, Award, Sparkles, Loader2, Trophy, Target, ArrowRight } from 'lucide-react';
import SocraticChat from './SocraticChat';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';
import { API_BASE_URL } from '@/utils/api';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts';

interface EvaluationData {
  scores: {
    Focus: number;
    Content: number;
    Organization: number;
    Style: number;
    Conventions: number;
  };
  feedback: {
    Focus: string;
    Content: string;
    Organization: string;
    Style: string;
    Conventions: string;
  };
  celebrations: string[];
  growth_goals: string[];
}

interface Prompt {
  id: number;
  topic: string;
  prompt_text: string;
  assignment_type: string;
}

interface LessonContent {
  video_url: string;
  content_html: string;
}

interface PhaseTabsProps {
  phase: string;
  topic: string;
}

export default function PhaseTabs({ phase, topic }: PhaseTabsProps) {
  const { user, token } = useAuth();
  const [activeSub, setActiveSub] = useState<'i-do' | 'we-do' | 'you-do'>('i-do');
  const [writingContent, setWritingContent] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evaluation, setEvaluation] = useState<EvaluationData | null>(null);
  const [evaluationError, setEvaluationError] = useState<string | null>(null);
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null);
  const [isLoadingPrompts, setIsLoadingPrompts] = useState(false);
  const [lessonContent, setLessonContent] = useState<LessonContent | null>(null);
  const [isLoadingLesson, setIsLoadingLesson] = useState(false);

  React.useEffect(() => {
    // Reset selection when changing phase or topic
    setSelectedPrompt(null);
    setPrompts([]);
    setLessonContent(null);
    
    if (user) {
      if (activeSub === 'we-do' || activeSub === 'you-do') {
        fetchPrompts();
      } else if (activeSub === 'i-do') {
        fetchLesson();
      }
    }
  }, [activeSub, topic, phase, user]);

  const fetchPrompts = async () => {
    if (!token) return;
    setIsLoadingPrompts(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/tutor/prompts`, {
        params: {
          topic: topic,
          assignment_type: activeSub
        },
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setPrompts(response.data);
    } catch (error) {
      console.error("Error fetching prompts:", error);
    } finally {
      setIsLoadingPrompts(false);
    }
  };

  const fetchLesson = async () => {
    if (!token) return;
    setIsLoadingLesson(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/tutor/lesson`, {
        params: { topic, phase },
        headers: { Authorization: `Bearer ${token}` }
      });
      setLessonContent(response.data);
    } catch (error) {
      console.error("Error fetching lesson:", error);
    } finally {
      setIsLoadingLesson(false);
    }
  };

  const handleEvaluate = async () => {
    if (!writingContent.trim() || isEvaluating) return;

    setIsEvaluating(true);
    setEvaluation(null);

    try {
      setEvaluationError(null);
      const response = await axios.post(`${API_BASE_URL}/tutor/evaluate`, {
        text: writingContent,
        topic: topic,
        prompt: selectedPrompt?.prompt_text
      });
      setEvaluation(response.data);
    } catch (error: any) {
      console.error("Evaluation error:", error);
      if (axios.isAxiosError(error) && error.response) {
        if (error.response.status === 503) {
          setEvaluationError('AI service unavailable. Admins: rotate GOOGLE_API_KEY and check AI billing/permissions.');
        } else if (error.response.status === 429) {
          setEvaluationError('Google API quota reached. Please wait 1-2 minutes before trying to evaluate again.');
        } else if (error.response.data?.detail) {
          setEvaluationError(error.response.data.detail);
        } else {
          setEvaluationError('Evaluation failed due to server error.');
        }
      } else {
        setEvaluationError('Network error. Please try again.');
      }
    } finally {
      setIsEvaluating(false);
    }
  };

  const scoreChartData = evaluation ? Object.entries(evaluation.scores).map(([key, value]) => ({
    subject: key,
    score: value,
    fullMark: 4
  })) : [];

  const subPhases = [
    { id: 'i-do', label: 'I DO', icon: <Youtube className="mr-2" />, description: 'Watch and Learn' },
    { id: 'we-do', label: 'WE DO', icon: <HelpCircle className="mr-2" />, description: 'Work with Coach' },
    { id: 'you-do', label: 'YOU DO', icon: <PenTool className="mr-2" />, description: 'Try on Your Own' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-black text-gray-800 uppercase tracking-tight">{phase} Phase</h2>
          <p className="text-gray-600 font-medium">Currently working on: <span className="text-blue-600 underline decoration-2">{topic} Writing</span></p>
        </div>
      </div>

      {/* Sub-phase selection (Tabs) */}
      <div className="flex space-x-2 bg-gray-100 p-1 rounded-xl">
        {subPhases.map((sub) => (
          <button
            key={sub.id}
            onClick={() => setActiveSub(sub.id as any)}
            className={`flex-1 flex items-center justify-center py-3 rounded-lg font-bold transition-all ${
              activeSub === sub.id 
                ? 'bg-white text-blue-600 shadow-md transform scale-105' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {sub.icon}
            {sub.label}
          </button>
        ))}
      </div>

      {/* Accordion-style Content */}
      <div className="mt-6 border-2 border-gray-100 rounded-2xl p-6 bg-white shadow-inner">
        {activeSub === 'i-do' && (
          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {isLoadingLesson ? (
              <div className="flex flex-col items-center justify-center p-12">
                <Loader2 className="animate-spin text-blue-600 mb-4" size={48} />
                <p className="text-gray-500 font-medium">Loading your lesson...</p>
              </div>
            ) : (
              <>
                <h3 className="text-xl font-bold mb-4 flex items-center text-blue-800">
                  <Youtube className="mr-2" /> Teacher Lesson: {phase}
                </h3>
                <div className="aspect-video bg-black rounded-xl overflow-hidden mb-6 shadow-xl">
                  <iframe 
                    width="100%" 
                    height="100%" 
                    src={`https://www.youtube.com/embed/${lessonContent?.video_url || 'dQw4w9WgXcQ'}`}
                    title="Teacher Lesson" 
                    frameBorder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowFullScreen
                  ></iframe>
                </div>
                
                <div className="bg-blue-50 p-6 rounded-xl border-l-4 border-blue-500 mb-8">
                  <div 
                    className="prose prose-blue max-w-none text-gray-800"
                    dangerouslySetInnerHTML={{ __html: lessonContent?.content_html || `<p>No lesson content found for ${user?.grade_level || 3}th Grade ${topic} - ${phase}.</p><p class="text-sm text-gray-500 mt-2">Try checking the database seed or switching topics.</p>` }}
                  />
                </div>
              </>
            )}

            <div className="bg-white p-6 rounded-xl border-2 border-blue-100">
              <h4 className="font-bold text-blue-800 mb-4 flex items-center text-lg">
                <FileText className="mr-2" size={22} /> Lesson Reference: Grade 3 Writing Guidelines
              </h4>
              <div className="h-[600px] bg-white border-2 border-blue-100 rounded-lg overflow-hidden shadow-inner font-sans">
                <iframe 
                  src="/Grade3_PSSA.pdf" 
                  className="w-full h-full"
                  title="Lesson PDF"
                ></iframe>
              </div>
            </div>
          </div>
        )}

        {activeSub === 'we-do' && (
          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {!selectedPrompt ? (
              <div className="space-y-6">
                <div className="text-center space-y-2">
                  <h3 className="text-2xl font-bold text-green-800">Choose your practice prompt!</h3>
                  <p className="text-gray-600 italic">Pick one of these topics to work on with your writing coach.</p>
                </div>
                {isLoadingPrompts ? (
                  <div className="flex justify-center p-12">
                     <Loader2 className="animate-spin text-green-600" size={48} />
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {prompts.length > 0 ? (
                      prompts.map((p) => (
                        <button
                          key={p.id}
                          onClick={() => setSelectedPrompt(p)}
                          className="p-6 text-left border-2 border-green-50 rounded-2xl hover:border-green-400 hover:bg-green-50 transition-all group bg-white shadow-sm"
                        >
                          <p className="text-lg text-gray-800 font-medium group-hover:text-green-800 transition-colors">{p.prompt_text}</p>
                          <div className="mt-4 flex items-center text-green-600 font-bold text-sm opacity-0 group-hover:opacity-100 transition-opacity">
                            Pick this one <ArrowRight size={16} className="ml-2" />
                          </div>
                        </button>
                      ))
                    ) : (
                      <div className="col-span-full text-center p-8 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
                        <p className="text-gray-500">No practice prompts found for {user?.grade_level}th Grade {topic} {activeSub}.</p>
                        <p className="text-sm text-gray-400 mt-2">Try switching topics or checking your grade level.</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex justify-between items-center bg-green-50 p-4 rounded-xl border border-green-100">
                  <div>
                    <span className="text-xs font-bold text-green-600 uppercase tracking-widest">Active Prompt</span>
                    <p className="text-lg font-bold text-green-900">{selectedPrompt.prompt_text}</p>
                  </div>
                  <button 
                    onClick={() => setSelectedPrompt(null)}
                    className="text-sm font-bold text-green-700 hover:underline"
                  >
                    Change Prompt
                  </button>
                </div>
                <h3 className="text-xl font-bold flex items-center text-green-800">
                  <HelpCircle className="mr-2" /> Chat with Writing Coach
                </h3>
                <div className="h-[500px] border-2 border-green-100 rounded-2xl overflow-hidden shadow-sm">
                  <SocraticChat topic={topic} phase={phase} prompt={selectedPrompt.prompt_text} />
                </div>
              </div>
            )}
          </div>
        )}

        {activeSub === 'you-do' && (
          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {!selectedPrompt ? (
               <div className="space-y-6">
                <div className="text-center space-y-2">
                  <h3 className="text-2xl font-bold text-purple-800">Independent Writing Challenge</h3>
                  <p className="text-gray-600 italic">Pick a prompt and show what you can do on your own!</p>
                </div>
                {isLoadingPrompts ? (
                  <div className="flex justify-center p-12">
                     <Loader2 className="animate-spin text-purple-600" size={48} />
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {prompts.length > 0 ? (
                      prompts.map((p) => (
                        <button
                          key={p.id}
                          onClick={() => setSelectedPrompt(p)}
                          className="p-6 text-left border-2 border-purple-50 rounded-2xl hover:border-purple-400 hover:bg-purple-50 transition-all group bg-white shadow-sm"
                        >
                          <p className="text-lg text-gray-800 font-medium group-hover:text-purple-800 transition-colors">{p.prompt_text}</p>
                          <div className="mt-4 flex items-center text-purple-600 font-bold text-sm opacity-0 group-hover:opacity-100 transition-opacity">
                            Start Writing <ArrowRight size={16} className="ml-2" />
                          </div>
                        </button>
                      ))
                    ) : (
                      <div className="col-span-full text-center p-8 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
                        <p className="text-gray-500">No writing prompts found for {user?.grade_level}th Grade {topic} {activeSub}.</p>
                        <p className="text-sm text-gray-400 mt-2">Try switching topics or checking your grade level.</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : (
              <div>
                {/* Independent Writing Content */}
                <div className="flex justify-between items-center bg-purple-50 p-4 rounded-xl border border-purple-100 mb-6">
                  <div>
                    <span className="text-xs font-bold text-purple-600 uppercase tracking-widest">Active Prompt</span>
                    <p className="text-lg font-bold text-purple-900">{selectedPrompt.prompt_text}</p>
                  </div>
                  <button 
                    onClick={() => setSelectedPrompt(null)}
                    className="text-sm font-bold text-purple-700 hover:underline"
                  >
                    Change Prompt
                  </button>
                </div>
                
                <h3 className="text-xl font-bold mb-4 flex items-center text-purple-800">
                  <PenTool className="mr-2" /> Independent Writing
                </h3>
                
                {evaluation ? (
                  <div className="space-y-8 animate-in zoom-in duration-300">
                    {evaluationError && (
                      <div className="bg-red-50 border border-red-100 text-red-700 p-3 rounded mb-4">
                        {evaluationError}
                      </div>
                    )}
                    <div className="bg-white rounded-2xl border-2 border-purple-100 shadow-sm overflow-hidden">
                      <div className="bg-purple-600 p-4 text-white flex justify-between items-center">
                        <h4 className="text-xl font-bold flex items-center">
                          <Trophy className="mr-2" /> PSSA Writing Evaluation
                        </h4>
                        <button 
                          onClick={() => setEvaluation(null)}
                          className="bg-white/20 hover:bg-white/30 px-3 py-1 rounded text-sm font-bold transition-colors"
                        >
                          Back to Editor
                        </button>
                      </div>

                      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Visual Charts */}
                        <div className="bg-gray-50 rounded-xl p-4 border border-gray-100 flex flex-col items-center">
                          <p className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Skill Analysis</p>
                          <div className="w-full h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                              <RadarChart data={scoreChartData}>
                                <PolarGrid />
                                <PolarAngleAxis dataKey="subject" tick={{ fill: '#6b7280', fontSize: 12, fontWeight: 'bold' }} />
                                <PolarRadiusAxis angle={30} domain={[0, 4]} />
                                <Radar
                                  name="Score"
                                  dataKey="score"
                                  stroke="#9333ea"
                                  fill="#9333ea"
                                  fillOpacity={0.6}
                                />
                              </RadarChart>
                            </ResponsiveContainer>
                          </div>
                        </div>

                        <div className="space-y-4">
                          <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">Score Summary</p>
                          <div className="grid grid-cols-1 gap-3">
                            {Object.entries(evaluation.scores).map(([key, score]) => (
                              <div key={key} className="flex items-center space-x-4 bg-white p-3 rounded-lg border border-gray-100 shadow-sm">
                                <div className="w-24 text-sm font-bold text-gray-600">{key}</div>
                                <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
                                  <div 
                                    className={`h-full rounded-full ${
                                      score >= 3.5 ? 'bg-green-500' : 
                                      score >= 2.5 ? 'bg-blue-500' : 
                                      'bg-yellow-500'
                                    }`}
                                    style={{ width: `${(score / 4) * 100}%` }}
                                  />
                                </div>
                                <div className="text-lg font-black text-purple-700">{score}<span className="text-xs text-gray-400 font-normal">/4</span></div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="p-6 border-t border-gray-100">
                        <h5 className="font-black text-gray-800 mb-6 flex items-center text-lg uppercase tracking-tight">
                          <FileText className="mr-2 text-purple-600" /> Detailed Performance Feedback
                        </h5>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          {Object.entries(evaluation.feedback).map(([key, text]) => (
                            <div key={key} className="bg-white p-4 rounded-xl border border-purple-50 shadow-sm">
                              <p className="font-black text-purple-600 text-sm mb-2 uppercase tracking-wide">{key}</p>
                              <p className="text-gray-700 leading-relaxed text-sm">{text}</p>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 bg-gray-50 border-t border-gray-100">
                        <div className="p-6 border-b md:border-b-0 md:border-r border-gray-100">
                          <h5 className="font-bold text-green-700 mb-4 flex items-center">
                            <Trophy className="mr-2" /> Celebrations
                          </h5>
                          <ul className="space-y-3">
                            {evaluation.celebrations.map((c, i) => (
                              <li key={i} className="flex items-start text-gray-700 text-sm">
                                <CheckCircle size={16} className="text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                                <span>{c}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div className="p-6">
                          <h5 className="font-bold text-blue-700 mb-4 flex items-center">
                            <Target className="mr-2" /> Growth Goals
                          </h5>
                          <ul className="space-y-3">
                            {evaluation.growth_goals.map((g, i) => (
                              <li key={i} className="flex items-start text-gray-700 text-sm">
                                <ArrowRight size={16} className="text-blue-500 mt-0.5 mr-2 flex-shrink-0" />
                                <span>{g}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div className="flex justify-center space-x-4">
                      <button 
                        onClick={() => setEvaluation(null)}
                        className="bg-white border-2 border-purple-600 text-purple-600 font-bold py-3 px-8 rounded-full shadow-md hover:bg-purple-50 transition-all"
                      >
                        Edit Again
                      </button>
                      {phase === 'Publishing' && (
                        <button className="bg-green-600 hover:bg-green-700 text-white font-black py-4 px-12 rounded-full shadow-xl transform transition-transform hover:scale-110 active:scale-95 flex items-center text-xl">
                          Publish My Work! <Award className="ml-3" size={28} />
                        </button>
                      )}
                    </div>
                  </div>
                ) : (
                  <>
                    <p className="mb-4 text-gray-600 font-medium">Use what we learned to write your {topic.toLowerCase()} piece here!</p>
                    
                    {evaluationError && (
                      <div className="bg-red-50 border-2 border-red-200 text-red-700 p-4 rounded-xl mb-6 flex items-start">
                        <div className="bg-red-100 p-1 rounded-full mr-3 mt-0.5">
                          <HelpCircle className="text-red-600" size={18} />
                        </div>
                        <div>
                          <p className="font-bold">Check Failed</p>
                          <p className="text-sm opacity-90">{evaluationError}</p>
                        </div>
                      </div>
                    )}

                    <textarea 
                      value={writingContent}
                      onChange={(e) => setWritingContent(e.target.value)}
                      className="w-full h-96 p-6 border-2 border-purple-100 rounded-2xl focus:ring-4 focus:ring-purple-200 outline-none text-lg leading-relaxed shadow-sm font-sans"
                      placeholder={`Start writing your ${topic.toLowerCase()} piece...`}
                    ></textarea>
                    <div className="mt-4 flex justify-end space-x-3">
                      <button 
                        onClick={handleEvaluate}
                        disabled={isEvaluating || !writingContent.trim()}
                        className="bg-purple-600 hover:bg-purple-700 disabled:bg-purple-300 text-white font-black py-3 px-8 rounded-full shadow-lg transform transition-transform hover:scale-105 active:scale-95 flex items-center"
                      >
                        {isEvaluating ? (
                          <>Checking... <Loader2 className="ml-2 animate-spin" /></>
                        ) : (
                          <>Submit for Check <CheckCircle className="ml-2" /></>
                        )}
                      </button>
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
