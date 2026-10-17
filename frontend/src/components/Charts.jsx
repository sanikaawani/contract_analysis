import React from 'react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend
} from 'recharts';

export function CategoryRadarChart({ data }) {
  // Format data for radar
  const formattedData = data.map(item => ({
    subject: item.category.replace(' Clauses', '').replace(' Terms', ''),
    score: item.risk_score,
    fullCategory: item.category
  }));

  return (
    <div className="w-full h-72 flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={formattedData}>
          <PolarGrid stroke="#334155" strokeDasharray="3 3" />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 600 }} 
          />
          <PolarRadiusAxis 
            angle={30} 
            domain={[0, 100]} 
            stroke="#475569" 
            tick={{ fill: '#64748b', fontSize: 10 }} 
          />
          <Radar
            name="Risk Exposure (0-100)"
            dataKey="score"
            stroke="#ef4444"
            fill="#ef4444"
            fillOpacity={0.4}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
            itemStyle={{ color: '#f8fafc' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function RiskDistributionPieChart({ counts }) {
  const data = [
    { name: 'High Risk', value: counts.high_risk || 0, color: '#ef4444' },
    { name: 'Medium Risk', value: counts.medium_risk || 0, color: '#f59e0b' },
    { name: 'Low / Safe', value: counts.low_risk || 0, color: '#10b981' },
  ].filter(d => d.value > 0);

  return (
    <div className="w-full h-64 flex flex-col items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={80}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
            itemStyle={{ color: '#f8fafc' }}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36} 
            formatter={(value) => <span className="text-xs text-slate-300 font-medium">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function CategoryBarChart({ data }) {
  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis type="number" domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 11, fill: '#64748b' }} />
          <YAxis 
            type="category" 
            dataKey="category" 
            stroke="#64748b" 
            tick={{ fontSize: 11, fill: '#94a3b8', width: 120 }} 
            width={130}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
            itemStyle={{ color: '#f8fafc' }}
          />
          <Bar dataKey="risk_score" name="Risk Score (0-100)" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => {
              const color = entry.severity === 'High' ? '#ef4444' : (entry.severity === 'Medium' ? '#f59e0b' : '#10b981');
              return <Cell key={`cell-bar-${index}`} fill={color} />;
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
