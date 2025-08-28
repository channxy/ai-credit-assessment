import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calculator, TrendingUp, TrendingDown, Home, DollarSign, Briefcase, Loader } from 'lucide-react';
import { simulationAPI } from '../services/api';
import CreditScoreExplanation from '../components/CreditScoreExplanation';

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
  const [simulationResult, setSimulationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [simulationHistory, setSimulationHistory] = useState([]);
  
  // Test data for debugging
  const testResult = {
    original_score: 756.32,
    simulated_score: 788.32,
    score_change: 32.00,
    factor_changes: {
      "salary": "+$10,000",
      "monthly_income": "+$833"
    },
    recommendations: [
      "This scenario would improve your credit score by 32.00 points",
      "Higher income typically improves creditworthiness and borrowing capacity"
    ]
  };

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

  // Load simulation history on component mount
  useEffect(() => {
    loadSimulationHistory();
  }, []);

  const loadSimulationHistory = async () => {
    try {
      const history = await simulationAPI.getSimulationHistory(1); // Using user ID 1 for demo
      setSimulationHistory(history);
    } catch (error) {
      console.error('Failed to load simulation history:', error);
    }
  };

  const runSimulation = async () => {
    setIsLoading(true);
    setError(null);
    setSimulationResult(null);

    try {
      // Prepare simulation request
      const simulationRequest = {
        user_id: 1, // Using user ID 1 for demo
        scenario_type: selectedScenario,
        parameters: simulationParams
      };

      console.log('Running simulation with:', simulationRequest);
      
      const result = await simulationAPI.runSimulation(simulationRequest);
      console.log('Simulation result:', result);
      console.log('Setting simulation result state...');
      setSimulationResult(result);
      console.log('Simulation result state set');
      
      // Reload simulation history
      await loadSimulationHistory();
      
    } catch (error) {
      console.error('Simulation failed:', error);
      setError(error.response?.data?.detail || 'Failed to run simulation');
    } finally {
      setIsLoading(false);
    }
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
          disabled={isLoading}
          className="btn btn-primary mr-2"
        >
          {isLoading ? (
            <Loader className="h-4 w-4 mr-2 animate-spin" />
          ) : (
            <Calculator className="h-4 w-4 mr-2" />
          )}
          {isLoading ? 'Running...' : 'Run Simulation'}
        </button>
        <button 
          onClick={() => setSimulationResult(testResult)}
          className="btn btn-secondary"
        >
          Test Results
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

      {/* Debug Info */}
      <div className="card bg-gray-50">
        <h3 className="font-medium text-gray-900 mb-2">Debug Info</h3>
        <div className="text-sm text-gray-600">
          <p>Loading: {isLoading ? 'true' : 'false'}</p>
          <p>Error: {error || 'none'}</p>
          <p>Simulation Result: {simulationResult ? 'exists' : 'null'}</p>
          <p>Selected Scenario: {selectedScenario}</p>
          {simulationResult && (
            <div className="mt-2 p-2 bg-white rounded border">
              <p><strong>Result Data:</strong></p>
              <pre className="text-xs overflow-auto">
                {JSON.stringify(simulationResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card bg-red-50 border-red-200"
        >
          <div className="text-red-800">
            <h3 className="font-medium">Simulation Error</h3>
            <p className="text-sm">{error}</p>
          </div>
        </motion.div>
      )}

      {/* Simulation Results */}
      {simulationResult ? (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Simulation Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <p className="text-sm text-gray-600">Current Score</p>
              <p className="text-3xl font-bold text-gray-900">{simulationResult.original_score?.toFixed(2)}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Simulated Score</p>
              <p className={`text-3xl font-bold ${simulationResult.score_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {simulationResult.simulated_score?.toFixed(2)}
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Score Change</p>
              <p className={`text-3xl font-bold ${simulationResult.score_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {simulationResult.score_change >= 0 ? '+' : ''}{simulationResult.score_change?.toFixed(2)}
              </p>
            </div>
          </div>
          
          {simulationResult.factor_changes && Object.keys(simulationResult.factor_changes).length > 0 && (
            <div className="mt-6">
              <h3 className="font-medium text-gray-900 mb-3">Factor Changes</h3>
              <div className="space-y-2">
                {Object.entries(simulationResult.factor_changes).map(([factor, change]) => (
                  <div key={factor} className="flex justify-between">
                    <span className="text-gray-600">{factor}</span>
                    <span className="font-medium text-green-600">{change}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {simulationResult.recommendations && simulationResult.recommendations.length > 0 && (
            <div className="mt-6">
              <h3 className="font-medium text-gray-900 mb-3">Recommendations</h3>
              <div className="space-y-2">
                {simulationResult.recommendations.map((recommendation, index) => (
                  <div key={index} className="text-sm text-gray-700 bg-blue-50 p-3 rounded-lg">
                    {recommendation}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Credit Score Explanation */}
          <div className="mt-6">
            <CreditScoreExplanation 
              score={simulationResult.simulated_score} 
              showDetails={true}
            />
          </div>
        </div>
      ) : (
        <div className="card">
          <p className="text-gray-600">No simulation results yet. Click "Run Simulation" to see results.</p>
        </div>
      )}

      {/* Simulation History */}
      {simulationHistory.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Simulation History</h2>
          <div className="space-y-3">
            {simulationHistory.slice(0, 5).map((sim) => (
              <div key={sim.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-medium text-gray-900 capitalize">{sim.scenario_type.replace('_', ' ')}</h3>
                    <p className="text-sm text-gray-600">
                      {new Date(sim.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Score Change</p>
                    <p className={`font-bold ${sim.score_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {sim.score_change >= 0 ? '+' : ''}{sim.score_change}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Simulation;
