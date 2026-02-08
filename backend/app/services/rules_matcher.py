"""
Pattern Matching for RajaNadiRules.txt
Simple, fast in-memory keyword matching (NO vector embeddings needed!)
"""
from pathlib import Path
from typing import List, Dict
import re

class RulesMatcher:
    """Load and pattern-match rules from RajaNadiRules.txt"""
    
    def __init__(self, rules_path: str = None):
        """
        Initialize and load rules file into memory
        
        Args:
            rules_path: Path to RajaNadiRules.txt (defaults to knowledge_base/)
        """
        if rules_path is None:
            rules_path = Path(__file__).parent.parent.parent / "knowledge_base" / "RajaNadiRules.txt"
        else:
            rules_path = Path(rules_path)
        
        self.rules_text = rules_path.read_text(encoding='utf-8')
        self.lines = self.rules_text.split('\n')
    
    def find_relevant_rules(self, keywords: List[str], max_sections: int = 15) -> str:
        """
        Find rules using keyword matching
        
        Args:
            keywords: List of keywords to search for
                     e.g., ['retrograde', 'saturn', 'authority', 'transit']
            max_sections: Maximum number of rule sections to return
            
        Returns:
            Formatted text with matched rule sections
        """
        matched_sections = []
        
        for i, line in enumerate(self.lines):
            score = 0
            line_lower = line.lower()
            
            # Score by keyword matches
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in line_lower:
                    score += line_lower.count(keyword_lower) * 2  # Weight keyword matches
            
            if score > 0:
                # Get context: 5 lines before and 5 lines after
                start_idx = max(0, i - 5)
                end_idx = min(len(self.lines), i + 6)
                context_lines = self.lines[start_idx:end_idx]
                
                # Join and clean
                context = '\n'.join(context_lines).strip()
                
                matched_sections.append({
                    'content': context,
                    'score': score,
                    'line_num': i
                })
        
        # Sort by score
        matched_sections.sort(key=lambda x: x['score'], reverse=True)
        
        # Remove duplicate contexts (check line numbers)
        unique_sections = []
        used_line_ranges = set()
        
        for section in matched_sections:
            line_num = section['line_num']
            # Check if this line range overlaps with already used ranges
            overlap = False
            for used_start, used_end in used_line_ranges:
                if line_num >= used_start - 10 and line_num <= used_end + 10:
                    overlap = True
                    break
            
            if not overlap:
                unique_sections.append(section)
                used_line_ranges.add((line_num - 5, line_num + 5))
                
                if len(unique_sections) >= max_sections:
                    break
        
        # Format output
        result = '\n\n---\n\n'.join([s['content'] for s in unique_sections])
        return result if result else "No specific rules matched. Using general Rajanadi principles."
    
    def build_context_for_chart(self, chart_analysis: Dict) -> str:
        """
        Build relevant rules context based on chart analysis
        
        Args:
            chart_analysis: Analysis from RajanadiEngine
            
        Returns:
            Curated rule text to include in Ollama prompt
        """
        keywords = []
        
        # Authority planet
        if chart_analysis.get('authority_planet'):
            keywords.extend(['authority', chart_analysis['authority_planet'].lower()])
        
        # Retrograde planets
        if chart_analysis.get('retrogrades'):
            keywords.append('retrograde')
            keywords.append('vakram')
            for planet in chart_analysis['retrogrades']:
                keywords.append(planet.lower())
        
        # Edge planets
        if chart_analysis.get('edge_planets'):
            keywords.extend(['edge', 'degree', 'vilimbu'])
        
        # Add general keywords for conjunctions
        if chart_analysis.get('conjunctions'):
            keywords.extend(['conjunction', '5th', '7th', '9th', '3rd', '11th'])
        
        # Add planet names and their Rasis (signs)
        planets = chart_analysis.get('planets', {})
        for planet_name, planet_data in planets.items():
            if planet_name in ['Ascendant']:
                continue
            keywords.append(planet_name.lower())
            if 'rasi_name' in planet_data:
                keywords.append(planet_data['rasi_name'].lower())
        
        # Add Karaka-specific keywords
        karakas = chart_analysis.get('karakas', {})
        for karaka_planet, karaka_data in karakas.items():
            for signification in karaka_data.get('significations', []):
                keywords.append(signification.lower())
        
        # Transit keywords
        keywords.extend(['transit', 'saturn', 'jupiter', 'dasa', 'period'])
        
        # Remove duplicates
        keywords = list(set(keywords))
        
        # Get relevant rules
        relevant_rules = self.find_relevant_rules(keywords, max_sections=20)
        
        return relevant_rules

# Global instance
rules_matcher = RulesMatcher()
