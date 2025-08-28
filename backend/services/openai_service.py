import openai
import os
import json
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = None
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            try:
                self.client = openai.OpenAI(
                    api_key=api_key,
                    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
                )
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        
    def generate_credit_explanation(self, user_data: Dict[str, Any], credit_score: float, factor_scores: Dict[str, float]) -> str:
        """Generate a natural language explanation of the credit score"""
        try:
            prompt = f"""
            You are a financial advisor explaining a credit assessment. Please provide a clear, friendly explanation of this credit score.

            User Profile:
            - Age: {user_data.get('age', 'N/A')}
            - Monthly Income: ${user_data.get('monthly_income', 0):,.0f}
            - Monthly Expenses: ${user_data.get('monthly_expenses', 0):,.0f}
            - Housing Status: {user_data.get('housing_status', 'N/A')}
            - Years of Experience: {user_data.get('years_experience', 0)}
            - Education: {user_data.get('education_level', 'N/A')}

            Credit Assessment Results:
            - Overall Credit Score: {credit_score:.0f}
            - Financial Score: {factor_scores.get('financial', 0):.0f}/100
            - Career Score: {factor_scores.get('career', 0):.0f}/100
            - Housing Score: {factor_scores.get('housing', 0):.0f}/100
            - Social Score: {factor_scores.get('social', 0):.0f}/100

            Please provide a 2-3 paragraph explanation that:
            1. Explains what the credit score means
            2. Highlights the strongest and weakest areas
            3. Uses a friendly, encouraging tone
            4. Avoids financial jargon
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful financial advisor who explains credit scores in simple, friendly terms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating credit explanation: {e}")
            return "We've calculated your credit score based on multiple factors including your financial health, career stability, housing situation, and social indicators."

    def generate_personalized_recommendations(self, user_data: Dict[str, Any], factor_scores: Dict[str, float], risk_factors: List[str]) -> List[str]:
        """Generate personalized recommendations using OpenAI"""
        try:
            prompt = f"""
            As a financial advisor, provide 3-5 specific, actionable recommendations to improve this person's credit score.

            User Profile:
            - Age: {user_data.get('age', 'N/A')}
            - Monthly Income: ${user_data.get('monthly_income', 0):,.0f}
            - Monthly Expenses: ${user_data.get('monthly_expenses', 0):,.0f}
            - Credit Card Balance: ${user_data.get('credit_card_balance', 0):,.0f}
            - Credit Card Limit: ${user_data.get('credit_card_limit', 1):,.0f}
            - Savings Balance: ${user_data.get('savings_balance', 0):,.0f}
            - Housing Status: {user_data.get('housing_status', 'N/A')}
            - Years of Experience: {user_data.get('years_experience', 0)}

            Current Scores:
            - Financial: {factor_scores.get('financial', 0):.0f}/100
            - Career: {factor_scores.get('career', 0):.0f}/100
            - Housing: {factor_scores.get('housing', 0):.0f}/100
            - Social: {factor_scores.get('social', 0):.0f}/100

            Risk Factors: {', '.join(risk_factors) if risk_factors else 'None identified'}

            Provide specific, actionable recommendations that are:
            1. Realistic for their financial situation
            2. Prioritized by impact
            3. Include specific amounts or percentages where relevant
            4. Written in a supportive, encouraging tone

            Format as a numbered list.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial advisor providing personalized credit improvement recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            # Parse numbered list into individual recommendations
            recommendations = [line.strip() for line in content.split('\n') if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))]
            
            return recommendations[:5]  # Limit to 5 recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return [
                "Consider reducing your monthly expenses to improve your financial score",
                "Focus on building emergency savings",
                "Reduce credit card utilization to below 30%"
            ]

    def generate_risk_analysis(self, user_data: Dict[str, Any], factor_scores: Dict[str, float]) -> str:
        """Generate detailed risk analysis using OpenAI"""
        try:
            prompt = f"""
            Analyze the credit risk profile for this individual and provide a concise risk assessment.

            Financial Profile:
            - Income: ${user_data.get('monthly_income', 0):,.0f}/month
            - Expenses: ${user_data.get('monthly_expenses', 0):,.0f}/month
            - Credit Utilization: {(user_data.get('credit_card_balance', 0) / (user_data.get('credit_card_limit', 1) + 1)) * 100:.1f}%
            - Late Payments: {user_data.get('late_payments', 0)}
            - Missed Payments: {user_data.get('missed_payments', 0)}

            Factor Scores:
            - Financial: {factor_scores.get('financial', 0):.0f}/100
            - Career: {factor_scores.get('career', 0):.0f}/100
            - Housing: {factor_scores.get('housing', 0):.0f}/100
            - Social: {factor_scores.get('social', 0):.0f}/100

            Provide a 2-3 sentence risk assessment that:
            1. Identifies the primary risk factors
            2. Assesses overall risk level (Low/Medium/High)
            3. Mentions any positive factors that mitigate risk
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a credit risk analyst providing concise risk assessments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating risk analysis: {e}")
            return "Risk assessment based on financial behavior, career stability, and credit history."

    def generate_synthetic_user_profile(self) -> Dict[str, Any]:
        """Generate a realistic synthetic user profile for testing"""
        try:
            prompt = """
            Generate a realistic user profile for credit assessment testing. Return only a JSON object with the following structure:
            {
                "age": 25-65,
                "monthly_income": 2000-15000,
                "monthly_expenses": 1000-8000,
                "savings_balance": 0-50000,
                "credit_card_balance": 0-10000,
                "credit_card_limit": 1000-20000,
                "loan_balance": 0-100000,
                "late_payments": 0-5,
                "missed_payments": 0-3,
                "years_experience": 0-30,
                "salary": 25000-200000,
                "job_stability_score": 0.1-1.0,
                "housing_status": "renting|owned|mortgaged",
                "monthly_rent": 500-3000,
                "mortgage_payment": 0-4000,
                "property_value": 0-1000000,
                "education_level": "high_school|bachelors|masters|phd",
                "social_score": 0.1-1.0
            }
            
            Make the profile realistic and internally consistent.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data generator creating realistic user profiles for financial testing."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error generating synthetic profile: {e}")
            # Fallback to default profile
            return {
                "age": 35,
                "monthly_income": 5000,
                "monthly_expenses": 3000,
                "savings_balance": 10000,
                "credit_card_balance": 2000,
                "credit_card_limit": 8000,
                "loan_balance": 15000,
                "late_payments": 1,
                "missed_payments": 0,
                "years_experience": 8,
                "salary": 60000,
                "job_stability_score": 0.7,
                "housing_status": "renting",
                "monthly_rent": 1500,
                "mortgage_payment": 0,
                "property_value": 0,
                "education_level": "bachelors",
                "social_score": 0.6
            }

    def generate_scenario_analysis(self, scenario: str, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis for 'what-if' scenarios"""
        try:
            prompt = f"""
            Analyze how this scenario would impact the user's credit score and provide insights.

            Current Profile:
            - Monthly Income: ${current_data.get('monthly_income', 0):,.0f}
            - Credit Score: {current_data.get('credit_score', 0):.0f}
            - Financial Score: {current_data.get('financial_score', 0):.0f}/100
            - Career Score: {current_data.get('career_score', 0):.0f}/100

            Scenario: {scenario}

            Provide analysis in JSON format:
            {{
                "impact_score": "positive|negative|neutral",
                "estimated_score_change": -50 to +50,
                "reasoning": "explanation of impact",
                "recommendations": ["action1", "action2"],
                "timeline": "short-term|medium-term|long-term"
            }}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst evaluating scenario impacts on credit scores."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            
            content = response.choices[0].message.content.strip()
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            return json.loads(json_str)
            
        except Exception as e:
            logger.error(f"Error generating scenario analysis: {e}")
            return {
                "impact_score": "neutral",
                "estimated_score_change": 0,
                "reasoning": "Unable to analyze scenario at this time",
                "recommendations": ["Consult with a financial advisor"],
                "timeline": "short-term"
            }

    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            return bool(api_key and api_key != "your_openai_api_key_here" and self.client is not None)
        except:
            return False
