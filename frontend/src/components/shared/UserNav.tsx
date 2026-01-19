"use client";

import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { User, LogOut, BarChart2, ChevronDown } from 'lucide-react';
import Link from 'next/link';

interface UserNavProps {
  onShowReport: () => void;
}

export default function UserNav({ onShowReport }: UserNavProps) {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) {
    return (
      <div className="flex items-center space-x-4">
        <Link 
          href="/auth/login" 
          className="text-white font-bold hover:text-blue-100 transition-colors"
        >
          Sign In
        </Link>
        <Link 
          href="/auth/register" 
          className="bg-white text-blue-600 px-4 py-2 rounded-lg font-bold hover:bg-blue-50 transition-colors shadow-sm"
        >
          Register
        </Link>
      </div>
    );
  }

  return (
    <div className="relative">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition-colors border border-blue-500 shadow-sm"
      >
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center font-bold">
          {user.username[0].toUpperCase()}
        </div>
        <span className="font-bold hidden md:inline">{user.username}</span>
        <ChevronDown size={16} className={`transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-xl py-2 border border-gray-100 z-50 overflow-hidden">
          <div className="px-4 py-2 border-b border-gray-50 mb-1">
            <p className="text-xs font-semibold text-gray-400 uppercase">Account</p>
            <p className="text-sm font-bold text-gray-700 truncate">{user.email}</p>
          </div>
          
          <button
            onClick={() => {
              onShowReport();
              setIsOpen(false);
            }}
            className="w-full flex items-center space-x-2 px-4 py-2 text-gray-600 hover:bg-blue-50 hover:text-blue-600 transition-colors"
          >
            <BarChart2 size={18} />
            <span className="font-semibold text-sm">View Progress</span>
          </button>

          <button
            onClick={() => {
              logout();
              setIsOpen(false);
            }}
            className="w-full flex items-center space-x-2 px-4 py-2 text-red-500 hover:bg-red-50 transition-colors"
          >
            <LogOut size={18} />
            <span className="font-semibold text-sm">Log Out</span>
          </button>
        </div>
      )}
    </div>
  );
}
