"""
Ollama LLM integration for AI-powered predictions
"""
import ollama
from typing import Dict, Optional
from datetime import datetime
import json

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
                              question: str, category: str) -> str:
        """
        Generate direct answer to specific question
        
        Args:
            birth_data: Birth details
            chart_analysis: Chart analysis
            transit_data: Transit data
            matched_rules: Relevant rules
            question: The specific question asked
            category: Category of question (marriage, career, etc.)
            
        Returns:
            Direct answer to the question
        """
        
        print(f"\n=== CUSTOM QUESTION DEBUG ===")
        print(f"Question: {question}")
        print(f"Category: {category}")
        print(f"Name: {birth_data.get('name')}")
        print(f"===========================\n")
        
        prompt = f"""You are an expert Vedic astrologer. Answer this specific question directly.

QUESTION: "{question}"

Person: {birth_data.get('name')}
Born: {birth_data.get('date_of_birth')} at {birth_data.get('time_of_birth')}
Place: {birth_data.get('place_of_birth')}

Key Planets:
{self.format_chart_data(chart_analysis)}

Authority Planet: {chart_analysis.get('authority_planet')}
Today's Date: {datetime.now().strftime('%B %d, %Y')}

Answer their question directly in 2-3 paragraphs. Provide specific timeframes. Start immediately with the answer - no introductions."""

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
                                    category: str) -> str:
        """
        Generate category-specific prediction
        
        Args:
            birth_data: Birth details
            chart_analysis: Chart analysis
            transit_data: Transit data
            matched_rules: Relevant rules
            category: Prediction category
            
        Returns:
            Category-focused prediction
        """
        category_focus = {
            'marriage': 'Marriage, Relationships, Spouse characteristics, Marriage timing',
            'career': 'Career path, Professional success, Job changes, Business prospects',
            'health': 'Health patterns, Medical issues, Vitality, Recovery periods',
            'parents': 'Father relationship, Mother relationship, Family dynamics',
            'children': 'Children prospects, Progeny timing, Parenting style',
            'wealth': 'Financial status, Wealth accumulation, Income sources, Investments'
        }
        
        focus = category_focus.get(category, 'General life predictions')
        
        prompt = f"""You are a Rajanadi Shastra expert providing focused predictions about {focus}.

### FOCUS AREA: {focus.upper()}

### BIRTH CHART:
**Name:** {birth_data.get('name')}
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

Keep response under 6 paragraphs. Be specific and actionable."""

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
        # If there's a custom question, answer it directly
        if custom_question and custom_question.strip():
            return self.generate_custom_answer(
                birth_data, chart_analysis, transit_data, 
                matched_rules, custom_question, category
            )
        
        # If it's a specific category, give category prediction
        if category and category != "general":
            return self.generate_category_prediction(
                birth_data, chart_analysis, transit_data,
                matched_rules, category
            )
        
        # Otherwise give general comprehensive prediction
        return self._generate_comprehensive_prediction(
            birth_data, chart_analysis, transit_data, matched_rules
        )
    
    def _generate_comprehensive_prediction(self, birth_data: Dict, 
                                          chart_analysis: Dict,
                                          transit_data: Dict, 
                                          matched_rules: str) -> str:
        """Generate comprehensive general prediction"""
        prompt = f"""You are a Rajanadi Shastra expert providing comprehensive life predictions.

### BIRTH CHART:
**Name:** {birth_data.get('name', 'Native')}
**Date of Birth:** {birth_data.get('date_of_birth')}

**Planetary Positions:**
{self.format_chart_data(chart_analysis)}

**Authority Planet:** {chart_analysis.get('authority_planet', 'Unknown')}
**Karakas:**
{self.format_karakas(chart_analysis.get('karakas', {}))}

### RAJANADI RULES:
{matched_rules}

### TASK:
Provide comprehensive predictions covering:
1. Authority Planet influence on life path
2. Career and profession
3. Marriage and relationships
4. Health patterns
5. Wealth and finances
6. Current transit impacts

Use Rajanadi rules. Be specific and actionable."""

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
