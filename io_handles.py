import csv
from typing import List, Dict, Tuple
from models import Employee

class CSVDataPipeline:
    """Manages transactional file ingest, verification, and artifact writing."""

    @staticmethod
    def parse_employee_registry(file_path: str) -> List[Employee]:
        employees = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = {h.strip().lower(): h for h in reader.fieldnames} if reader.fieldnames else {}
                
                name_key = headers.get('employee_name')
                email_key = headers.get('employee_emailid')
                
                if not name_key or not email_key:
                    raise KeyError("Source file missing 'Employee_Name' or 'Employee_EmailID'.")
                
                for row in reader:
                    if row[name_key] and row[email_key]:
                        employees.append(Employee(row[name_key], row[email_key]))
        except FileNotFoundError:
            raise FileNotFoundError(f"Target manifest file could not be resolved at: {file_path}")
        return employees

    @staticmethod
    def parse_historical_constraints(file_path: str) -> Dict[str, str]:
        history_map = {}
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = {h.strip().lower(): h for h in reader.fieldnames} if reader.fieldnames else {}
                
                giver_key = headers.get('employee_emailid')
                child_key = headers.get('secret_child_emailid')
                
                if not giver_key or not child_key:
                    return history_map
                    
                for row in reader:
                    giver = row[giver_key].strip().lower()
                    child = row[child_key].strip().lower()
                    if giver and child:
                        history_map[giver] = child
        except FileNotFoundError:
            return {}
        return history_map

    @staticmethod
    def export_assignments(file_path: str, pairings: List[Tuple[Employee, Employee]]) -> None:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Employee_Name', 'Employee_EmailID', 
                    'Secret_Child_Name', 'Secret_Child_EmailID'
                ])
                for giver, child in pairings:
                    writer.writerow([giver.name, giver.email, child.name, child.email])
        except IOError as err:
            raise IOError(f"Critical writing failure while exporting assignments: {err}")