from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from ..database import get_db
from ..models import credit_models, user_models
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/{user_id}")
async def get_recommendations(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for a user"""
    try:
        # Get user's latest assessment
        assessment = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).first()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit assessment found for user"
            )
        
        # Get user profile
        profile = db.query(user_models.UserProfile).filter(
            user_models.UserProfile.user_id == user_id
        ).first()
        
        # Generate comprehensive recommendations
        recommendations = {
            "credit_score": assessment.credit_score,
            "risk_category": assessment.risk_category,
            "priority_recommendations": [],
            "financial_recommendations": [],
            "career_recommendations": [],
            "housing_recommendations": [],
            "long_term_goals": [],
            "immediate_actions": []
        }
        
        # Priority recommendations based on risk category
        if assessment.risk_category in ["poor", "very_poor"]:
            recommendations["priority_recommendations"].extend([
                "Focus on reducing high-interest debt immediately",
                "Establish emergency savings fund",
                "Review and reduce monthly expenses",
                "Consider credit counseling services"
            ])
        elif assessment.risk_category == "fair":
            recommendations["priority_recommendations"].extend([
                "Improve credit utilization ratio",
                "Build consistent payment history",
                "Increase savings rate",
                "Monitor credit report regularly"
            ])
        else:
            recommendations["priority_recommendations"].extend([
                "Maintain current healthy financial habits",
                "Consider investment opportunities",
                "Explore premium credit products",
                "Plan for major purchases"
            ])
        
        # Financial recommendations
        if assessment.financial_score < 60:
            recommendations["financial_recommendations"].extend([
                "Create a detailed budget and track all expenses",
                "Set up automatic savings transfers",
                "Pay more than minimum on credit cards",
                "Consider debt consolidation options"
            ])
        
        if profile and profile.credit_card_balance and profile.credit_card_limit:
            utilization = profile.credit_card_balance / profile.credit_card_limit
            if utilization > 0.3:
                recommendations["financial_recommendations"].append(
                    f"Reduce credit card utilization from {utilization*100:.1f}% to below 30%"
                )
        
        # Career recommendations
        if assessment.career_score < 60:
            recommendations["career_recommendations"].extend([
                "Consider professional development opportunities",
                "Research salary benchmarks for your role",
                "Build industry-specific skills",
                "Network within your professional community"
            ])
        
        if profile and profile.years_experience and profile.years_experience < 3:
            recommendations["career_recommendations"].append(
                "Focus on building experience and expertise in your field"
            )
        
        # Housing recommendations
        if assessment.housing_score < 50:
            if profile and profile.housing_status == "renting":
                recommendations["housing_recommendations"].extend([
                    "Consider homeownership when financially ready",
                    "Build savings for down payment",
                    "Improve credit score to qualify for better mortgage rates"
                ])
            elif profile and profile.housing_status == "mortgaged":
                recommendations["housing_recommendations"].extend([
                    "Consider refinancing if rates are favorable",
                    "Make extra mortgage payments when possible",
                    "Maintain property value through regular maintenance"
                ])
        
        # Long-term goals
        recommendations["long_term_goals"] = [
            "Build 6-month emergency fund",
            "Achieve excellent credit score (750+)",
            "Diversify income sources",
            "Plan for retirement savings",
            "Consider investment portfolio"
        ]
        
        # Immediate actions
        recommendations["immediate_actions"] = [
            "Review current credit report",
            "Set up payment reminders",
            "Create monthly budget",
            "Automate bill payments",
            "Start emergency fund"
        ]
        
        # Add specific recommendations from assessment
        if assessment.recommendations:
            recommendations["specific_recommendations"] = assessment.recommendations
        
        # Add risk factors
        if assessment.risk_factors:
            recommendations["risk_factors"] = assessment.risk_factors
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

@router.get("/{user_id}/improvement-plan")
async def get_improvement_plan(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a detailed improvement plan for the user"""
    try:
        # Get user's latest assessment
        assessment = db.query(credit_models.CreditAssessment).filter(
            credit_models.CreditAssessment.user_id == user_id
        ).order_by(credit_models.CreditAssessment.assessment_date.desc()).first()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credit assessment found for user"
            )
        
        # Calculate potential improvements
        current_score = assessment.credit_score
        target_score = 750  # Excellent credit score target
        
        improvement_plan = {
            "current_score": current_score,
            "target_score": target_score,
            "points_needed": max(0, target_score - current_score),
            "timeline_months": 12,
            "monthly_goals": [],
            "quarterly_milestones": [],
            "success_metrics": {}
        }
        
        # Monthly goals
        points_per_month = improvement_plan["points_needed"] / 12
        
        for month in range(1, 13):
            target_monthly_score = current_score + (points_per_month * month)
            improvement_plan["monthly_goals"].append({
                "month": month,
                "target_score": min(target_score, target_monthly_score),
                "focus_areas": get_focus_areas_for_month(month, assessment)
            })
        
        # Quarterly milestones
        for quarter in range(1, 5):
            target_quarterly_score = current_score + (points_per_month * quarter * 3)
            improvement_plan["quarterly_milestones"].append({
                "quarter": quarter,
                "target_score": min(target_score, target_quarterly_score),
                "key_actions": get_quarterly_actions(quarter, assessment)
            })
        
        # Success metrics
        improvement_plan["success_metrics"] = {
            "credit_utilization_target": "Below 30%",
            "payment_history_target": "100% on-time payments",
            "savings_rate_target": "20% of income",
            "debt_to_income_target": "Below 36%"
        }
        
        return improvement_plan
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting improvement plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating improvement plan: {str(e)}"
        )

def get_focus_areas_for_month(month: int, assessment) -> List[str]:
    """Get focus areas for a specific month"""
    if month <= 3:
        return ["Payment history", "Credit utilization", "Emergency fund"]
    elif month <= 6:
        return ["Debt reduction", "Income increase", "Credit mix"]
    elif month <= 9:
        return ["Credit history length", "New credit applications", "Financial stability"]
    else:
        return ["Maintenance", "Optimization", "Long-term planning"]

def get_quarterly_actions(quarter: int, assessment) -> List[str]:
    """Get key actions for a specific quarter"""
    if quarter == 1:
        return [
            "Set up automatic payments",
            "Reduce credit card balances",
            "Create emergency fund"
        ]
    elif quarter == 2:
        return [
            "Apply for credit limit increases",
            "Diversify credit mix",
            "Increase income streams"
        ]
    elif quarter == 3:
        return [
            "Monitor credit report",
            "Optimize credit utilization",
            "Plan major purchases"
        ]
    else:
        return [
            "Maintain excellent habits",
            "Review and adjust goals",
            "Plan for next year"
        ]
