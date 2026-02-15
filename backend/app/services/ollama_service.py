"""
Ollama LLM integration for AI-powered predictions
"""
import ollama
from typing import Dict, Optional
from datetime import datetime, date
import json
from app.utils.age_utils import (
    calculate_age,
    is_category_allowed,
    get_age_appropriate_message,
    get_age_context_for_prompt,
    filter_prediction_topics
)

class OllamaService:
    """Generate predictions using Ollama LLM"""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama service
        
        Args:
            model: Ollama model name (default: llama3)
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
    
    def format_chart_data(self, chart_analysis: Dict) -> str:
        """Format chart data for the prompt"""
        planets_str = ""
        for planet, data in chart_analysis.get('planets', {}).items():
            retro = " (R)" if data.get('is_retrograde') else ""
            planets_str += f"- **{planet}**: {data['rasi_name']} {data['degree']:.1f}°{retro}\n"
        
        return planets_str
    
    def format_karakas(self, karakas: Dict) -> str:
        """Format Karaka information"""
        karaka_str = ""
        for planet, data in karakas.items():
            karaka_str += f"- **{planet}** ({', '.join(data['significations'])}): "
            karaka_str += f"{data['rasi_name']} {data['degree']:.1f}°"
            if data['is_retrograde']:
                karaka_str += " (Retrograde)"
            karaka_str += "\n"
        
        return karaka_str
    
    def generate_custom_answer(self, birth_data: Dict, chart_analysis: Dict, 
                              transit_data: Dict, matched_rules: str, 
                              question: str, category: str, age: Optional[int] = None) -> str:
        """
        Generate direct answer to specific question
        
        Args:
            birth_data: Birth details
            chart_analysis: Chart analysis
            transit_data: Transit data
            matched_rules: Relevant rules
            question: The specific question asked
            category: Category of question (marriage, career, etc.)
            age: Current age of the person (optional)
            
        Returns:
            Direct answer to the question
        """
        
        print(f"\n=== CUSTOM QUESTION DEBUG ===")
        print(f"Question: {question}")
        print(f"Category: {category}")
        print(f"Name: {birth_data.get('name')}")
        print(f"Age: {age}")
        print(f"===========================\n")
        
        # Add age context if available
        age_context = ""
        if age is not None:
            age_context = f"\n\nIMPORTANT AGE CONTEXT:\n{get_age_context_for_prompt(age, birth_data.get('name', 'Native'))}\n"
        
        prompt = f"""You are an expert Vedic astrologer. Answer this specific question directly.

QUESTION: "{question}"

Person: {birth_data.get('name')}
Born: {birth_data.get('date_of_birth')} at {birth_data.get('time_of_birth')}
Place: {birth_data.get('place_of_birth')}
{age_context}
Key Planets:
{self.format_chart_data(chart_analysis)}

Authority Planet: {chart_analysis.get('authority_planet')}
Today's Date: {datetime.now().strftime('%B %d, %Y')}

Answer their question directly in 2-3 paragraphs. Provide specific timeframes when relevant. Ensure your answer is appropriate for their age. Start immediately with the answer - no introductions."""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.6,
                    'top_p': 0.85,
                    'max_tokens': 600
                }
            )
            
            return response['response']
        
        except Exception as e:
            error_msg = f"Error connecting to Ollama: {str(e)}\n\n"
            error_msg += "Please ensure Ollama is running (ollama serve) and the llama3 model is installed (ollama pull llama3)."
            return error_msg
    
    def generate_category_prediction(self, birth_data: Dict, chart_analysis: Dict, 
                                    transit_data: Dict, matched_rules: str, 
                                    category: str, age: Optional[int] = None) -> str:
        """
        Generate category-specific prediction
        
        Args:
            birth_data: Birth details
            chart_analysis: Chart analysis
            transit_data: Transit data
            matched_rules: Relevant rules
            category: Prediction category
            age: Current age of the person (optional)
            
        Returns:
            Category-focused prediction
        """
        category_focus = {
            'marriage': 'Marriage, Relationships, Spouse characteristics, Marriage timing',
            'career': 'Career path, Professional success, Job changes, Business prospects',
            'health': 'Health patterns, Medical issues, Vitality, Recovery periods',
            'parents': 'Father relationship, Mother relationship, Family dynamics',
            'children': 'Children prospects, Progeny timing, Parenting style',
            'wealth': 'Financial status, Wealth accumulation, Income sources, Investments',
            'education': 'Education, Learning abilities, Academic success, Suitable fields of study'
        }
        
        focus = category_focus.get(category, 'General life predictions')
        
        # Add age context if available
        age_context = ""
        if age is not None:
            age_context = f"\n\n### AGE CONTEXT:\n{get_age_context_for_prompt(age, birth_data.get('name', 'Native'))}\n"
        
        prompt = f"""You are a Rajanadi Shastra expert providing focused predictions about {focus}.

### FOCUS AREA: {focus.upper()}

### BIRTH CHART:
**Name:** {birth_data.get('name')}
**Date of Birth:** {birth_data.get('date_of_birth')}
{age_context}
**Planetary Positions:**
{self.format_chart_data(chart_analysis)}
**Authority Planet:** {chart_analysis.get('authority_planet')}

### RAJANADI RULES:
{matched_rules}

### TASK:
Provide a focused prediction ONLY about {focus}. Structure your answer:

1. **Current Situation**: What's happening now in this area
2. **Planetary Influences**: Which planets affect this area and how
3. **Timing**: When will key events occur (use current transits - it's {datetime.now().strftime('%B %Y')})
4. **Recommendations**: Specific actions to take

Ensure your predictions are appropriate for the person's age and life stage. Keep response under 6 paragraphs. Be specific and actionable."""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.65,
                    'top_p': 0.9,
                    'max_tokens': 1000
                }
            )
            
            return response['response']
        
        except Exception as e:
            error_msg = f"Error connecting to Ollama: {str(e)}\n\n"
            error_msg += "Please ensure Ollama is running."
            return error_msg
    
    def generate_prediction(self, birth_data: Dict, chart_analysis: Dict, 
                          transit_data: Dict, matched_rules: str,
                          category: str = "general", 
                          custom_question: Optional[str] = None) -> str:
        """
        Generate prediction - routes to appropriate method based on type
        
        Args:
            birth_data: Birth details
            chart_analysis: Chart analysis
            transit_data: Transit data
            matched_rules: Relevant rules
            category: Type of prediction
            custom_question: Optional custom question
            
        Returns:
            AI-generated prediction
        """
        # Calculate person's age
        age = None
        date_of_birth_str = birth_data.get('date_of_birth')
        
        if date_of_birth_str:
            try:
                # Parse date of birth (could be string or date object)
                if isinstance(date_of_birth_str, str):
                    dob = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
                elif isinstance(date_of_birth_str, date):
                    dob = date_of_birth_str
                else:
                    dob = None
                
                if dob:
                    age = calculate_age(dob)
                    print(f"\n=== AGE CALCULATION ===")
                    print(f"Name: {birth_data.get('name')}")
                    print(f"Date of Birth: {dob}")
                    print(f"Current Age: {age} years")
                    print(f"Category: {category}")
                    print(f"======================\n")
            except Exception as e:
                print(f"Error calculating age: {e}")
                age = None
        
        # Check if category is age-appropriate
        if age is not None and category != "general":
            if not is_category_allowed(category, age):
                inappropriate_msg = get_age_appropriate_message(category, age)
                return f"⚠️ **Age-Inappropriate Request**\n\n{inappropriate_msg}\n\nPlease choose a more relevant category for predictions, or use 'general' for an overall reading appropriate to this age."
        
        # If there's a custom question, answer it directly
        if custom_question and custom_question.strip():
            return self.generate_custom_answer(
                birth_data, chart_analysis, transit_data, 
                matched_rules, custom_question, category, age
            )
        
        # If it's a specific category, give category prediction
        if category and category != "general":
            return self.generate_category_prediction(
                birth_data, chart_analysis, transit_data,
                matched_rules, category, age
            )
        
        # Otherwise give general comprehensive prediction
        return self._generate_comprehensive_prediction(
            birth_data, chart_analysis, transit_data, matched_rules, age
        )
    
    def _generate_comprehensive_prediction(self, birth_data: Dict, 
                                          chart_analysis: Dict,
                                          transit_data: Dict, 
                                          matched_rules: str,
                                          age: Optional[int] = None) -> str:
        """Generate comprehensive general prediction"""
        
        # Get age-appropriate topics
        topics = None
        age_context = ""
        if age is not None:
            topics = filter_prediction_topics(age)
            age_context = f"\n\n### AGE CONTEXT:\n{get_age_context_for_prompt(age, birth_data.get('name', 'Native'))}\n"
            topics_str = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(topics)])
        else:
            topics_str = """1. Authority Planet influence on life path
2. Career and profession
3. Marriage and relationships
4. Health patterns
5. Wealth and finances
6. Current transit impacts"""
        
        prompt = f"""You are a Rajanadi Shastra expert providing comprehensive life predictions.

### BIRTH CHART:
**Name:** {birth_data.get('name', 'Native')}
**Date of Birth:** {birth_data.get('date_of_birth')}
{age_context}
**Planetary Positions:**
{self.format_chart_data(chart_analysis)}

**Authority Planet:** {chart_analysis.get('authority_planet', 'Unknown')}
**Karakas:**
{self.format_karakas(chart_analysis.get('karakas', {}))}

### RAJANADI RULES:
{matched_rules}

### TASK:
Provide comprehensive predictions covering these topics (appropriate for the person's age):
{topics_str}

Use Rajanadi rules. Be specific and actionable. Ensure all predictions are age-appropriate and relevant to their current life stage."""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 2000
                }
            )
            
            return response['response']
        
        except Exception as e:
            return f"Error: {str(e)}"

# Global instance
ollama_service = OllamaService()
