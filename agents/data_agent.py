#!/usr/bin/env python3
"""
📊 Data-Agent
Data Engineer агент

Создаёт:
- ETL pipelines
- Data warehouses
- SQL аналитику
- Data quality checks
"""

import argparse
from pathlib import Path
from typing import Dict


class DataAgent:
    """
    📊 Data-Agent
    
    Специализация: Data Engineering
    Экспертиза: ETL, Data Warehousing, SQL, Big Data
    """
    
    NAME = "📊 Data-Agent"
    ROLE = "Data Engineer"
    EXPERTISE = ["ETL", "Data Warehousing", "SQL", "Big Data", "Apache Spark"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        files = {}
        
        files["etl_pipeline.py"] = """import pandas as pd
import logging
from datetime import datetime
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:
    '''ETL Pipeline for data processing'''
    
    def __init__(self, source: str, destination: str):
        self.source = source
        self.destination = destination
        self.data = None
    
    def extract(self) -> pd.DataFrame:
        '''Extract data from source'''
        logger.info(f"Extracting data from {self.source}")
        # Example: Read from CSV
        self.data = pd.read_csv(self.source)
        logger.info(f"Extracted {len(self.data)} rows")
        return self.data
    
    def transform(self) -> pd.DataFrame:
        '''Transform data'''
        logger.info("Transforming data")
        
        # Remove duplicates
        self.data = self.data.drop_duplicates()
        
        # Handle missing values
        self.data = self.data.fillna(method='ffill')
        
        # Data type conversions
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Add derived columns
        if 'amount' in self.data.columns:
            self.data['amount_category'] = pd.cut(
                self.data['amount'],
                bins=[0, 100, 1000, float('inf')],
                labels=['small', 'medium', 'large']
            )
        
        logger.info(f"Transformed data: {len(self.data)} rows")
        return self.data
    
    def load(self):
        '''Load data to destination'''
        logger.info(f"Loading data to {self.destination}")
        self.data.to_csv(self.destination, index=False)
        logger.info(f"Loaded {len(self.data)} rows to destination")
    
    def run(self):
        '''Execute full ETL pipeline'''
        self.extract()
        self.transform()
        self.load()
        logger.info("✅ ETL pipeline completed successfully")

if __name__ == "__main__":
    pipeline = ETLPipeline("input.csv", "output.csv")
    pipeline.run()
"""
        
        files["data_quality.py"] = """import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class DataQuality:
    '''Data Quality Assessment Tool'''
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.report = {}
    
    def check_completeness(self) -> Dict:
        '''Check for missing values'''
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        return {
            'missing_count': missing.to_dict(),
            'missing_percentage': missing_pct.to_dict(),
            'total_missing': missing.sum()
        }
    
    def check_uniqueness(self) -> Dict:
        '''Check for duplicate rows'''
        duplicates = self.df.duplicated().sum()
        return {
            'duplicate_rows': duplicates,
            'duplicate_percentage': round(duplicates / len(self.df) * 100, 2),
            'unique_rows': len(self.df) - duplicates
        }
    
    def check_consistency(self) -> Dict:
        '''Check data consistency'''
        issues = []
        
        # Check numeric ranges
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].min() < 0:
                issues.append(f"{col} has negative values")
        
        # Check date consistency
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            if self.df[col].max() > pd.Timestamp.now():
                issues.append(f"{col} has future dates")
        
        return {'consistency_issues': issues}
    
    def generate_report(self) -> Dict:
        '''Generate full quality report'''
        self.report = {
            'dataset_info': {
                'rows': len(self.df),
                'columns': len(self.df.columns),
                'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
            },
            'completeness': self.check_completeness(),
            'uniqueness': self.check_uniqueness(),
            'consistency': self.check_consistency()
        }
        return self.report
    
    def print_report(self):
        '''Print quality report'''
        report = self.generate_report()
        print("=" * 50)
        print("📊 DATA QUALITY REPORT")
        print("=" * 50)
        print(f"Rows: {report['dataset_info']['rows']}")
        print(f"Columns: {report['dataset_info']['columns']}")
        print(f"Memory: {report['dataset_info']['memory_usage']}")
        print(f"Duplicates: {report['uniqueness']['duplicate_rows']}")
        print("=" * 50)

if __name__ == "__main__":
    # Example
    df = pd.DataFrame({
        'id': [1, 2, 3, 3],
        'name': ['A', 'B', 'C', None],
        'value': [100, 200, -50, 400]
    })
    dq = DataQuality(df)
    dq.print_report()
"""
        
        return files


def main():
    parser = argparse.ArgumentParser(description="📊 Data-Agent — Data Engineering")
    parser.add_argument("request", nargs="?", help="Что создать")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    
    args = parser.parse_args()
    
    agent = DataAgent()
    
    if args.request:
        print(f"📊 {agent.NAME} создаёт: {args.request}")
        files = agent.process_request(args.request)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print(f"📊 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")


if __name__ == "__main__":
    main()
