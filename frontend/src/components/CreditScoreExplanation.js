import React from 'react';
import { Info, CheckCircle, AlertCircle, XCircle, HelpCircle } from 'lucide-react';

const CreditScoreExplanation = ({ score, showDetails = false }) => {
  const getScoreRange = (score) => {
    if (score >= 800) return { range: '800-850', category: 'Exceptional', color: 'text-green-600', bgColor: 'bg-green-50', icon: CheckCircle };
    if (score >= 740) return { range: '740-799', category: 'Very Good', color: 'text-green-500', bgColor: 'bg-green-50', icon: CheckCircle };
    if (score >= 670) return { range: '670-739', category: 'Good', color: 'text-blue-600', bgColor: 'bg-blue-50', icon: CheckCircle };
    if (score >= 580) return { range: '580-669', category: 'Fair', color: 'text-yellow-600', bgColor: 'bg-yellow-50', icon: AlertCircle };
    if (score >= 300) return { range: '300-579', category: 'Poor', color: 'text-red-600', bgColor: 'bg-red-50', icon: XCircle };
    return { range: 'N/A', category: 'Unknown', color: 'text-gray-600', bgColor: 'bg-gray-50', icon: HelpCircle };
  };

  const getLoanApprovalInfo = (score) => {
    if (score >= 800) {
      return {
        approval: 'Very High',
        rates: 'Best Available',
        description: 'Excellent credit score. You qualify for the best interest rates and terms on loans and credit cards.',
        benefits: ['Lowest interest rates', 'Highest credit limits', 'Best loan terms', 'Premium credit cards']
      };
    } else if (score >= 740) {
      return {
        approval: 'High',
        rates: 'Very Good',
        description: 'Very good credit score. You qualify for competitive interest rates and favorable loan terms.',
        benefits: ['Competitive interest rates', 'High credit limits', 'Good loan terms', 'Most credit cards available']
      };
    } else if (score >= 670) {
      return {
        approval: 'Good',
        rates: 'Good',
        description: 'Good credit score. You qualify for most loans and credit cards with reasonable terms.',
        benefits: ['Reasonable interest rates', 'Good credit limits', 'Standard loan terms', 'Most credit cards available']
      };
    } else if (score >= 580) {
      return {
        approval: 'Fair',
        rates: 'Higher',
        description: 'Fair credit score. You may qualify for loans but with higher interest rates and stricter terms.',
        benefits: ['Higher interest rates', 'Lower credit limits', 'Stricter terms', 'Limited credit card options']
      };
    } else {
      return {
        approval: 'Low',
        rates: 'Very High',
        description: 'Poor credit score. You may have difficulty getting approved for loans and credit cards.',
        benefits: ['Very high interest rates', 'Low credit limits', 'Strict terms', 'Limited options']
      };
    }
  };

  const scoreInfo = getScoreRange(score);
  const loanInfo = getLoanApprovalInfo(score);
  const Icon = scoreInfo.icon;

  return (
    <div className="space-y-4">
      {/* Score Range Display */}
      <div className={`p-4 rounded-lg border ${scoreInfo.bgColor}`}>
        <div className="flex items-center space-x-3">
          <Icon className={`h-6 w-6 ${scoreInfo.color}`} />
          <div>
            <h3 className={`font-semibold ${scoreInfo.color}`}>
              {scoreInfo.category} Credit Score
            </h3>
            <p className="text-sm text-gray-600">
              Range: {scoreInfo.range} | Your Score: {score?.toFixed(2) || 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Loan Approval Information */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
          <Info className="h-5 w-5 mr-2 text-blue-600" />
          Loan Approval & Interest Rates
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">Approval Likelihood</p>
            <p className="text-xl font-bold text-gray-900">{loanInfo.approval}</p>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">Interest Rates</p>
            <p className="text-xl font-bold text-gray-900">{loanInfo.rates}</p>
          </div>
        </div>

        <p className="text-gray-700 mb-4">{loanInfo.description}</p>

        <div className="space-y-2">
          <h4 className="font-medium text-gray-900">What this means for you:</h4>
          <ul className="space-y-1">
            {loanInfo.benefits.map((benefit, index) => (
              <li key={index} className="flex items-center text-sm text-gray-600">
                <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                {benefit}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Credit Score Ranges Reference */}
      {showDetails && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Credit Score Ranges</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <div>
                  <p className="font-medium text-green-800">Exceptional (800-850)</p>
                  <p className="text-sm text-green-600">Best rates and terms available</p>
                </div>
              </div>
              <span className="text-sm font-medium text-green-800">Excellent</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <div>
                  <p className="font-medium text-green-700">Very Good (740-799)</p>
                  <p className="text-sm text-green-600">Competitive rates and terms</p>
                </div>
              </div>
              <span className="text-sm font-medium text-green-700">Very Good</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="font-medium text-blue-800">Good (670-739)</p>
                  <p className="text-sm text-blue-600">Reasonable rates and terms</p>
                </div>
              </div>
              <span className="text-sm font-medium text-blue-800">Good</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <AlertCircle className="h-5 w-5 text-yellow-600" />
                <div>
                  <p className="font-medium text-yellow-800">Fair (580-669)</p>
                  <p className="text-sm text-yellow-600">Higher rates and stricter terms</p>
                </div>
              </div>
              <span className="text-sm font-medium text-yellow-800">Fair</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <XCircle className="h-5 w-5 text-red-600" />
                <div>
                  <p className="font-medium text-red-800">Poor (300-579)</p>
                  <p className="text-sm text-red-600">Limited options and high rates</p>
                </div>
              </div>
              <span className="text-sm font-medium text-red-800">Poor</span>
            </div>
          </div>
        </div>
      )}

      {/* Tips for Improving Credit Score */}
      <div className="card bg-blue-50 border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">Tips to Improve Your Credit Score</h3>
        <div className="space-y-2">
          <div className="flex items-start space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
            <p className="text-sm text-blue-800">Pay all bills on time, every time</p>
          </div>
          <div className="flex items-start space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
            <p className="text-sm text-blue-800">Keep credit card balances below 30% of your limit</p>
          </div>
          <div className="flex items-start space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
            <p className="text-sm text-blue-800">Don't close old credit accounts</p>
          </div>
          <div className="flex items-start space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
            <p className="text-sm text-blue-800">Limit new credit applications</p>
          </div>
          <div className="flex items-start space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
            <p className="text-sm text-blue-800">Build a mix of credit types over time</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreditScoreExplanation;
