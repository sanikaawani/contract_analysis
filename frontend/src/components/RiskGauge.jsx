import React from 'react';
import { ShieldAlert, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function RiskGauge({ score = 0, grade = 'N/A', badge = 'Medium', size = 'default' }) {
  // Determine color scheme based on score
  const isHigh = score >= 65;
  const isMedium = score >= 40 && score < 65;
  
  const strokeColor = isHigh ? '#ef4444' : isMedium ? '#f59e0b' : '#10b981';
  const bgColor = isHigh ? 'bg-red-500/10 border-red-500/30 text-red-400' : isMedium ? 'bg-amber-500/10 border-amber-500/30 text-amber-400' : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400';
  const Icon = isHigh ? ShieldAlert : isMedium ? AlertTriangle : ShieldCheck;

  // SVG Gauge calculations
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference * 0.75; // 270 degree arc

  return (
    <div className="flex flex-col items-center justify-center p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl relative overflow-hidden">
      
      {/* Background glow */}
      <div 
        className={`absolute -top-10 -right-10 w-36 h-36 rounded-full blur-3xl opacity-20 ${
          isHigh ? 'bg-red-500' : isMedium ? 'bg-amber-500' : 'bg-emerald-500'
        }`}
      />

      <div className="relative w-40 h-40 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-135" viewBox="0 0 160 160">
          {/* Background circle track */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            fill="transparent"
            stroke="#1e293b"
            strokeWidth="12"
            strokeDasharray={circumference * 0.75}
            strokeLinecap="round"
          />
          {/* Active progress arc */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            fill="transparent"
            stroke={strokeColor}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold tracking-tight text-white font-mono">
            {score}
          </span>
          <span className="text-[11px] font-semibold text-slate-400 tracking-wider uppercase">
            / 100
          </span>
        </div>
      </div>

      {/* Grade and Badge */}
      <div className="mt-2 text-center">
        <div className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold border ${bgColor}`}>
          <Icon className="w-3.5 h-3.5" />
          <span>{badge} Risk</span>
        </div>
        <p className="text-xs text-slate-400 mt-2 font-medium">{grade}</p>
      </div>

    </div>
  );
}
