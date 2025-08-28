#!/usr/bin/env python3
"""
Script to set up test user data for the AI Credit Assessment Platform
"""

import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal, engine
from backend.models import user_models, credit_models
from backend.services.ai_models import CreditScoringModel

def setup_test_data():
    """Set up test user and profile data"""
    print("🔧 Setting up test data...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(user_models.User).filter(user_models.User.id == 1).first()
        
        if existing_user:
            print("✅ Test user already exists")
            return
        
        # Create test user
        test_user = user_models.User(
            id=1,
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print("✅ Created test user")
        
        # Create user profile
        test_profile = user_models.UserProfile(
            user_id=1,
            age=32,
            education_level="bachelors",
            job_title="Software Engineer",
            industry="Technology",
            years_experience=8,
            salary=75000,
            employment_status="full_time",
            housing_status="renting",
            monthly_rent=1500,
            mortgage_payment=0,
            property_value=0,
            monthly_income=6250,
            monthly_expenses=3800,
            savings_balance=15000,
            investment_balance=5000
        )
        
        db.add(test_profile)
        db.commit()
        print("✅ Created user profile")
        
        # Create credit history
        credit_history = credit_models.CreditHistory(
            user_id=1,
            credit_card_balance=2500,
            credit_card_limit=10000,
            loan_balance=15000,
            mortgage_balance=0,
            late_payments=1,
            missed_payments=0,
            credit_utilization_ratio=0.25
        )
        
        db.add(credit_history)
        db.commit()
        print("✅ Created credit history")
        
        # Create initial credit assessment
        credit_model = CreditScoringModel()
        credit_model.load_models()
        
        # Prepare user data for assessment
        user_data = {
            'monthly_income': 6250,
            'monthly_expenses': 3800,
            'savings_balance': 15000,
            'investment_balance': 5000,
            'age': 32,
            'education_level': 'bachelors',
            'job_title': 'Software Engineer',
            'industry': 'Technology',
            'years_experience': 8,
            'salary': 75000,
            'employment_status': 'full_time',
            'housing_status': 'renting',
            'monthly_rent': 1500,
            'mortgage_payment': 0,
            'property_value': 0,
            'job_stability_score': 0.8,
            'social_score': 0.7,
            'credit_card_balance': 2500,
            'credit_card_limit': 10000,
            'loan_balance': 15000,
            'late_payments': 1,
            'missed_payments': 0,
        }
        
        # Get AI prediction
        prediction = credit_model.predict_credit_score(user_data)
        
        # Create assessment
        assessment = credit_models.CreditAssessment(
            user_id=1,
            credit_score=prediction['credit_score'],
            risk_category=prediction['risk_category'],
            confidence_score=prediction['confidence_score'],
            financial_score=prediction['financial_score'],
            career_score=prediction['career_score'],
            housing_score=prediction['housing_score'],
            social_score=prediction['social_score'],
            factor_breakdown=prediction['factor_breakdown'],
            recommendations=prediction['recommendations'],
            risk_factors=prediction['risk_factors'],
            model_version=prediction['model_version']
        )
        
        db.add(assessment)
        db.commit()
        print("✅ Created initial credit assessment")
        
        print(f"🎯 Test user setup complete!")
        print(f"   User ID: 1")
        print(f"   Email: test@example.com")
        print(f"   Credit Score: {prediction['credit_score']:.0f}")
        print(f"   Risk Category: {prediction['risk_category']}")
        
    except Exception as e:
        print(f"❌ Error setting up test data: {e}")
        db.rollback()
    finally:
        db.close()

def test_simulation():
    """Test the simulation with the created user"""
    print("\n🧪 Testing simulation with test user...")
    
    import requests
    
    simulation_data = {
        "user_id": 1,
        "scenario_type": "salary_increase",
        "parameters": {
            "salary_increase": 10000
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/simulation/scenario",
            json=simulation_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Simulation working!")
            print(f"   Original Score: {result['original_score']:.0f}")
            print(f"   Simulated Score: {result['simulated_score']:.0f}")
            print(f"   Score Change: {result['score_change']:.0f}")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing simulation: {e}")

if __name__ == "__main__":
    setup_test_data()
    test_simulation()
