# AW Client Report Portal - Working Prototype

This prototype demonstrates the complete full-stack pipeline of taking raw financial inputs, pulling static client data from a database, performing complex internal deterministic math, and generating the SACS (Cashflow) report via a browser-native print strategy.

I implemented a local SQLite database (`db.sqlite`) to securely store client profiles. This fulfills the PRD's requirement to eliminate redundant data entry by allowing the team to quickly load existing clients and lock in their static info (like salaries and deductibles) every quarter.

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
*Note: The server includes a startup event that automatically creates the `db.sqlite` database and seeds it with two dummy clients on the first run.*

### 5. Access the Portal & Workflow
1. Open your browser and navigate to `http://127.0.0.1:8000`.
2. Use the **Select Client** dropdown at the top to load a profile (e.g., "The Smith Family").
3. Notice how the static baseline data (salary, budget) automatically pre-fills and locks in.
4. Enter dummy values for the dynamic quarterly bank balances.
5. Click **Generate Report**.
6. On the generated SACS diagram page, click **Print to PDF** (or use Ctrl+P / Cmd+P) to save the flawless, Tailwind-styled layout using your browser's native print engine.

---

## Next Steps (The Backlog)
Since I successfully built the math engine, database layer, and SACS print view within the 2-hour constraint, the next logical features to implement would be:

1. **TCC (Net Worth) Report Generation**: Applying the exact same Tailwind + Browser-Print strategy used for the SACS diagram to map out the TCC account bubbles.
2. **Client Management UI (CRUD)**: Building an admin screen to add, edit, or delete client profiles from the SQLite database directly from the browser, bypassing the need for database viewer tools.
3. **Automated Data Integrations (V2)**: Exploring secure API connections (e.g., the Zillow API for the trust value) to further reduce the manual entry of the dynamic quarterly balances.
