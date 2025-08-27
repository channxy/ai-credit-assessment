import React, { useEffect, useRef } from 'react';

const CreditScoreGauge = ({ score }) => {
  const progressRef = useRef(null);

  useEffect(() => {
    if (progressRef.current) {
      const percentage = (score / 850) * 100;
      const circumference = 2 * Math.PI * 90; // radius = 90
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
      <svg width="200" height="200" viewBox="0 0 200 200">
        {/* Background circle */}
        <circle
          cx="100"
          cy="100"
          r="90"
          className="background"
        />
        
        {/* Progress circle */}
        <circle
          ref={progressRef}
          cx="100"
          cy="100"
          r="90"
          className="progress"
          style={{
            stroke: getScoreColor(score),
            strokeDasharray: 2 * Math.PI * 90,
            strokeDashoffset: 2 * Math.PI * 90,
          }}
        />
        
        {/* Center text */}
        <text
          x="100"
          y="85"
          textAnchor="middle"
          className="text-2xl font-bold"
          fill="#1f2937"
        >
          {score}
        </text>
        
        <text
          x="100"
          y="105"
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
