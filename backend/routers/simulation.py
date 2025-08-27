from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from ..database import get_db
from ..schemas.credit_schemas import SimulationRequest, SimulationResponse
from ..services.ai_models import CreditScoringModel
from ..models import credit_models, user_models
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

# Initialize AI model
credit_model = CreditScoringModel()

@router.post("/scenario", response_model=SimulationResponse)
async def run_simulation(
    request: SimulationRequest,
    db: Session = Depends(get_db)
):
    """Run a scenario simulation for a user"""
    try:
        logger.info(f"Starting simulation for user {request.user_id}, scenario: {request.scenario_type}")
        
        # Get user profile
        user_profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == request.user_id
        ).first()
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        # Get user's credit history
        credit_history = db.query(credit_models.CreditHistory).filter(
            credit_models.CreditHistory.user_id == request.user_id
        ).first()
        
        # Get current assessment
        current_assessment = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == request.user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).first()
        
        if not current_assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit assessment found for user"
            )
        
        # Prepare base user data
        user_data = {
            'monthly_income': user_profile.monthly_income or 0,
            'monthly_expenses': user_profile.monthly_expenses or 0,
            'savings_balance': user_profile.savings_balance or 0,
            'investment_balance': user_profile.investment_balance or 0,
            'age': user_profile.age or 30,
            'education_level': 'bachelors',
            'job_title': user_profile.job_title or '',
            'industry': user_profile.industry or '',
            'years_experience': user_profile.years_experience or 0,
            'salary': user_profile.salary or 0,
            'employment_status': user_profile.employment_status or 'full_time',
            'housing_status': user_profile.housing_status or 'renting',
            'monthly_rent': user_profile.monthly_rent or 0,
            'mortgage_payment': user_profile.mortgage_payment or 0,
            'property_value': user_profile.property_value or 0,
            'job_stability_score': 0.7,
            'social_score': 0.6,
        }
        
        # Add credit history data
        if credit_history:
            user_data.update({
                'credit_card_balance': credit_history.credit_card_balance or 0,
                'credit_card_limit': credit_history.credit_card_limit or 1,
                'loan_balance': credit_history.loan_balance or 0,
                'late_payments': credit_history.late_payments or 0,
                'missed_payments': credit_history.missed_payments or 0,
            })
        else:
            user_data.update({
                'credit_card_balance': 0,
                'credit_card_limit': 5000,
                'loan_balance': 0,
                'late_payments': 0,
                'missed_payments': 0,
            })
        
        # Apply scenario modifications
        modified_data = user_data.copy()
        factor_changes = {}
        
        if request.scenario_type == "salary_increase":
            salary_increase = request.parameters.get('salary_increase', 0)
            modified_data['salary'] += salary_increase
            modified_data['monthly_income'] += salary_increase / 12
            factor_changes['salary'] = f"+${salary_increase:,.0f}"
            factor_changes['monthly_income'] = f"+${salary_increase/12:,.0f}"
            
        elif request.scenario_type == "job_change":
            new_salary = request.parameters.get('new_salary', user_data['salary'])
            new_industry = request.parameters.get('new_industry', user_data['industry'])
            modified_data['salary'] = new_salary
            modified_data['monthly_income'] = new_salary / 12
            modified_data['industry'] = new_industry
            factor_changes['salary'] = f"${new_salary:,.0f} (was ${user_data['salary']:,.0f})"
            factor_changes['industry'] = f"{new_industry} (was {user_data['industry']})"
            
        elif request.scenario_type == "house_purchase":
            property_value = request.parameters.get('property_value', 300000)
            down_payment = request.parameters.get('down_payment', 60000)
            mortgage_amount = property_value - down_payment
            monthly_payment = request.parameters.get('monthly_payment', 1500)
            
            modified_data['housing_status'] = 'mortgaged'
            modified_data['property_value'] = property_value
            modified_data['mortgage_payment'] = monthly_payment
            modified_data['savings_balance'] -= down_payment
            
            factor_changes['housing_status'] = "mortgaged (was renting)"
            factor_changes['property_value'] = f"${property_value:,.0f}"
            factor_changes['monthly_expenses'] = f"+${monthly_payment:,.0f} mortgage"
            factor_changes['savings_balance'] = f"-${down_payment:,.0f} down payment"
            
        elif request.scenario_type == "debt_reduction":
            debt_reduction = request.parameters.get('debt_reduction', 0)
            modified_data['credit_card_balance'] = max(0, user_data['credit_card_balance'] - debt_reduction)
            modified_data['savings_balance'] -= debt_reduction
            factor_changes['credit_card_balance'] = f"-${debt_reduction:,.0f}"
            factor_changes['savings_balance'] = f"-${debt_reduction:,.0f}"
            
        elif request.scenario_type == "expense_reduction":
            expense_reduction = request.parameters.get('expense_reduction', 0)
            modified_data['monthly_expenses'] = max(0, user_data['monthly_expenses'] - expense_reduction)
            factor_changes['monthly_expenses'] = f"-${expense_reduction:,.0f}"
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown scenario type: {request.scenario_type}"
            )
        
        # Get simulated prediction
        simulated_prediction = credit_model.predict_credit_score(modified_data)
        
        # Calculate score change
        original_score = current_assessment.credit_score
        simulated_score = simulated_prediction['credit_score']
        score_change = simulated_score - original_score
        
        # Generate recommendations based on simulation
        recommendations = []
        if score_change > 0:
            recommendations.append(f"This scenario would improve your credit score by {score_change:.0f} points")
        elif score_change < 0:
            recommendations.append(f"This scenario would decrease your credit score by {abs(score_change):.0f} points")
        else:
            recommendations.append("This scenario would have minimal impact on your credit score")
        
        # Add scenario-specific recommendations
        if request.scenario_type == "salary_increase":
            recommendations.append("Higher income typically improves creditworthiness and borrowing capacity")
        elif request.scenario_type == "house_purchase":
            if score_change > 0:
                recommendations.append("Homeownership can improve credit scores through consistent mortgage payments")
            else:
                recommendations.append("Consider the impact of additional debt on your overall financial health")
        elif request.scenario_type == "debt_reduction":
            recommendations.append("Reducing debt improves your debt-to-income ratio and credit utilization")
        
        # Save simulation to database
        simulation = credit_models.Simulation(
            user_id=request.user_id,
            scenario_type=request.scenario_type,
            parameters=request.parameters,
            original_score=original_score,
            simulated_score=simulated_score,
            score_change=score_change,
            factor_changes=factor_changes,
            recommendations=recommendations,
            model_version=credit_model.model_version
        )
        
        db.add(simulation)
        db.commit()
        db.refresh(simulation)
        
        logger.info(f"Simulation completed for user {request.user_id}")
        
        return SimulationResponse(
            id=simulation.id,
            user_id=simulation.user_id,
            scenario_type=simulation.scenario_type,
            parameters=simulation.parameters,
            original_score=simulation.original_score,
            simulated_score=simulation.simulated_score,
            score_change=simulation.score_change,
            factor_changes=simulation.factor_changes,
            recommendations=simulation.recommendations,
            created_at=simulation.created_at,
            model_version=simulation.model_version
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in simulation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running simulation: {str(e)}"
        )

@router.get("/history/{user_id}")
async def get_simulation_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get simulation history for a user"""
    try:
        simulations = db.query(credit_models.Simulation).filter(
            credit_models.Simulation.user_id == user_id
        ).order_by(credit_models.Simulation.created_at.desc()).all()
        
        return [
            {
                "id": sim.id,
                "scenario_type": sim.scenario_type,
                "parameters": sim.parameters,
                "original_score": sim.original_score,
                "simulated_score": sim.simulated_score,
                "score_change": sim.score_change,
                "factor_changes": sim.factor_changes,
                "recommendations": sim.recommendations,
                "created_at": sim.created_at
            }
            for sim in simulations
        ]
        
    except Exception as e:
        logger.error(f"Error getting simulation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving simulation history: {str(e)}"
        )
