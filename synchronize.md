# Application Sync Document: AW Client Portal (2-Hour MVP Version)

## 1. Global Data Contract
To adhere strictly to the 2-hour constraint, avoid dynamic arrays and JavaScript DOM manipulation. All workers MUST use the following flattened variable names to ensure the components link up natively.

**Form Data (HTML standard POST -> Backend FastAPI `Form(...)`):**
- `client_1_ira_balance` (Float)
- `client_2_roth_balance` (Float)
- `joint_brokerage_balance` (Float)
- `mortgage_balance` (Float)
- `zillow_trust_value` (Float)

**Backend Calculation Output (Jinja Variables for PDF):**
- `{{ client_name }}` (String - e.g., "John & Jane Doe")
- `{{ inflow_amount }}` (Float - from DB)
- `{{ outflow_amount }}` (Float - from DB)
- `{{ sacs_excess }}` (Float - calculated)
- `{{ private_reserve_target }}` (Float - calculated)
- `{{ tcc_client_1_retirement_total }}` (Float - calculated)
- `{{ tcc_client_2_retirement_total }}` (Float - calculated)
- `{{ tcc_non_retirement_total }}` (Float - calculated)
- `{{ trust_value }}` (Float - exact match to zillow_trust_value)
- `{{ tcc_grand_total_net_worth }}` (Float - calculated)
- `{{ tcc_liabilities_total }}` (Float - calculated)

---

## 2. Component Directives

### Worker 1: UI Architect (`templates/index.html`)
- **Task:** Build a beautiful, modern data entry form using Tailwind CSS (via CDN).
- **Constraints:** NO JavaScript whatsoever. Do not build dynamic arrays or use JSON payloads.
- **Form Specs:** Create a standard HTML form `<form action="/generate" method="POST">`. 
- **Inputs:** Create exactly 5 number inputs mapped exactly to the `Form Data` variable names in the Global Data Contract (e.g., `name="client_1_ira_balance"`).
- **Design:** Group the inputs logically (Retirement, Non-Retirement, Trust, Liabilities). Make it look like a premium internal financial tool.

### Worker 2: Backend Logic (`main.py`)
- **Task:** Build the FastAPI backend and deterministic math engine.
- **Database (The 15% Flex):** Implement a local, ephemeral SQLite database using Python's built-in `sqlite3`. On startup, create a `clients` table and seed it with one record: Name: "John & Jane Doe", Salary: 15000, Expense Budget: 11000, Insurance Deductibles: 2000.
- **Endpoint:** Create a POST `/generate` route that reads the static data from SQLite and accepts the 5 exact `Form Data` variables using FastAPI's `Form(...)`.
- **Math Engine (CRITICAL RULES):**
  - SACS Excess = Salary - Expense Budget
  - Private Reserve Target = (6 * Expense Budget) + Insurance Deductibles
  - Client 1 Retirement Total = `client_1_ira_balance`
  - Client 2 Retirement Total = `client_2_roth_balance`
  - Non-Retirement Total = `joint_brokerage_balance`
  - Grand Total Net Worth = Client 1 + Client 2 + Non-Retirement + `zillow_trust_value`
  - Liabilities Total = `mortgage_balance`
  - **STRICT PRD RULE:** Liabilities exist in a separate box. NEVER subtract them from the Net Worth. NEVER add the trust value into the Non-Retirement total.
- **Output:** Render the calculated totals into the `sacs_report.html` and `tcc_report.html` Jinja templates and return a PDF via WeasyPrint.

### Worker 3: PDF Templater (`templates/sacs_report.html` & `templates/tcc_report.html`)
- **Task:** Build Jinja2 HTML templates optimized for WeasyPrint to generate fixed-layout PDFs.
- **Constraints:** Do NOT use Jinja `{% for %}` loops to iterate over accounts. We are hardcoding the structure to ensure visual stability for the MVP.
- **SACS Layout:** Create a fixed cashflow bubble diagram using embedded CSS flexbox/grid. Connect conceptual boxes: Inflow (green), Outflow (red), and Private Reserve (blue).
- **TCC Layout:** Create a fixed layout mapping the 5 specific inputs: Retirement accounts at the top, Non-Retirement at the bottom, Trust in the center, and Liabilities in a visually separated section.
- **Variables:** Inject the exact Jinja variables listed in the `Backend Calculation Output` contract above.