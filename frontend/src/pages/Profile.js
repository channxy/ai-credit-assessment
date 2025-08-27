import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Edit, Save, X } from 'lucide-react';

const Profile = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState({
    personal: {
      fullName: 'John Doe',
      email: 'john.doe@example.com',
      age: 32,
      educationLevel: 'bachelors',
      degreeField: 'Computer Science'
    },
    career: {
      jobTitle: 'Software Engineer',
      industry: 'Technology',
      yearsExperience: 5,
      salary: 78000,
      employmentStatus: 'full_time'
    },
    housing: {
      housingStatus: 'renting',
      monthlyRent: 1200,
      mortgagePayment: 0,
      propertyValue: 0
    },
    financial: {
      monthlyIncome: 6500,
      monthlyExpenses: 3200,
      savingsBalance: 25000,
      investmentBalance: 15000,
      creditCardBalance: 2800,
      creditCardLimit: 10000
    }
  });

  const [editProfile, setEditProfile] = useState(profile);

  const handleEdit = () => {
    setEditProfile(profile);
    setIsEditing(true);
  };

  const handleSave = () => {
    setProfile(editProfile);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditProfile(profile);
    setIsEditing(false);
  };

  const handleChange = (section, field, value) => {
    setEditProfile(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const currentData = isEditing ? editProfile : profile;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600 mt-1">Manage your personal and financial information</p>
        </div>
        <div className="flex space-x-2">
          {isEditing ? (
            <>
              <button onClick={handleSave} className="btn btn-success">
                <Save className="h-4 w-4 mr-2" />
                Save
              </button>
              <button onClick={handleCancel} className="btn btn-secondary">
                <X className="h-4 w-4 mr-2" />
                Cancel
              </button>
            </>
          ) : (
            <button onClick={handleEdit} className="btn btn-primary">
              <Edit className="h-4 w-4 mr-2" />
              Edit Profile
            </button>
          )}
        </div>
      </div>

      {/* Profile Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Personal Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <User className="h-5 w-5 text-blue-600 mr-2" />
            <h2 className="text-xl font-semibold text-gray-900">Personal Information</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              {isEditing ? (
                <input
                  type="text"
                  value={currentData.personal.fullName}
                  onChange={(e) => handleChange('personal', 'fullName', e.target.value)}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">{currentData.personal.fullName}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              {isEditing ? (
                <input
                  type="email"
                  value={currentData.personal.email}
                  onChange={(e) => handleChange('personal', 'email', e.target.value)}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">{currentData.personal.email}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.personal.age}
                  onChange={(e) => handleChange('personal', 'age', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">{currentData.personal.age}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Education Level</label>
              {isEditing ? (
                <select
                  value={currentData.personal.educationLevel}
                  onChange={(e) => handleChange('personal', 'educationLevel', e.target.value)}
                  className="input"
                >
                  <option value="high_school">High School</option>
                  <option value="bachelors">Bachelor's Degree</option>
                  <option value="masters">Master's Degree</option>
                  <option value="phd">PhD</option>
                </select>
              ) : (
                <p className="text-gray-900 capitalize">{currentData.personal.educationLevel.replace('_', ' ')}</p>
              )}
            </div>
          </div>
        </motion.div>

        {/* Career Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Career Information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
              {isEditing ? (
                <input
                  type="text"
                  value={currentData.career.jobTitle}
                  onChange={(e) => handleChange('career', 'jobTitle', e.target.value)}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">{currentData.career.jobTitle}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
              {isEditing ? (
                <input
                  type="text"
                  value={currentData.career.industry}
                  onChange={(e) => handleChange('career', 'industry', e.target.value)}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">{currentData.career.industry}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Years of Experience</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.career.yearsExperience}
                  onChange={(e) => handleChange('career', 'yearsExperience', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">{currentData.career.yearsExperience}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Annual Salary</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.career.salary}
                  onChange={(e) => handleChange('career', 'salary', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">${currentData.career.salary.toLocaleString()}</p>
              )}
            </div>
          </div>
        </motion.div>

        {/* Housing Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Housing Information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Housing Status</label>
              {isEditing ? (
                <select
                  value={currentData.housing.housingStatus}
                  onChange={(e) => handleChange('housing', 'housingStatus', e.target.value)}
                  className="input"
                >
                  <option value="renting">Renting</option>
                  <option value="owned">Owned</option>
                  <option value="mortgaged">Mortgaged</option>
                </select>
              ) : (
                <p className="text-gray-900 capitalize">{currentData.housing.housingStatus}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Rent</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.housing.monthlyRent}
                  onChange={(e) => handleChange('housing', 'monthlyRent', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">${currentData.housing.monthlyRent.toLocaleString()}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Property Value</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.housing.propertyValue}
                  onChange={(e) => handleChange('housing', 'propertyValue', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">
                  {currentData.housing.propertyValue > 0 
                    ? `$${currentData.housing.propertyValue.toLocaleString()}` 
                    : 'No property owned'
                  }
                </p>
              )}
            </div>
          </div>
        </motion.div>

        {/* Financial Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Financial Information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Income</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.financial.monthlyIncome}
                  onChange={(e) => handleChange('financial', 'monthlyIncome', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">${currentData.financial.monthlyIncome.toLocaleString()}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Expenses</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.financial.monthlyExpenses}
                  onChange={(e) => handleChange('financial', 'monthlyExpenses', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">${currentData.financial.monthlyExpenses.toLocaleString()}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Savings Balance</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.financial.savingsBalance}
                  onChange={(e) => handleChange('financial', 'savingsBalance', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">${currentData.financial.savingsBalance.toLocaleString()}</p>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Credit Card Balance</label>
              {isEditing ? (
                <input
                  type="number"
                  value={currentData.financial.creditCardBalance}
                  onChange={(e) => handleChange('financial', 'creditCardBalance', parseInt(e.target.value))}
                  className="input"
                />
              ) : (
                <p className="text-gray-900">${currentData.financial.creditCardBalance.toLocaleString()}</p>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Profile;
