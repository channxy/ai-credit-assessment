#!/usr/bin/env python3
"""
Test script to demonstrate OpenAI integration in the AI Credit Assessment Platform
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

load_dotenv()

def test_openai_service():
    """Test the OpenAI service functionality"""
    print("🤖 Testing OpenAI Integration...")
    
    try:
        from services.openai_service import OpenAIService
        
        # Initialize the service
        openai_service = OpenAIService()
        
        print(f"✅ OpenAI Service initialized")
        print(f"🔑 OpenAI Available: {openai_service.is_available()}")
        print(f"🤖 Model: {openai_service.model}")
        
        # Test with sample data
        user_data = {
            'age': 32,
            'monthly_income': 6500,
            'monthly_expenses': 3800,
            'housing_status': 'mortgaged',
            'years_experience': 8,
            'education_level': 'bachelors',
            'credit_card_balance': 2500,
            'credit_card_limit': 10000,
            'savings_balance': 15000,
            'late_payments': 0,
            'missed_payments': 0
        }
        
        factor_scores = {
            'financial': 78,
            'career': 82,
            'housing': 75,
            'social': 70
        }
        
        credit_score = 725
        
        print("\n📊 Sample User Data:")
        print(f"   Age: {user_data['age']}")
        print(f"   Monthly Income: ${user_data['monthly_income']:,.0f}")
        print(f"   Credit Score: {credit_score}")
        print(f"   Financial Score: {factor_scores['financial']}/100")
        
        # Test synthetic profile generation
        print("\n🎲 Testing Synthetic Profile Generation...")
        try:
            profile = openai_service.generate_synthetic_user_profile()
            print(f"✅ Generated synthetic profile with {len(profile)} fields")
            print(f"   Age: {profile.get('age', 'N/A')}")
            print(f"   Income: ${profile.get('monthly_income', 0):,.0f}")
        except Exception as e:
            print(f"⚠️  Synthetic profile generation failed: {e}")
        
        # Test scenario analysis
        print("\n🔮 Testing Scenario Analysis...")
        try:
            current_data = {
                'credit_score': credit_score,
                'financial_score': factor_scores['financial'],
                'career_score': factor_scores['career'],
                'monthly_income': user_data['monthly_income'],
                'monthly_expenses': user_data['monthly_expenses']
            }
            
            scenario = "What if I get a 20% salary increase?"
            analysis = openai_service.generate_scenario_analysis(scenario, current_data)
            print(f"✅ Scenario analysis completed")
            print(f"   Impact: {analysis.get('impact_score', 'unknown')}")
            print(f"   Score Change: {analysis.get('estimated_score_change', 0)}")
        except Exception as e:
            print(f"⚠️  Scenario analysis failed: {e}")
        
        print("\n🎯 OpenAI Integration Test Complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_ai_features_endpoints():
    """Test the AI features API endpoints"""
    print("\n🌐 Testing AI Features API Endpoints...")
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:8000"
        
        # Test AI status endpoint
        print("   Testing /api/v1/ai/ai-status...")
        try:
            response = requests.get(f"{base_url}/api/v1/ai/ai-status")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ OpenAI Available: {data.get('openai_available', False)}")
                print(f"   🤖 Model: {data.get('model', 'N/A')}")
            else:
                print(f"   ❌ Status check failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("   ⚠️  Backend not running. Start with: python -m uvicorn backend.main:app --reload")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test synthetic profile generation endpoint
        print("   Testing /api/v1/ai/generate-synthetic-profile...")
        try:
            response = requests.post(f"{base_url}/api/v1/ai/generate-synthetic-profile")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Profile generated: {data.get('ai_generated', False)}")
                profile = data.get('profile', {})
                print(f"   📊 Age: {profile.get('age', 'N/A')}, Income: ${profile.get('monthly_income', 0):,.0f}")
            else:
                print(f"   ❌ Profile generation failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("   ⚠️  Backend not running")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
    except ImportError:
        print("   ⚠️  Requests library not available. Install with: pip install requests")

def main():
    """Main test function"""
    print("🚀 AI Credit Assessment Platform - OpenAI Integration Test")
    print("=" * 60)
    
    # Test OpenAI service
    test_openai_service()
    
    # Test API endpoints
    test_ai_features_endpoints()
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("1. Set your OpenAI API key in .env file")
    print("2. Start the backend: python -m uvicorn backend.main:app --reload")
    print("3. Test the API endpoints at http://localhost:8000/docs")
    print("4. Check the OPENAI_INTEGRATION_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()
