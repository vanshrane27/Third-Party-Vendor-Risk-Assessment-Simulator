from config import Config

class RiskScoring:
    @staticmethod
    def calculate_risk_score(responses):
        """
        Calculate total risk score based on assessment responses.
        
        Args:
            responses (dict): Dictionary of question IDs and their responses
            
        Returns:
            tuple: (total_score, risk_classification)
        """
        total_score = 0
        
        for question_id, response in responses.items():
            # Get question details from the response
            question_data = response.get('question_data', {})
            control_weight = question_data.get('weight', 'medium')
            
            # Calculate score based on response
            if response.get('answer') == 'No':
                score = Config.CONTROL_WEIGHTS.get(control_weight, 5)
                total_score += score
        
        # Determine risk classification
        risk_classification = RiskScoring.classify_risk(total_score)
        
        return total_score, risk_classification
    
    @staticmethod
    def classify_risk(score):
        """
        Classify risk based on total score.
        
        Args:
            score (int): Total risk score
            
        Returns:
            str: Risk classification (low, medium, high)
        """
        if score <= Config.RISK_THRESHOLDS['low']:
            return 'Low Risk'
        elif score <= Config.RISK_THRESHOLDS['medium']:
            return 'Medium Risk'
        else:
            return 'High Risk'
    
    @staticmethod
    def get_improvement_suggestions(responses):
        """
        Generate improvement suggestions based on failed controls.
        
        Args:
            responses (dict): Dictionary of question IDs and their responses
            
        Returns:
            list: List of improvement suggestions
        """
        suggestions = []
        
        for question_id, response in responses.items():
            if response.get('answer') == 'No':
                question_data = response.get('question_data', {})
                suggestion = {
                    'control': question_data.get('control_id', 'Unknown'),
                    'description': question_data.get('description', ''),
                    'suggestion': question_data.get('improvement_suggestion', 'Implement the required control.')
                }
                suggestions.append(suggestion)
        
        return suggestions 