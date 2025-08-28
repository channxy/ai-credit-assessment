import React, { useEffect, useRef } from 'react';

const CreditScoreGauge = ({ score }) => {
  const progressRef = useRef(null);

  useEffect(() => {
    if (progressRef.current) {
      const percentage = (score / 850) * 100;
      // For a semi-circle gauge, we use half the circumference
      const circumference = Math.PI * 90; // radius = 90, half circle
      const offset = circumference - (percentage / 100) * circumference;
      progressRef.current.style.strokeDashoffset = offset;
    }
  }, [score]);

  const getScoreColor = (score) => {
    if (score >= 750) return '#10b981'; // green
    if (score >= 700) return '#3b82f6'; // blue
    if (score >= 650) return '#f59e0b'; // yellow
    if (score >= 600) return '#f97316'; // orange
    return '#ef4444'; // red
  };

  const getScoreLabel = (score) => {
    if (score >= 750) return 'Excellent';
    if (score >= 700) return 'Good';
    if (score >= 650) return 'Fair';
    if (score >= 600) return 'Poor';
    return 'Very Poor';
  };

  return (
    <div className="credit-gauge">
      <svg width="200" height="120" viewBox="0 0 200 120">
        {/* Background semi-circle */}
        <path
          d="M 10 110 A 90 90 0 0 1 190 110"
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="8"
        />
        
        {/* Progress semi-circle */}
        <path
          ref={progressRef}
          d="M 10 110 A 90 90 0 0 1 190 110"
          fill="none"
          stroke={getScoreColor(score)}
          strokeWidth="8"
          strokeLinecap="round"
          style={{
            strokeDasharray: Math.PI * 90,
            strokeDashoffset: Math.PI * 90,
          }}
        />
        
        {/* Gauge markers */}
        {[300, 450, 600, 750, 850].map((mark, index) => {
          const angle = (index * Math.PI) / 4; // Distribute markers evenly
          const x = 100 + 85 * Math.cos(angle);
          const y = 110 - 85 * Math.sin(angle);
          const x2 = 100 + 95 * Math.cos(angle);
          const y2 = 110 - 95 * Math.sin(angle);
          
          return (
            <g key={mark}>
              <line
                x1={x}
                y1={y}
                x2={x2}
                y2={y2}
                stroke="#9ca3af"
                strokeWidth="2"
              />
              <text
                x={100 + 105 * Math.cos(angle)}
                y={110 - 105 * Math.sin(angle)}
                textAnchor="middle"
                className="text-xs"
                fill="#6b7280"
              >
                {mark}
              </text>
            </g>
          );
        })}
        
        {/* Center text */}
        <text
          x="100"
          y="95"
          textAnchor="middle"
          className="text-2xl font-bold"
          fill="#1f2937"
        >
          {score?.toFixed(2)}
        </text>
        
        <text
          x="100"
          y="115"
          textAnchor="middle"
          className="text-sm"
          fill="#6b7280"
        >
          {getScoreLabel(score)}
        </text>
      </svg>
    </div>
  );
};

export default CreditScoreGauge;
