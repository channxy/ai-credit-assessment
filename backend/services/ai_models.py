import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, List, Tuple, Any
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import shap
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CreditScoringModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.model_version = "1.0.0"
        self.models_dir = "models"
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
    
    def load_models(self):
        """Load pre-trained models if they exist, otherwise train new ones"""
        try:
            model_path = os.path.join(self.models_dir, "credit_model.pkl")
            scaler_path = os.path.join(self.models_dir, "scaler.pkl")
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                logger.info("Loaded pre-trained models")
            else:
                logger.info("Training new models...")
                self._train_models()
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self._train_models()
    
    def _train_models(self):
        """Train the credit scoring model with synthetic data"""
        # Generate synthetic training data
        X, y = self._generate_synthetic_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train XGBoost model
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            objective='reg:squarederror'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Save models
        joblib.dump(self.model, os.path.join(self.models_dir, "credit_model.pkl"))
        joblib.dump(self.scaler, os.path.join(self.models_dir, "scaler.pkl"))
        
        # Evaluate model
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        logger.info(f"Model trained - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
    
    def _generate_synthetic_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Generate synthetic training data for credit scoring"""
        np.random.seed(42)
        n_samples = 10000
        
        # Generate synthetic features
        data = {
            # Financial features
            'monthly_income': np.random.normal(5000, 2000, n_samples),
            'monthly_expenses': np.random.normal(3000, 1000, n_samples),
            'savings_balance': np.random.exponential(10000, n_samples),
            'credit_card_balance': np.random.exponential(2000, n_samples),
            'credit_card_limit': np.random.normal(8000, 3000, n_samples),
            'loan_balance': np.random.exponential(15000, n_samples),
            'late_payments': np.random.poisson(1, n_samples),
            'missed_payments': np.random.poisson(0.5, n_samples),
            
            # Career features
            'years_experience': np.random.exponential(5, n_samples),
            'salary': np.random.normal(60000, 25000, n_samples),
            'job_stability_score': np.random.beta(2, 2, n_samples),
            
            # Housing features
            'housing_status_encoded': np.random.choice([0, 1, 2], n_samples, p=[0.4, 0.3, 0.3]),
            'monthly_rent': np.random.normal(1500, 500, n_samples),
            'mortgage_payment': np.random.normal(2000, 800, n_samples),
            'property_value': np.random.exponential(300000, n_samples),
            
            # Social features
            'education_level_encoded': np.random.choice([0, 1, 2, 3], n_samples, p=[0.2, 0.3, 0.3, 0.2]),
            'age': np.random.normal(35, 10, n_samples),
            'social_score': np.random.beta(3, 2, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate derived features
        df['income_expense_ratio'] = df['monthly_income'] / (df['monthly_expenses'] + 1)
        df['credit_utilization'] = df['credit_card_balance'] / (df['credit_card_limit'] + 1)
        df['savings_rate'] = (df['monthly_income'] - df['monthly_expenses']) / (df['monthly_income'] + 1)
        df['debt_to_income'] = (df['credit_card_balance'] + df['loan_balance']) / (df['monthly_income'] * 12 + 1)
        
        # Generate target credit scores (300-850 range)
        # Base score from financial health
        base_score = 300 + (df['income_expense_ratio'] * 100) + (df['savings_rate'] * 200)
        
        # Adjust for credit history
        credit_adjustment = -df['late_payments'] * 20 - df['missed_payments'] * 30
        credit_adjustment += (1 - df['credit_utilization']) * 100
        
        # Adjust for career stability
        career_adjustment = df['job_stability_score'] * 100 + df['years_experience'] * 5
        
        # Adjust for housing
        housing_adjustment = df['housing_status_encoded'] * 50
        
        # Adjust for education and age
        education_adjustment = df['education_level_encoded'] * 30
        age_adjustment = np.clip(df['age'] - 25, 0, 30) * 2
        
        # Calculate final score
        credit_scores = base_score + credit_adjustment + career_adjustment + housing_adjustment + education_adjustment + age_adjustment
        
        # Add some noise and clip to valid range
        credit_scores += np.random.normal(0, 30, n_samples)
        credit_scores = np.clip(credit_scores, 300, 850)
        
        # Store feature names
        self.feature_names = df.columns.tolist()
        
        return df, pd.Series(credit_scores)
    
    def predict_credit_score(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict credit score for a user"""
        try:
            # Prepare features
            features = self._prepare_features(user_data)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Make prediction
            credit_score = self.model.predict(features_scaled)[0]
            credit_score = np.clip(credit_score, 300, 850)
            
            # Calculate factor scores
            factor_scores = self._calculate_factor_scores(user_data)
            
            # Determine risk category
            risk_category = self._determine_risk_category(credit_score)
            
            # Generate explainability
            explanations = self._generate_explanations(user_data, factor_scores)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(user_data, factor_scores)
            
            return {
                'credit_score': float(credit_score),
                'risk_category': risk_category,
                'confidence_score': 0.85,  # Placeholder
                'financial_score': factor_scores['financial'],
                'career_score': factor_scores['career'],
                'housing_score': factor_scores['housing'],
                'social_score': factor_scores['social'],
                'factor_breakdown': explanations,
                'recommendations': recommendations,
                'risk_factors': self._identify_risk_factors(user_data, factor_scores),
                'model_version': self.model_version
            }
            
        except Exception as e:
            logger.error(f"Error predicting credit score: {e}")
            raise
    
    def _prepare_features(self, user_data: Dict[str, Any]) -> List[float]:
        """Prepare features for model prediction"""
        # Extract features from user data
        features = []
        
        # Financial features
        monthly_income = user_data.get('monthly_income', 0)
        monthly_expenses = user_data.get('monthly_expenses', 0)
        savings_balance = user_data.get('savings_balance', 0)
        credit_card_balance = user_data.get('credit_card_balance', 0)
        credit_card_limit = user_data.get('credit_card_limit', 1)
        loan_balance = user_data.get('loan_balance', 0)
        late_payments = user_data.get('late_payments', 0)
        missed_payments = user_data.get('missed_payments', 0)
        
        # Career features
        years_experience = user_data.get('years_experience', 0)
        salary = user_data.get('salary', 0)
        job_stability_score = user_data.get('job_stability_score', 0.5)
        
        # Housing features
        housing_status = user_data.get('housing_status', 'renting')
        monthly_rent = user_data.get('monthly_rent', 0)
        mortgage_payment = user_data.get('mortgage_payment', 0)
        property_value = user_data.get('property_value', 0)
        
        # Social features
        education_level = user_data.get('education_level', 'high_school')
        age = user_data.get('age', 30)
        social_score = user_data.get('social_score', 0.5)
        
        # Encode categorical variables
        housing_status_encoded = {'renting': 0, 'owned': 1, 'mortgaged': 2}.get(housing_status, 0)
        education_level_encoded = {'high_school': 0, 'bachelors': 1, 'masters': 2, 'phd': 3}.get(education_level, 0)
        
        # Calculate derived features
        income_expense_ratio = monthly_income / (monthly_expenses + 1)
        credit_utilization = credit_card_balance / (credit_card_limit + 1)
        savings_rate = (monthly_income - monthly_expenses) / (monthly_income + 1)
        debt_to_income = (credit_card_balance + loan_balance) / (monthly_income * 12 + 1)
        
        # Return feature vector
        return [
            monthly_income, monthly_expenses, savings_balance, credit_card_balance,
            credit_card_limit, loan_balance, late_payments, missed_payments,
            years_experience, salary, job_stability_score, housing_status_encoded,
            monthly_rent, mortgage_payment, property_value, education_level_encoded,
            age, social_score, income_expense_ratio, credit_utilization,
            savings_rate, debt_to_income
        ]
    
    def _calculate_factor_scores(self, user_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate individual factor scores"""
        # Financial score (0-100)
        monthly_income = user_data.get('monthly_income', 0)
        monthly_expenses = user_data.get('monthly_expenses', 0)
        savings_balance = user_data.get('savings_balance', 0)
        credit_card_balance = user_data.get('credit_card_balance', 0)
        credit_card_limit = user_data.get('credit_card_limit', 1)
        late_payments = user_data.get('late_payments', 0)
        
        income_expense_ratio = monthly_income / (monthly_expenses + 1)
        credit_utilization = credit_card_balance / (credit_card_limit + 1)
        
        financial_score = min(100, max(0, 
            50 + (income_expense_ratio * 20) + (savings_balance / 1000) - 
            (credit_utilization * 30) - (late_payments * 10)
        ))
        
        # Career score (0-100)
        years_experience = user_data.get('years_experience', 0)
        salary = user_data.get('salary', 0)
        job_stability_score = user_data.get('job_stability_score', 0.5)
        
        career_score = min(100, max(0,
            50 + (years_experience * 2) + (salary / 10000) + (job_stability_score * 30)
        ))
        
        # Housing score (0-100)
        housing_status = user_data.get('housing_status', 'renting')
        property_value = user_data.get('property_value', 0)
        
        housing_scores = {'renting': 30, 'owned': 80, 'mortgaged': 60}
        housing_score = housing_scores.get(housing_status, 30) + (property_value / 100000)
        housing_score = min(100, max(0, housing_score))
        
        # Social score (0-100)
        education_level = user_data.get('education_level', 'high_school')
        age = user_data.get('age', 30)
        social_score = user_data.get('social_score', 0.5)
        
        education_scores = {'high_school': 30, 'bachelors': 60, 'masters': 80, 'phd': 90}
        education_base = education_scores.get(education_level, 30)
        
        social_score_final = min(100, max(0,
            education_base + (age - 25) * 0.5 + (social_score * 20)
        ))
        
        return {
            'financial': financial_score,
            'career': career_score,
            'housing': housing_score,
            'social': social_score_final
        }
    
    def _determine_risk_category(self, credit_score: float) -> str:
        """Determine risk category based on credit score"""
        if credit_score >= 750:
            return "excellent"
        elif credit_score >= 700:
            return "good"
        elif credit_score >= 650:
            return "fair"
        elif credit_score >= 600:
            return "poor"
        else:
            return "very_poor"
    
    def _generate_explanations(self, user_data: Dict[str, Any], factor_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate explanations for the credit score"""
        explanations = {
            'financial_factors': {
                'income_expense_ratio': f"Your income is {user_data.get('monthly_income', 0) / (user_data.get('monthly_expenses', 1) + 1):.1f}x your expenses",
                'savings_rate': f"You save ${user_data.get('monthly_income', 0) - user_data.get('monthly_expenses', 0):.0f} monthly",
                'credit_utilization': f"Credit utilization: {user_data.get('credit_card_balance', 0) / (user_data.get('credit_card_limit', 1) + 1) * 100:.1f}%"
            },
            'career_factors': {
                'experience': f"{user_data.get('years_experience', 0)} years of experience",
                'salary': f"Annual salary: ${user_data.get('salary', 0):,.0f}",
                'stability': f"Job stability score: {user_data.get('job_stability_score', 0.5) * 100:.0f}%"
            },
            'housing_factors': {
                'status': f"Housing status: {user_data.get('housing_status', 'renting')}",
                'property_value': f"Property value: ${user_data.get('property_value', 0):,.0f}" if user_data.get('property_value', 0) > 0 else "No property owned"
            },
            'social_factors': {
                'education': f"Education: {user_data.get('education_level', 'high_school')}",
                'age': f"Age: {user_data.get('age', 30)}",
                'social_score': f"Social score: {user_data.get('social_score', 0.5) * 100:.0f}%"
            }
        }
        
        return explanations
    
    def _generate_recommendations(self, user_data: Dict[str, Any], factor_scores: Dict[str, float]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Financial recommendations
        if factor_scores['financial'] < 50:
            recommendations.append("Consider reducing monthly expenses to improve your financial score")
            recommendations.append("Focus on building emergency savings")
        
        if user_data.get('credit_card_balance', 0) > user_data.get('credit_card_limit', 1) * 0.3:
            recommendations.append("Reduce credit card utilization to below 30%")
        
        # Career recommendations
        if factor_scores['career'] < 50:
            recommendations.append("Consider upskilling or pursuing additional certifications")
            recommendations.append("Look for opportunities to increase your salary")
        
        # Housing recommendations
        if factor_scores['housing'] < 50:
            recommendations.append("Consider homeownership as it typically improves credit scores")
        
        # General recommendations
        if len(recommendations) == 0:
            recommendations.append("Your credit profile looks good! Keep maintaining healthy financial habits")
        
        return recommendations
    
    def _identify_risk_factors(self, user_data: Dict[str, Any], factor_scores: Dict[str, float]) -> List[str]:
        """Identify potential risk factors"""
        risk_factors = []
        
        if user_data.get('late_payments', 0) > 0:
            risk_factors.append(f"{user_data['late_payments']} late payments in recent history")
        
        if user_data.get('missed_payments', 0) > 0:
            risk_factors.append(f"{user_data['missed_payments']} missed payments")
        
        if user_data.get('credit_card_balance', 0) > user_data.get('credit_card_limit', 1) * 0.8:
            risk_factors.append("High credit card utilization")
        
        if user_data.get('monthly_expenses', 0) > user_data.get('monthly_income', 1) * 0.9:
            risk_factors.append("High debt-to-income ratio")
        
        if user_data.get('job_stability_score', 1) < 0.3:
            risk_factors.append("Low job stability")
        
        return risk_factors
