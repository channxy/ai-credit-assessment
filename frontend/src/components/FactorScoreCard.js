import React from 'react';

const FactorScoreCard = ({ title, score, icon: Icon, color }) => {
  const getColorClasses = (color) => {
    switch (color) {
      case 'blue':
        return {
          bg: 'bg-blue-100',
          text: 'text-blue-600',
          bar: 'bg-blue-500'
        };
      case 'green':
        return {
          bg: 'bg-green-100',
          text: 'text-green-600',
          bar: 'bg-green-500'
        };
      case 'purple':
        return {
          bg: 'bg-purple-100',
          text: 'text-purple-600',
          bar: 'bg-purple-500'
        };
      case 'orange':
        return {
          bg: 'bg-orange-100',
          text: 'text-orange-600',
          bar: 'bg-orange-500'
        };
      default:
        return {
          bg: 'bg-gray-100',
          text: 'text-gray-600',
          bar: 'bg-gray-500'
        };
    }
  };

  const colorClasses = getColorClasses(color);

  return (
    <div className="p-4 border border-gray-200 rounded-lg bg-white">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <div className={`p-2 rounded-lg ${colorClasses.bg}`}>
            <Icon className={`h-4 w-4 ${colorClasses.text}`} />
          </div>
          <span className="text-sm font-medium text-gray-900">{title}</span>
        </div>
        <span className="text-lg font-bold text-gray-900">{score}</span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${colorClasses.bar} transition-all duration-500`}
          style={{ width: `${score}%` }}
        ></div>
      </div>
      
      <div className="flex justify-between text-xs text-gray-500 mt-1">
        <span>0</span>
        <span>100</span>
      </div>
    </div>
  );
};

export default FactorScoreCard;
