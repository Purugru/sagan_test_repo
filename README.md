# AW Client Report Portal - 2-Hour MVP

This prototype demonstrates the core pipeline of taking raw financial inputs, performing complex internal deterministic math, and generating the SACS and TCC PDF reports. 

As per the technical limitations of a 2-hour scope, this prototype deliberately bypasses persistent SQLite database storage (Client Management CRUD) to focus entirely on the highest-value core feature: the math and the PDF output.

## How to Run the Demo

### 1. Create a Virtual Environment
In your terminal, navigate to this project folder and run:
```bash
python -m venv venv
```

### 2. Activate the Virtual Environment
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: WeasyPrint might require additional system dependencies on Windows/macOS. E.g., GTK3. If you encounter a WeasyPrint error on Windows, you may need to install the [GTK3 runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases) first.)*

### 4. Run the Server
```bash
uvicorn main:app --reload
```

### 5. Access the Portal
Open your browser and navigate to `http://127.0.0.1:8000`. You will see the structured form with pre-populated dummy data. Click **Generate PDF Report** at the bottom to download the automatically generated SACS and TCC PDF files!

---

## Next Steps (The Backlog)
If given more time beyond the 2 hours, the next logical features to implement would be:
1. **SQLite Database & Client CRUD**: Implementing persistent client profiles so the team doesn't have to re-enter static data every quarter.
2. **Pixel-Perfect Styling**: Refining the WeasyPrint CSS to perfectly replicate the original Canva graphic documents.
3. **Authentication/Security**: Ensuring only authorized team members can access client data.
