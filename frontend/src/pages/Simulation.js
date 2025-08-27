import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Calculator, TrendingUp, TrendingDown, Home, DollarSign, Briefcase } from 'lucide-react';

const Simulation = () => {
  const [selectedScenario, setSelectedScenario] = useState('salary_increase');
  const [simulationParams, setSimulationParams] = useState({
    salary_increase: 10000,
    new_salary: 85000,
    new_industry: 'Technology',
    property_value: 350000,
    down_payment: 70000,
    monthly_payment: 1800,
    debt_reduction: 5000,
    expense_reduction: 500
  });

  const scenarios = [
    {
      id: 'salary_increase',
      title: 'Salary Increase',
      icon: TrendingUp,
      description: 'Simulate the impact of a salary increase on your credit score',
      color: 'green'
    },
    {
      id: 'job_change',
      title: 'Job Change',
      icon: Briefcase,
      description: 'See how changing jobs affects your creditworthiness',
      color: 'blue'
    },
    {
      id: 'house_purchase',
      title: 'House Purchase',
      icon: Home,
      description: 'Analyze the impact of buying a home on your credit score',
      color: 'purple'
    },
    {
      id: 'debt_reduction',
      title: 'Debt Reduction',
      icon: TrendingDown,
      description: 'Calculate the benefits of reducing your debt',
      color: 'orange'
    },
    {
      id: 'expense_reduction',
      title: 'Expense Reduction',
      icon: DollarSign,
      description: 'See how cutting expenses improves your financial health',
      color: 'red'
    }
  ];

  const handleScenarioChange = (scenarioId) => {
    setSelectedScenario(scenarioId);
  };

  const handleParamChange = (param, value) => {
    setSimulationParams(prev => ({
      ...prev,
      [param]: value
    }));
  };

  const runSimulation = () => {
    // Mock simulation result
    const mockResult = {
      originalScore: 725,
      simulatedScore: 745,
      scoreChange: 20,
      factorChanges: {
        'Income': '+$10,000',
        'Monthly Income': '+$833',
        'Debt-to-Income': 'Improved'
      },
      recommendations: [
        'This salary increase would improve your credit score by 20 points',
        'Higher income typically improves creditworthiness and borrowing capacity'
      ]
    };
    
    // In a real app, this would call the API
    console.log('Running simulation with:', { selectedScenario, simulationParams });
    console.log('Result:', mockResult);
  };

  const getScenarioIcon = (scenario) => {
    const Icon = scenario.icon;
    return <Icon className={`h-6 w-6 text-${scenario.color}-600`} />;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Scenario Simulation</h1>
          <p className="text-gray-600 mt-1">Test how life changes affect your credit score</p>
        </div>
        <button 
          onClick={runSimulation}
          className="btn btn-primary"
        >
          <Calculator className="h-4 w-4 mr-2" />
          Run Simulation
        </button>
      </div>

      {/* Scenario Selection */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Choose a Scenario</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {scenarios.map((scenario) => (
            <div
              key={scenario.id}
              onClick={() => handleScenarioChange(scenario.id)}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                selectedScenario === scenario.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center space-x-3">
                {getScenarioIcon(scenario)}
                <div>
                  <h3 className="font-medium text-gray-900">{scenario.title}</h3>
                  <p className="text-sm text-gray-600">{scenario.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Scenario Parameters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Scenario Parameters</h2>
        
        {selectedScenario === 'salary_increase' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Annual Salary Increase
              </label>
              <input
                type="number"
                value={simulationParams.salary_increase}
                onChange={(e) => handleParamChange('salary_increase', parseInt(e.target.value))}
                className="input"
                placeholder="Enter amount"
              />
            </div>
          </div>
        )}

        {selectedScenario === 'job_change' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                New Annual Salary
              </label>
              <input
                type="number"
                value={simulationParams.new_salary}
                onChange={(e) => handleParamChange('new_salary', parseInt(e.target.value))}
                className="input"
                placeholder="Enter new salary"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                New Industry
              </label>
              <select
                value={simulationParams.new_industry}
                onChange={(e) => handleParamChange('new_industry', e.target.value)}
                className="input"
              >
                <option value="Technology">Technology</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Finance">Finance</option>
                <option value="Education">Education</option>
                <option value="Manufacturing">Manufacturing</option>
              </select>
            </div>
          </div>
        )}

        {selectedScenario === 'house_purchase' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Property Value
              </label>
              <input
                type="number"
                value={simulationParams.property_value}
                onChange={(e) => handleParamChange('property_value', parseInt(e.target.value))}
                className="input"
                placeholder="Enter property value"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Down Payment
              </label>
              <input
                type="number"
                value={simulationParams.down_payment}
                onChange={(e) => handleParamChange('down_payment', parseInt(e.target.value))}
                className="input"
                placeholder="Enter down payment"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monthly Mortgage Payment
              </label>
              <input
                type="number"
                value={simulationParams.monthly_payment}
                onChange={(e) => handleParamChange('monthly_payment', parseInt(e.target.value))}
                className="input"
                placeholder="Enter monthly payment"
              />
            </div>
          </div>
        )}

        {selectedScenario === 'debt_reduction' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Debt Reduction Amount
              </label>
              <input
                type="number"
                value={simulationParams.debt_reduction}
                onChange={(e) => handleParamChange('debt_reduction', parseInt(e.target.value))}
                className="input"
                placeholder="Enter amount to reduce"
              />
            </div>
          </div>
        )}

        {selectedScenario === 'expense_reduction' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monthly Expense Reduction
              </label>
              <input
                type="number"
                value={simulationParams.expense_reduction}
                onChange={(e) => handleParamChange('expense_reduction', parseInt(e.target.value))}
                className="input"
                placeholder="Enter monthly reduction"
              />
            </div>
          </div>
        )}
      </motion.div>

      {/* Simulation Results (Mock) */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card"
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Simulation Results</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <p className="text-sm text-gray-600">Current Score</p>
            <p className="text-3xl font-bold text-gray-900">725</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Simulated Score</p>
            <p className="text-3xl font-bold text-green-600">745</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Score Change</p>
            <p className="text-3xl font-bold text-green-600">+20</p>
          </div>
        </div>
        
        <div className="mt-6">
          <h3 className="font-medium text-gray-900 mb-3">Factor Changes</h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Income</span>
              <span className="font-medium text-green-600">+$10,000</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Monthly Income</span>
              <span className="font-medium text-green-600">+$833</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Debt-to-Income</span>
              <span className="font-medium text-green-600">Improved</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Simulation;
