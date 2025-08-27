import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, Target, TrendingUp, CheckCircle, AlertTriangle } from 'lucide-react';

const Recommendations = () => {
  const [activeTab, setActiveTab] = useState('priority');

  const recommendations = {
    priority: [
      'Focus on reducing high-interest debt immediately',
      'Establish emergency savings fund',
      'Review and reduce monthly expenses',
      'Consider credit counseling services'
    ],
    financial: [
      'Create a detailed budget and track all expenses',
      'Set up automatic savings transfers',
      'Pay more than minimum on credit cards',
      'Consider debt consolidation options',
      'Reduce credit card utilization from 28.5% to below 30%'
    ],
    career: [
      'Consider professional development opportunities',
      'Research salary benchmarks for your role',
      'Build industry-specific skills',
      'Network within your professional community'
    ],
    housing: [
      'Consider homeownership when financially ready',
      'Build savings for down payment',
      'Improve credit score to qualify for better mortgage rates'
    ]
  };

  const improvementPlan = {
    currentScore: 725,
    targetScore: 750,
    pointsNeeded: 25,
    timeline: 12,
    monthlyGoals: [
      { month: 1, target: 730, focus: ['Payment history', 'Credit utilization', 'Emergency fund'] },
      { month: 2, target: 735, focus: ['Payment history', 'Credit utilization', 'Emergency fund'] },
      { month: 3, target: 740, focus: ['Payment history', 'Credit utilization', 'Emergency fund'] },
      { month: 6, target: 745, focus: ['Debt reduction', 'Income increase', 'Credit mix'] },
      { month: 9, target: 748, focus: ['Credit history length', 'New credit applications', 'Financial stability'] },
      { month: 12, target: 750, focus: ['Maintenance', 'Optimization', 'Long-term planning'] }
    ]
  };

  const tabs = [
    { id: 'priority', label: 'Priority', icon: AlertTriangle },
    { id: 'financial', label: 'Financial', icon: TrendingUp },
    { id: 'career', label: 'Career', icon: Target },
    { id: 'housing', label: 'Housing', icon: CheckCircle }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Recommendations</h1>
          <p className="text-gray-600 mt-1">Personalized financial advice and improvement plan</p>
        </div>
        <button className="btn btn-primary">
          <Lightbulb className="h-4 w-4 mr-2" />
          Generate New Recommendations
        </button>
      </div>

      {/* Credit Score Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        <div className="card">
          <div className="text-center">
            <p className="text-sm text-gray-600">Current Score</p>
            <p className="text-3xl font-bold text-gray-900">{improvementPlan.currentScore}</p>
          </div>
        </div>
        <div className="card">
          <div className="text-center">
            <p className="text-sm text-gray-600">Target Score</p>
            <p className="text-3xl font-bold text-blue-600">{improvementPlan.targetScore}</p>
          </div>
        </div>
        <div className="card">
          <div className="text-center">
            <p className="text-sm text-gray-600">Points Needed</p>
            <p className="text-3xl font-bold text-green-600">+{improvementPlan.pointsNeeded}</p>
          </div>
        </div>
      </motion.div>

      {/* Recommendations Tabs */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        <div className="space-y-4">
          {recommendations[activeTab].map((recommendation, index) => (
            <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
              <p className="text-gray-700">{recommendation}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Improvement Plan */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">12-Month Improvement Plan</h2>
        
        <div className="space-y-4">
          {improvementPlan.monthlyGoals.map((goal) => (
            <div key={goal.month} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-medium text-gray-900">Month {goal.month}</h3>
                <span className="text-lg font-bold text-blue-600">Target: {goal.target}</span>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-gray-600">Focus Areas:</p>
                <div className="flex flex-wrap gap-2">
                  {goal.focus.map((area, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                    >
                      {area}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Success Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Success Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="font-medium text-green-800 mb-2">Credit Utilization Target</h3>
            <p className="text-green-700">Below 30%</p>
          </div>
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-medium text-blue-800 mb-2">Payment History Target</h3>
            <p className="text-blue-700">100% on-time payments</p>
          </div>
          <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
            <h3 className="font-medium text-purple-800 mb-2">Savings Rate Target</h3>
            <p className="text-purple-700">20% of income</p>
          </div>
          <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
            <h3 className="font-medium text-orange-800 mb-2">Debt-to-Income Target</h3>
            <p className="text-orange-700">Below 36%</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Recommendations;
