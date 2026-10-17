import React from 'react';
import { Building2, Calendar, IndianRupee, Clock, UserCheck } from 'lucide-react';

export default function EntityBadge({ type, value }) {
  const configs = {
    organizations: {
      label: 'Organization',
      icon: Building2,
      style: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
    },
    dates: {
      label: 'Date',
      icon: Calendar,
      style: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    },
    money_amounts: {
      label: 'Financial Term',
      icon: IndianRupee,
      style: 'bg-amber-500/10 text-amber-400 border-amber-500/30'
    },
    contract_durations: {
      label: 'Duration / Notice',
      icon: Clock,
      style: 'bg-purple-500/10 text-purple-400 border-purple-500/30'
    },
    person_names: {
      label: 'Signatory / Person',
      icon: UserCheck,
      style: 'bg-blue-500/10 text-blue-400 border-blue-500/30'
    }
  };

  const cfg = configs[type] || {
    label: type,
    icon: Building2,
    style: 'bg-slate-800 text-slate-300 border-slate-700'
  };
  const Icon = cfg.icon;

  return (
    <span className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-medium border ${cfg.style} transition-all hover:scale-105`}>
      <Icon className="w-3.5 h-3.5 shrink-0" />
      <span className="font-mono">{value}</span>
    </span>
  );
}
