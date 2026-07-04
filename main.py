import sys
from io_handlers import CSVDataPipeline
from matcher import SecretSantaEngine

def start_assignment_pipeline(current_csv: str, historic_csv: str, output_csv: str):
    try:
        print("[+] Standardizing employee database registry...")
        roster = CSVDataPipeline.parse_employee_registry(current_csv)
        
        print("[+] Extracting historical performance exclusions...")
        exclusions = CSVDataPipeline.parse_historical_constraints(historic_csv)
        
        print("[+] Processing optimization engine configurations...")
        engine = SecretSantaEngine(roster, exclusions)
        final_pairings = engine.compute_pairings()
        
        print(f"[+] Outputting processed pairs to file: {output_csv}")
        CSVDataPipeline.export_assignments(output_csv, final_pairings)
        print("[!] Secret Santa execution finalized successfully.")
        
    except Exception as err:
        print(f"[-] Operational Failure Encountered: {err}", file=sys.stderr)
        sys.exit(1)

if _name_ == "_main_":
    start_assignment_pipeline("employees.csv", "previous_year.csv", "secret_child_assignments.csv")