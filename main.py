import csv
import codecs
import sys
from io import StringIO
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

# Import our custom modules
from models import Employee
from matcher import SecretSantaEngine

app = FastAPI(title="Acme Secret Santa Engine API")

def parse_csv_stream(file_bytes) -> tuple:
    """Helper method to parse uploaded raw network file streams safely."""
    csv_data = codecs.iterdecode(file_bytes, 'utf-8')
    reader = csv.DictReader(StringIO("".join(list(csv_data))))
    headers = {h.strip().lower(): h for h in reader.fieldnames} if reader.fieldnames else {}
    return reader, headers

@app.post("/generate-assignments/")
async def generate_assignments(
    current_year_file: UploadFile = File(...),
    previous_year_file: Optional[UploadFile] = File(None)
):
    try:
        # 1. Process current employee roster upload
        current_content = await current_year_file.read()
        reader, headers = parse_csv_stream(current_content)
        
        name_key = headers.get('employee_name')
        email_key = headers.get('employee_emailid')
        if not name_key or not email_key:
            raise HTTPException(status_code=400, detail="Missing required columns in employee list.")
            
        roster = [Employee(row[name_key], row[email_key]) for row in reader if row.get(name_key)]

        # 2. Process historical exclusion file if attached
        exclusions = {}
        if previous_year_file:
            prev_content = await previous_year_file.read()
            p_reader, p_headers = parse_csv_stream(prev_content)
            giver_key = p_headers.get('employee_emailid')
            child_key = p_headers.get('secret_child_emailid')
            
            if giver_key and child_key:
                exclusions = {row[giver_key].strip().lower(): row[child_key].strip().lower() 
                              for row in p_reader if row.get(giver_key)}

        # 3. Compute the assignments
        engine = SecretSantaEngine(roster, exclusions)
        final_pairings = engine.compute_pairings()

        # 4. Stream output data back over the connection dynamically
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID'])
        
        for giver, child in final_pairings:
            writer.writerow([giver.name, giver.email, child.name, child.email])
            
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=secret_santa_matches.csv"}
        )

    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

# This block MUST be completely flush against the left margin
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)