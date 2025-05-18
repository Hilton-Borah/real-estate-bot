# import requests
# import json
# import os
# from django.conf import settings
# from typing import Dict, Any, Optional

# class LLMService:
#     def __init__(self, api_key: Optional[str] = None):
#         self.api_key = api_key or settings.HUGGINGFACE_API_KEY
#         self.api_url = settings.HUGGINGFACE_API_URL
        
#     def generate_summary(self, data: Dict[str, Any]) -> str:
#         """Generate a summary using an LLM (Hugging Face API)"""
#         # If no API key is provided, use a mock summary
#         if not self.api_key:
#             return self._generate_mock_summary(data)
            
#         # Prepare data for the LLM
#         prompt = self._prepare_prompt(data)
        
#         # Call the Hugging Face API
#         try:
#             headers = {
#                 "Authorization": f"Bearer {self.api_key}",
#                 "Content-Type": "application/json"
#             }
            
#             payload = {
#                 "inputs": prompt,
#                 "parameters": {
#                     "max_length": 200,
#                     "temperature": 0.7,
#                     "top_p": 0.9,
#                     "return_full_text": False
#                 }
#             }
            
#             response = requests.post(self.api_url, headers=headers, json=payload)
            
#             if response.status_code == 200:
#                 result = response.json()
#                 if isinstance(result, list) and len(result) > 0:
#                     generated_text = result[0].get("generated_text", "")
#                     return generated_text
                    
#             # Fallback to mock summary if API call fails
#             return self._generate_mock_summary(data)
            
#         except Exception as e:
#             print(f"Error calling Hugging Face API: {e}")
#             return self._generate_mock_summary(data)
    
#     def _prepare_prompt(self, data: Dict[str, Any]) -> str:
#         """Prepare a prompt for the LLM based on the data"""
#         query = data.get('query', '')
#         areas = data.get('areas', [])
#         metrics = data.get('metrics', [])
        
#         prompt = f"Generate a concise real estate market analysis summary for the following information:\n"
#         prompt += f"Query: {query}\n"
        
#         if areas:
#             prompt += f"Areas: {', '.join(areas)}\n"
            
#         if metrics:
#             prompt += f"Metrics: {', '.join(metrics)}\n"
            
#         if 'price_growth' in data:
#             prompt += f"Price growth rate: {data['price_growth']:.2f}%\n"
            
#         if 'demand_growth' in data:
#             prompt += f"Demand growth rate: {data['demand_growth']:.2f}%\n"
            
#         prompt += "\nSummary:"
        
#         return prompt
    
#     def _generate_mock_summary(self, data: Dict[str, Any]) -> str:
#         """Generate a mock summary when API key is not available"""
#         areas = data.get('areas', [])
#         metrics = data.get('metrics', [])
        
#         if not areas:
#             return "No specific area was identified in your query. Please specify an area for analysis."
            
#         # Single area analysis
#         if len(areas) == 1:
#             area = areas[0]
            
#             if 'price' in metrics and 'price_growth' in data:
#                 growth = data['price_growth']
#                 if growth > 0:
#                     return f"The real estate market in {area} has shown positive growth with prices increasing by approximately {growth:.2f}% over the analyzed period. The area demonstrates good investment potential with consistent demand patterns."
#                 else:
#                     return f"The real estate market in {area} has experienced a slight decline with prices decreasing by approximately {abs(growth):.2f}% over the analyzed period. This might present buying opportunities for long-term investors."
                    
#             if 'demand' in metrics and 'demand_growth' in data:
#                 growth = data['demand_growth']
#                 if growth > 0:
#                     return f"The demand for properties in {area} has increased by approximately {growth:.2f}% over the analyzed period. This increasing interest suggests the area is becoming more desirable for residents and investors alike."
#                 else:
#                     return f"The demand for properties in {area} has decreased by approximately {abs(growth):.2f}% over the analyzed period. This might indicate shifting preferences or new developments in nearby areas attracting potential buyers."
                    
#             # Default single area summary
#             return f"Based on the available data, {area} shows typical market patterns for the region. Property values have remained relatively stable with seasonal fluctuations. Consider long-term investment strategies if looking at this area."
            
#         # Comparison between areas
#         else:
#             areas_str = " and ".join(areas) if len(areas) == 2 else ", ".join(areas[:-1]) + ", and " + areas[-1]
            
#             # Default comparison summary
#             if 'price' in metrics:
#                 return f"Comparing {areas_str}, the data reveals distinct price patterns. Each area has its own market dynamics, with varying growth rates and investment potential. Further analysis of specific timeframes would provide more targeted insights for investment decisions."
                
#             if 'demand' in metrics:
#                 return f"The demand trends across {areas_str} show interesting variations. Market interest fluctuates across these areas, likely influenced by infrastructure development, amenities, and connectivity factors. A deeper timeframe analysis would reveal which area has more sustainable demand growth."
                
#             return f"Comparing real estate metrics across {areas_str} reveals unique market characteristics for each location. Consider factors like infrastructure development, connectivity, and local amenities when evaluating these areas for investment or residence."




import google.generativeai as genai
import pandas as pd
from django.conf import settings
import logging
import json
import plotly.express as px
import plotly.utils
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GOOGLE_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.data = None
        
    def load_data(self, file_path: str) -> bool:
        """Load and preprocess the Excel data"""
        try:
            self.data = pd.read_excel(file_path)
            self.data = self.data.fillna(0)
            return True
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            self.data = None
            return False
    
    def generate_response(self, query: str) -> dict:
        """Generate a comprehensive response using Google's Generative AI"""
        if self.data is None or self.data.empty:
            return {"error": "Data not loaded or empty"}
            
        try:
            # Filter data based on query
            filtered_data = self._filter_data(query)
            
            # Generate components
            summary = self._generate_summary(query, filtered_data)
            chart_data = self._prepare_chart_data(filtered_data, query)
            table_data = filtered_data.to_dict(orient='records')
            
            response = {
                "summary": summary,
                "chart_data": chart_data,
                "table_data": table_data
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"error": f"Error processing query: {str(e)}"}
    
    def _filter_data(self, query: str) -> pd.DataFrame:
        """Filter data based on query"""
        filtered = self.data.copy()
        
        # Extract locations from query
        locations = [loc for loc in self.data['final location'].unique() 
                   if loc.lower() in query.lower()]
        
        if locations:
            filtered = filtered[filtered['final location'].isin(locations)]
        
        # Handle time-based queries
        if "last" in query.lower() and "year" in query.lower():
            try:
                num_years = int(''.join(filter(str.isdigit, query.split("last")[1].split("year")[0])))
                latest_year = filtered['year'].max()
                filtered = filtered[filtered['year'] > (latest_year - num_years)]
            except:
                pass
                
        return filtered
    
    def _generate_summary(self, query: str, data: pd.DataFrame) -> str:
        """Generate summary using Google's Generative AI"""
        try:
            # Prepare the prompt
            prompt = self._prepare_prompt(query, data)
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            
            return self._generate_mock_summary(query, data)
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return self._generate_mock_summary(query, data)
    
    def _prepare_prompt(self, query: str, data: pd.DataFrame) -> str:
        """Create a detailed prompt for analysis"""
        # Calculate key metrics
        metrics = {
            'locations': data['final location'].unique().tolist(),
            'years': sorted(data['year'].unique().tolist()),
            'avg_price': data['flat - weighted average rate'].mean(),
            'total_sales': data['total_sales - igr'].sum(),
            'units_sold': data['total sold - igr'].sum()
        }
        
        # Calculate price trends
        price_trends = {}
        for loc in metrics['locations']:
            loc_data = data[data['final location'] == loc]
            if not loc_data.empty:
                earliest = loc_data.groupby('year')['flat - weighted average rate'].mean().iloc[0]
                latest = loc_data.groupby('year')['flat - weighted average rate'].mean().iloc[-1]
                growth = ((latest - earliest) / earliest * 100) if earliest != 0 else 0
                price_trends[loc] = growth
        
        prompt = f"""As a real estate market analyst, analyze this data based on the query: "{query}"

Data Summary:
- Locations analyzed: {', '.join(metrics['locations'])}
- Time period: {min(metrics['years'])} to {max(metrics['years'])}
- Average property price: ₹{metrics['avg_price']:,.2f}
- Total sales value: ₹{metrics['total_sales']:,.2f}
- Total units sold: {metrics['units_sold']:,}

Price Growth Trends:
{chr(10).join([f'- {loc}: {growth:.1f}% growth' for loc, growth in price_trends.items()])}

Please provide a comprehensive analysis including:
1. Key market trends and patterns
2. Comparison between locations (if multiple)
3. Price movement analysis
4. Investment potential and recommendations
5. Notable market dynamics

Keep the analysis concise but informative, focusing on the most relevant insights for the query."""
        
        return prompt
    
    def _prepare_chart_data(self, data: pd.DataFrame, query: str) -> Dict[str, Any]:
        """Prepare chart data based on the query and filtered data"""
        chart_data = {}
        
        try:
            # Price trends over time
            price_trends = data.groupby(['year', 'final location'])['flat - weighted average rate'].mean().reset_index()
            fig_price = px.line(price_trends, 
                              x='year', 
                              y='flat - weighted average rate',
                              color='final location',
                              title='Property Price Trends',
                              labels={'flat - weighted average rate': 'Average Price (₹)',
                                     'year': 'Year',
                                     'final location': 'Location'})
            chart_data['price_trends'] = json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig_price))
            
            # Demand trends (using total sold units)
            demand_trends = data.groupby(['year', 'final location'])['total sold - igr'].sum().reset_index()
            fig_demand = px.line(demand_trends,
                               x='year',
                               y='total sold - igr',
                               color='final location',
                               title='Property Demand Trends',
                               labels={'total sold - igr': 'Units Sold',
                                      'year': 'Year',
                                      'final location': 'Location'})
            chart_data['demand_trends'] = json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig_demand))
            
        except Exception as e:
            logger.error(f"Error preparing chart data: {e}")
            chart_data = {"error": str(e)}
            
        return chart_data
    
    def _generate_mock_summary(self, query: str, data: pd.DataFrame) -> str:
        """Generate a mock summary when API fails"""
        locations = data['final location'].unique()
        
        if len(locations) == 0:
            return "No data available for the specified query. Please try with different parameters."
            
        if len(locations) == 1:
            loc = locations[0]
            avg_price = data['flat - weighted average rate'].mean()
            price_change = data.groupby('year')['flat - weighted average rate'].mean()
            growth = ((price_change.iloc[-1] - price_change.iloc[0]) / price_change.iloc[0] * 100) if len(price_change) > 1 else 0
            
            return f"""Analysis for {loc}:
- Average property price: ₹{avg_price:,.2f}
- Price growth: {growth:.1f}% over the analyzed period
- Market shows {'positive' if growth > 0 else 'negative'} trends
- {'Good investment potential' if growth > 0 else 'Exercise caution before investing'}"""
        
        else:
            locations_str = ", ".join(locations[:-1]) + " and " + locations[-1]
            return f"""Comparative analysis of {locations_str}:
- Multiple locations analyzed
- Each area shows distinct market patterns
- Consider local factors and infrastructure development
- Detailed price and demand trends shown in the charts"""