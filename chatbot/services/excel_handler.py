import pandas as pd
import numpy as np
import os
from django.conf import settings
from datetime import datetime

class ExcelHandler:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.df = None
        
    def load_data(self):
        """Load data from Excel file"""
        if not self.file_path:
            raise ValueError("File path not provided")
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        try:
            self.df = pd.read_excel(self.file_path)
            # Convert column names to lowercase and replace spaces with underscores for easier handling
            self.df.columns = [col.lower().replace(' ', '_') for col in self.df.columns]
            print(f"Loaded columns: {list(self.df.columns)}")  # Add this for debugging
            return True
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return False

    def get_areas(self):
        """Get list of unique areas in the dataset"""
        if self.df is None:
            self.load_data()
        
        # Based on your Excel file, the column is "final location" which becomes "final_location"
        area_column = 'final_location'
        
        if area_column in self.df.columns:
            # Convert to strings in case they are numeric, and sort
            areas = sorted([str(x) for x in self.df[area_column].unique() if x == x])  # x == x filters out NaN values
            return areas
        
        # If column not found, print available columns for debugging
        print(f"Area column '{area_column}' not found. Available columns: {list(self.df.columns)}")
        return []
    
    def filter_by_area(self, area):
        """Filter data by area"""
        if self.df is None:
            self.load_data()
        
        area_column = 'final_location'
        if area_column not in self.df.columns:
            return pd.DataFrame()
        
        filtered_df = self.df[self.df[area_column].str.lower() == area.lower()]
        return filtered_df
    
    def get_price_trend(self, area):
        """Get price trend data for an area"""
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty or 'year' not in filtered_df.columns or 'price' not in filtered_df.columns:
            return []
            
        # Group by year and calculate average price
        price_trend = filtered_df.groupby('year')['price'].mean().reset_index()
        return price_trend.to_dict('records')
    
    def get_demand_trend(self, area):
        """Get demand trend data for an area"""
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty or 'year' not in filtered_df.columns or 'demand' not in filtered_df.columns:
            return []
            
        # Group by year and calculate average demand
        demand_trend = filtered_df.groupby('year')['demand'].mean().reset_index()
        return demand_trend.to_dict('records')
    
    def compare_areas(self, areas, metric='price'):
        """Compare multiple areas based on a metric"""
        if self.df is None:
            self.load_data()
            
        if not areas or metric not in self.df.columns:
            return []
            
        result = []
        
        for area in areas:
            filtered_df = self.filter_by_area(area)
            if not filtered_df.empty and 'year' in filtered_df.columns:
                trend = filtered_df.groupby('year')[metric].mean().reset_index()
                trend['area'] = area
                result.append(trend)
                
        if not result:
            return []
            
        # Combine all areas data
        combined = pd.concat(result)
        return combined.to_dict('records')
    
    def get_growth_rate(self, area, years=3, metric='price'):
        """Calculate growth rate for an area over specified number of years"""
        if self.df is None:
            self.load_data()
            
        filtered_df = self.filter_by_area(area)
        
        if filtered_df.empty or 'year' not in filtered_df.columns or metric not in filtered_df.columns:
            return None
            
        # Get current year and calculate start year
        current_year = datetime.now().year
        start_year = current_year - years
        
        # Filter data for the specified year range
        year_filtered = filtered_df[filtered_df['year'] >= start_year]
        
        if year_filtered.empty:
            return None
            
        # Group by year and calculate average metric
        yearly_data = year_filtered.groupby('year')[metric].mean().reset_index()
        
        if len(yearly_data) < 2:
            return None
            
        # Calculate growth rate
        first_value = yearly_data.iloc[0][metric]
        last_value = yearly_data.iloc[-1][metric]
        
        if first_value == 0:
            return None
            
        growth_rate = ((last_value - first_value) / first_value) * 100
        return growth_rate