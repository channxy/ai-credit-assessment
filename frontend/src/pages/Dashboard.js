import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  CreditCard,
  Home,
  Briefcase,
  Users,
  AlertTriangle
} from 'lucide-react';
import CreditScoreGauge from '../components/CreditScoreGauge';
import FactorScoreCard from '../components/FactorScoreCard';
import RecentTransactions from '../components/RecentTransactions';
import CreditScoreExplanation from '../components/CreditScoreExplanation';
import { api } from '../services/api';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // For demo purposes, we'll use mock data
        const mockData = {
          creditScore: 756.32,
          riskCategory: 'good',
          factorScores: {
            financial: 78,
            career: 85,
            housing: 65,
            social: 72
          },
          recentTransactions: [
            { id: 1, amount: 2500, type: 'income', category: 'Salary', date: '2024-01-15' },
            { id: 2, amount: -1200, type: 'expense', category: 'Rent', date: '2024-01-14' },
            { id: 3, amount: -450, type: 'expense', category: 'Groceries', date: '2024-01-13' },
            { id: 4, amount: -200, type: 'expense', category: 'Utilities', date: '2024-01-12' }
          ],
          keyMetrics: {
            monthlyIncome: 6500,
            monthlyExpenses: 3200,
            savingsRate: 0.23,
            creditUtilization: 0.28
          }
        };
        
        setDashboardData(mockData);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <AlertTriangle className="mx-auto h-12 w-12 text-red-500 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Dashboard</h3>
        <p className="text-gray-600">{error}</p>
      </div>
    );
  }

  const { creditScore, riskCategory, factorScores, recentTransactions, keyMetrics } = dashboardData;

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
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Your financial health overview</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Last updated</p>
          <p className="text-sm font-medium text-gray-900">
            {new Date().toLocaleDateString()}
          </p>
        </div>
      </div>

      {/* Credit Score Section */}
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
              <span className={`badge ${getRiskCategoryColor(riskCategory)}`}>
                {riskCategory.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            <div className="flex justify-center">
              <CreditScoreGauge score={creditScore} />
            </div>
            <div className="text-center mt-4">
              <p className="text-2xl font-bold text-gray-900">{creditScore}</p>
              <p className="text-sm text-gray-600">out of 850</p>
            </div>
          </div>
        </div>

        {/* Factor Scores */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Factor Scores</h2>
            <div className="grid grid-cols-2 gap-4">
              <FactorScoreCard
                title="Financial"
                score={factorScores.financial}
                icon={DollarSign}
                color="blue"
              />
              <FactorScoreCard
                title="Career"
                score={factorScores.career}
                icon={Briefcase}
                color="green"
              />
              <FactorScoreCard
                title="Housing"
                score={factorScores.housing}
                icon={Home}
                color="purple"
              />
              <FactorScoreCard
                title="Social"
                score={factorScores.social}
                icon={Users}
                color="orange"
              />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Monthly Income</p>
              <p className="text-2xl font-bold text-gray-900">
                ${keyMetrics.monthlyIncome.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <TrendingDown className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Monthly Expenses</p>
              <p className="text-2xl font-bold text-gray-900">
                ${keyMetrics.monthlyExpenses.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Savings Rate</p>
              <p className="text-2xl font-bold text-gray-900">
                {(keyMetrics.savingsRate * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <CreditCard className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Credit Utilization</p>
              <p className="text-2xl font-bold text-gray-900">
                {(keyMetrics.creditUtilization * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Credit Score Explanation */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <CreditScoreExplanation 
          score={creditScore} 
          showDetails={false}
        />
      </motion.div>

      {/* Recent Transactions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <RecentTransactions transactions={recentTransactions} />
      </motion.div>
    </div>
  );
};

export default Dashboard;
