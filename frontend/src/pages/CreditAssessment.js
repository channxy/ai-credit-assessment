import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import CreditScoreGauge from '../components/CreditScoreGauge';

const CreditAssessment = () => {
  const [assessmentData, setAssessmentData] = useState({
    creditScore: 725,
    riskCategory: 'good',
    factorBreakdown: {
      financial_factors: {
        income_expense_ratio: 'Your income is 2.0x your expenses',
        savings_rate: 'You save $3,300 monthly',
        credit_utilization: 'Credit utilization: 28.5%'
      },
      career_factors: {
        experience: '5 years of experience',
        salary: 'Annual salary: $78,000',
        stability: 'Job stability score: 70%'
      },
      housing_factors: {
        status: 'Housing status: renting',
        property_value: 'No property owned'
      },
      social_factors: {
        education: 'Education: bachelors',
        age: 'Age: 32',
        social_score: 'Social score: 60%'
      }
    },
    recommendations: [
      'Consider reducing monthly expenses to improve your financial score',
      'Focus on building emergency savings',
      'Reduce credit card utilization to below 30%'
    ],
    riskFactors: [
      'High credit card utilization',
      'Low job stability'
    ]
  });

  const getRiskCategoryColor = (category) => {
    switch (category) {
      case 'excellent': return 'text-green-600 bg-green-100';
      case 'good': return 'text-blue-600 bg-blue-100';
      case 'fair': return 'text-yellow-600 bg-yellow-100';
      case 'poor': return 'text-orange-600 bg-orange-100';
      case 'very_poor': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Credit Assessment</h1>
          <p className="text-gray-600 mt-1">AI-powered credit score analysis</p>
        </div>
        <button className="btn btn-primary">
          <BarChart3 className="h-4 w-4 mr-2" />
          Run New Assessment
        </button>
      </div>

      {/* Credit Score Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="grid grid-cols-1 lg:grid-cols-3 gap-6"
      >
        {/* Credit Score Gauge */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Credit Score</h2>
              <span className={`badge ${getRiskCategoryColor(assessmentData.riskCategory)}`}>
                {assessmentData.riskCategory.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            <div className="flex justify-center">
              <CreditScoreGauge score={assessmentData.creditScore} />
            </div>
            <div className="text-center mt-4">
              <p className="text-2xl font-bold text-gray-900">{assessmentData.creditScore}</p>
              <p className="text-sm text-gray-600">out of 850</p>
            </div>
          </div>
        </div>

        {/* Factor Breakdown */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Factor Breakdown</h2>
            <div className="space-y-4">
              {Object.entries(assessmentData.factorBreakdown).map(([category, factors]) => (
                <div key={category} className="border border-gray-200 rounded-lg p-4">
                  <h3 className="font-medium text-gray-900 mb-2 capitalize">
                    {category.replace('_', ' ')}
                  </h3>
                  <div className="space-y-2">
                    {Object.entries(factors).map(([factor, value]) => (
                      <div key={factor} className="flex justify-between text-sm">
                        <span className="text-gray-600 capitalize">
                          {factor.replace('_', ' ')}:
                        </span>
                        <span className="font-medium text-gray-900">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Recommendations and Risk Factors */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        {/* Recommendations */}
        <div className="card">
          <div className="flex items-center mb-4">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Recommendations</h2>
          </div>
          <div className="space-y-3">
            {assessmentData.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                <p className="text-gray-700">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Factors */}
        <div className="card">
          <div className="flex items-center mb-4">
            <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Risk Factors</h2>
          </div>
          <div className="space-y-3">
            {assessmentData.riskFactors.map((factor, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                <p className="text-gray-700">{factor}</p>
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Action Items */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Next Steps</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn btn-primary">
            <TrendingUp className="h-4 w-4 mr-2" />
            Run Simulation
          </button>
          <button className="btn btn-secondary">
            <BarChart3 className="h-4 w-4 mr-2" />
            View History
          </button>
          <button className="btn btn-success">
            <CheckCircle className="h-4 w-4 mr-2" />
            Get Recommendations
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default CreditAssessment;
