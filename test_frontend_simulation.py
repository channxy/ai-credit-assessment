#!/usr/bin/env python3
"""
Test script to verify frontend simulation integration
"""

import requests
import json

def test_frontend_simulation():
    """Test the frontend simulation integration"""
    print("🧪 Testing Frontend Simulation Integration...")
    
    # Test 1: Check if frontend is running
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend is running")
        else:
            print("❌ Frontend is not running")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running. Start with: cd frontend && npm start")
        return
    
    # Test 2: Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend is not running")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Start with: python -m uvicorn backend.main:app --reload")
        return
    
    # Test 3: Test simulation API directly
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
            print("✅ Simulation API working!")
            print(f"   Original Score: {result['original_score']:.0f}")
            print(f"   Simulated Score: {result['simulated_score']:.0f}")
            print(f"   Score Change: {result['score_change']:.0f}")
            print(f"   Factor Changes: {result['factor_changes']}")
            print(f"   Recommendations: {len(result['recommendations'])} items")
        else:
            print(f"❌ Simulation API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error testing simulation API: {e}")
        return
    
    # Test 4: Test simulation history API
    try:
        response = requests.get("http://localhost:8000/api/v1/simulation/history/1")
        if response.status_code == 200:
            history = response.json()
            print(f"✅ Simulation history API working! Found {len(history)} simulations")
        else:
            print(f"❌ Simulation history API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing simulation history API: {e}")
    
    print("\n🎯 Frontend Simulation Test Complete!")
    print("📋 Next Steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Navigate to the Simulation page")
    print("3. Click 'Run Simulation' or 'Test Results' button")
    print("4. Check the browser console for any errors")
    print("5. Verify that simulation results are displayed")

if __name__ == "__main__":
    test_frontend_simulation()
