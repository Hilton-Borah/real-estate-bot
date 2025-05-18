from typing import List, Dict, Any, Optional
import pandas as pd
import re
from .excel_handler import ExcelHandler

class DataProcessor:
    def __init__(self, excel_handler: ExcelHandler):
        self.excel_handler = excel_handler
        
    def extract_areas_from_query(self, query: str) -> List[str]:
        """Extract area names from the query"""
        # Load all possible areas from the data
        all_areas = self.excel_handler.get_areas()
        
        # Search for mentioned areas in the query
        found_areas = []
        for area in all_areas:
            if area.lower() in query.lower():
                found_areas.append(area)
                
        return found_areas
    
    def extract_years_from_query(self, query: str) -> List[int]:
        """Extract years from the query"""
        # Match 4-digit numbers that could be years
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', query)
        
        # Look for patterns like "last 3 years"
        last_years_match = re.search(r'last\s+(\d+)\s+years', query, re.IGNORECASE)
        if last_years_match:
            from datetime import datetime
            current_year = datetime.now().year
            num_years = int(last_years_match.group(1))
            return list(range(current_year - num_years + 1, current_year + 1))
            
        return [int(year) for year in years]
    
    def identify_metrics_from_query(self, query: str) -> List[str]:
        """Identify metrics mentioned in the query"""
        metrics = []
        
        # Common real estate metrics
        possible_metrics = {
            'price': ['price', 'cost', 'value'],
            'demand': ['demand', 'popularity', 'interest'],
            'size': ['size', 'area', 'square', 'sq ft', 'sqft'],
        }
        
        # Check for each metric in the query
        for metric, keywords in possible_metrics.items():
            for keyword in keywords:
                if keyword in query.lower():
                    metrics.append(metric)
                    break
                    
        # If no specific metric found, default to price
        if not metrics:
            metrics.append('price')
            
        return metrics
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process the user query and return relevant data"""
        # Extract information from query
        areas = self.extract_areas_from_query(query)
        years = self.extract_years_from_query(query)
        metrics = self.identify_metrics_from_query(query)
        
        result = {
            'query': query,
            'areas': areas,
            'metrics': metrics,
            'chart_data': [],
            'table_data': [],
            'summary': ''
        }
        
        # If no areas found, return empty result
        if not areas:
            result['summary'] = "I couldn't identify any specific areas in your query. Please specify an area like 'Wakad' or 'Aundh'."
            return result
            
        # Check if it's a comparison query
        is_comparison = len(areas) > 1 or "compare" in query.lower()
        
        # Process based on query type
        if is_comparison:
            # Handle comparison query
            for metric in metrics:
                result['chart_data'] = self.excel_handler.compare_areas(areas, metric)
                
            # Get filtered data for each area
            table_data = []
            for area in areas:
                filtered_df = self.excel_handler.filter_by_area(area)
                if not filtered_df.empty:
                    table_data.extend(filtered_df.to_dict('records'))
            result['table_data'] = table_data
            
        else:
            # Handle single area query
            area = areas[0]
            
            # Check for growth rate query
            if "growth" in query.lower() or "trend" in query.lower():
                for metric in metrics:
                    result['chart_data'] = self.excel_handler.get_price_trend(area) if metric == 'price' else self.excel_handler.get_demand_trend(area)
                
                # Calculate growth rate if mentioned
                growth_years = 3  # Default to 3 years
                if years:
                    growth_years = len(years)
                
                for metric in metrics:
                    growth_rate = self.excel_handler.get_growth_rate(area, growth_years, metric)
                    if growth_rate is not None:
                        result[f'{metric}_growth'] = growth_rate
            
            else:
                # General area analysis
                for metric in metrics:
                    if metric == 'price':
                        result['chart_data'] = self.excel_handler.get_price_trend(area)
                    elif metric == 'demand':
                        result['chart_data'] = self.excel_handler.get_demand_trend(area)
            
            # Get filtered data for the area
            filtered_df = self.excel_handler.filter_by_area(area)
            if not filtered_df.empty:
                result['table_data'] = filtered_df.to_dict('records')
        
        return result