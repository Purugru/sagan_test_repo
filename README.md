# AW Client Report Portal - Working Prototype

This prototype demonstrates the complete full-stack pipeline of taking raw financial inputs, pulling static client data from a database, performing complex internal deterministic math, and generating the SACS and TCC PDF reports via a browser-native print strategy. 

We have implemented a local SQLite database (`db.sqlite`) to securely store client profiles, allowing the team to quickly load existing clients without re-entering static info (like salaries and deductibles) every quarter.

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

### 4. Run the Server
```bash
uvicorn main:app --reload
```
*Note: The server includes a startup event that automatically creates the `db.sqlite` database and seeds it with two dummy clients on the first run!*

### 5. Access the Portal
Open your browser and navigate to `http://127.0.0.1:8000`. You will see the structured form with pre-populated dummy data. Click **Generate PDF Report** at the bottom to download the automatically generated SACS and TCC PDF files!

---

## Next Steps (The Backlog)
If given more time beyond the 2 hours, the next logical features to implement would be:
1. **SQLite Database & Client CRUD**: Implementing persistent client profiles so the team doesn't have to re-enter static data every quarter.
2. **Pixel-Perfect Styling**: Refining the WeasyPrint CSS to perfectly replicate the original Canva graphic documents.
3. **Authentication/Security**: Ensuring only authorized team members can access client data.
