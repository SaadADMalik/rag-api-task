"""Generate professional company policy PDF documents."""

from fpdf import FPDF
import os
from datetime import datetime


class PolicyPDF(FPDF):
    """Custom PDF class for company policy documents."""

    def __init__(self, title):
        super().__init__()
        self.title_text = title
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        """Add header to each page."""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'TechCorp Solutions Inc.', 0, 0, 'L')
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        """Add footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Confidential - For Employee Use Only', 0, 0, 'C')

    def chapter_title(self, title, size=14):
        """Add a chapter title."""
        self.set_font('Arial', 'B', size)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        """Add chapter body text."""
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

    def add_bullet(self, text):
        """Add bullet point."""
        self.set_font('Arial', '', 11)
        self.cell(10, 6, '-', 0, 0)
        self.multi_cell(0, 6, text)


def create_company_policy_handbook():
    """Create Company Policy Handbook PDF."""
    pdf = PolicyPDF("Company Policy Handbook 2026")
    pdf.add_page()

    # Cover page
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, 'Company Policy Handbook', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 10, '2026', 0, 1, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, 'Effective: January 1, 2026', 0, 1, 'C')

    # Introduction
    pdf.add_page()
    pdf.chapter_title('1. Introduction')
    pdf.chapter_body(
        'Welcome to TechCorp Solutions Inc. This handbook outlines our company policies and '
        'procedures to ensure a productive, respectful, and compliant workplace. All employees '
        'are expected to familiarize themselves with these policies and adhere to them.'
    )

    # Code of Conduct
    pdf.chapter_title('2. Code of Conduct')
    pdf.chapter_body('All employees must maintain professional behavior:')
    pdf.add_bullet('Dress code: Business casual Monday-Thursday, Casual Friday')
    pdf.add_bullet('Respect and inclusion for all colleagues')
    pdf.add_bullet('Conflict of interest must be disclosed')
    pdf.add_bullet('Gifts and entertainment limited to $50 per instance')
    pdf.add_bullet('Professional social media conduct')

    # Annual Leave Policy
    pdf.chapter_title('3. Annual Leave Policy')
    pdf.chapter_body(
        'Annual leave entitlement is based on tenure:\n\n'
        '• Standard (0-3 years): 15 days per year\n'
        '• Senior (3+ years): 20 days per year\n'
        '• Executive level: 25 days per year\n\n'
        'Accrual: Leave accrues at 1.25 days per month for standard employees.\n\n'
        'Carryover: Maximum 5 days may be carried to the next year, expiring March 31.\n\n'
       'Blackout Periods: No leave during last week of fiscal quarters (Mar, Jun, Sep, Dec).\n\n'
        'Request Process: Submit requests at least 2 weeks in advance via HR portal. '
        'Manager approval required within 3 business days.'
    )

    # Sick Leave
    pdf.add_page()
    pdf.chapter_title('4. Sick Leave Policy')
    pdf.chapter_body(
        'Entitlement: 12 days per year\n\n'
        'Documentation:\n'
        '• No doctor\'s note required for 1-2 days\n'
        '• Doctor\'s note required for 3+ consecutive days\n'
        '• Unused sick leave does NOT carry over\n\n'
        'Notification: Inform your manager before 9 AM on the first day of absence.\n\n'
        'Return to Work: Meeting with manager required after 5+ consecutive days off.'
    )

    # Parental Leave
    pdf.chapter_title('5. Parental Leave')
    pdf.chapter_body(
        'Primary Caregiver: 12 weeks paid leave\n'
        'Secondary Caregiver: 4 weeks paid leave\n\n'
        'Eligibility: Must be employed for 12+ months\n\n'
        'Flexible Return: Part-time return for 4 weeks allowed\n\n'
        'Notice: Inform HR at least 30 days before expected date'
    )

    # Public Holidays
    pdf.chapter_title('6. Public Holidays 2026')
    pdf.chapter_body(
        'The following 10 public holidays are observed:\n\n'
        '• New Year\'s Day - January 1\n'
        '• Martin Luther King Jr. Day - January 20\n'
        '• Presidents\' Day - February 17\n'
        '• Memorial Day - May 25\n'
        '• Independence Day - July 4\n'
        '• Labor Day - September 7\n'
        '• Thanksgiving - November 26-27\n'
        '• Christmas - December 25\n\n'
        'If a holiday falls on a weekend, the following Monday will be observed.'
    )

    # Work Hours
    pdf.add_page()
    pdf.chapter_title('7. Work Hours and Attendance')
    pdf.chapter_body(
        'Standard Hours: 9 AM - 6 PM (8 hours + 1 hour lunch)\n\n'
        'Core Hours: 10 AM - 4 PM (must be present or available)\n\n'
        'Flexible Start: Between 8 AM - 10 AM allowed\n\n'
        'Time Tracking: Mandatory clock in/out via company system\n\n'
        'Punctuality: Three late arrivals result in written warning'
    )

    # Performance Management
    pdf.chapter_title('8. Performance Management')
    pdf.chapter_body(
        'Review Cycle:\n'
        '• Quarterly performance reviews with manager\n'
        '• Annual compensation review in March\n\n'
        'Rating Scale:\n'
        '• 5: Exceptional\n'
        '• 4: Exceeds Expectations\n'
        '• 3: Meets Expectations\n'
        '• 2: Needs Improvement\n'
        '• 1: Unsatisfactory\n\n'
        'Performance ratings below 3 may result in Performance Improvement Plan (PIP).'
    )

    pdf.output('documents/company_policy.pdf')
    print("✓ Created company_policy.pdf")


def create_hr_handbook():
    """Create HR Handbook PDF."""
    pdf = PolicyPDF("HR Handbook 2026")
    pdf.add_page()

    # Cover
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, 'Human Resources Handbook', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 10, '2026', 0, 1, 'C')

    # Onboarding
    pdf.add_page()
    pdf.chapter_title('1. Welcome & Onboarding')
    pdf.chapter_body(
        'New Hire Onboarding (5-day schedule):\n\n'
        'Day 1: Orientation, IT setup, ID badge\n'
        'Day 2-3: Department introductions, systems training\n'
        'Day 4-5: Role-specific training\n\n'
        'Probation Period: 6 months for all new hires\n\n'
        '30-60-90 Day Expectations:\n'
        '• 30 days: Learn systems and processes\n'
        '• 60 days: Begin independent work\n'
        '• 90 days: Full productivity expected'
    )

    # Compensation
    pdf.chapter_title('2. Compensation & Payroll')
    pdf.chapter_body(
        'Pay Schedule: Bi-weekly (every other Friday)\n\n'
        'Direct Deposit: Mandatory for all employees\n\n'
        'Pay Stub Access: Via employee self-service portal\n\n'
        'Overtime: 1.5x rate for hourly employees (40+ hours/week)'
    )

    # Benefits
    pdf.add_page()
    pdf.chapter_title('3. Benefits Package')
    pdf.chapter_body(
        'Health Insurance:\n'
        '• Company pays 80% of premiums\n'
        '• Coverage starts first day of month after hire date\n'
        '• Family coverage available\n\n'
        'Dental & Vision: Company pays 50% of premiums\n\n'
        '401(k) Retirement Plan:\n'
        '• Eligible after 3 months of employment\n'
        '• Company match: 50% up to 6% of salary\n'
        '• 4-year graded vesting schedule\n\n'
        'Life Insurance: 2x annual salary (company-paid)\n\n'
        'Disability Insurance: Short-term and long-term coverage\n\n'
        'Employee Assistance Program (EAP): Free confidential counseling services'
    )

    # Professional Development
    pdf.chapter_title('4. Professional Development')
    pdf.chapter_body(
        'Annual Learning Budget: $2,000 per employee\n\n'
        'Conference Attendance: 1-2 conferences per year (pre-approved)\n\n'
        'Certification Reimbursement: 100% for job-related certifications\n\n'
        'Tuition Assistance: 50% reimbursement up to $5,000 per year'
    )

    # Performance Reviews
    pdf.add_page()
    pdf.chapter_title('5. Performance Reviews')
    pdf.chapter_body(
        'Review Frequency:\n'
        '• Quarterly check-ins with direct manager\n'
        '• Annual comprehensive review (January-February)\n'
        '• 360-degree feedback process\n\n'
        'Goal Setting: SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)\n\n'
        'Rating Scale:\n'
        '• 5: Exceptional - Consistently exceeds all expectations\n'
        '• 4: Exceeds Expectations - Frequently goes above and beyond\n'
        '• 3: Meets Expectations - Solid, reliable performance\n'
        '• 2: Needs Improvement - Performance concerns\n'
        '• 1: Unsatisfactory - Immediate improvement required'
    )

    # Offboarding
    pdf.chapter_title('6. Resignation & Offboarding')
    pdf.chapter_body(
        'Notice Period Requirements:\n'
        '• Individual Contributors: 2 weeks\n'
        '• Managers: 4 weeks\n'
        '• Executives: 8 weeks\n\n'
        'Exit Process:\n'
        '• Exit interview with HR\n'
        '• Return of all company property\n'
        '• Final paycheck within 30 days\n'
        '• Benefits continuation (COBRA) information provided\n\n'
        'References: HR will verify employment dates and title only'
    )

    pdf.output('documents/hr_handbook.pdf')
    print("✓ Created hr_handbook.pdf")


def create_it_security_guidelines():
    """Create IT Security Guidelines PDF."""
    pdf = PolicyPDF("IT Security Guidelines 2026")
    pdf.add_page()

    # Cover
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, 'IT Security Guidelines', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'CONFIDENTIAL', 0, 1, 'C')
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, '2026', 0, 1, 'C')

    # Password Policy
    pdf.add_page()
    pdf.chapter_title('1. Password Policy')
    pdf.chapter_body(
        'Password Requirements:\n\n'
        '• Minimum 12 characters in length\n'
        '• Must include: uppercase, lowercase, numbers, and special characters\n'
        '• Change every 90 days\n'
        '• Cannot reuse last 10 passwords\n'
        '• No dictionary words, company name, or personal information\n\n'
        'Password Manager: Use approved tools (1Password, LastPass)\n\n'
        'Multi-Factor Authentication (MFA):\n'
        '• Required for all corporate accounts\n'
        '• Authenticator app preferred over SMS\n'
        '• Backup codes must be stored securely'
    )

    # Data Classification
    pdf.chapter_title('2. Data Classification')
    pdf.chapter_body(
        'Public: Marketing materials, job postings, press releases\n'
        '  → No special handling required\n\n'
        'Internal: Internal memos, org charts, general documents\n'
        '  → Company use only, not for external sharing\n\n'
        'Confidential: Customer data, financial records, employee information\n'
        '  → Encryption required, limited access\n\n'
        'Secret: Trade secrets, unreleased products, strategic plans\n'
        '  → AES-256 encryption mandatory, strict access controls'
    )

    # Email Security
    pdf.add_page()
    pdf.chapter_title('3. Email Security')
    pdf.chapter_body(
        'Phishing Awareness - Red Flags:\n'
        '• Unexpected attachments or links\n'
        '• Urgent requests for credentials or money\n'
        '• Misspellings or grammar errors\n'
        '• Sender email doesn\'t match display name\n\n'
        'Best Practices:\n'
        '• Verify suspicious emails by contacting sender directly\n'
        '• Never click links from unknown senders\n'
        '• Scan all attachments before opening\n'
        '• Use email encryption for sensitive data\n'
        '• Do not auto-forward company email\n'
        '• Minimize personal email use on company devices'
    )

    # Device Security
    pdf.chapter_title('4. Device Security')
    pdf.chapter_body(
        'Laptop Security:\n'
        '• Full disk encryption (mandatory)\n'
        '• Screen lock after 5 minutes of inactivity\n'
        '• Automatic updates enabled\n'
        '• Antivirus/EDR installed and updated\n'
        '• Report lost/stolen devices immediately to IT\n\n'
        'Mobile Devices:\n'
        '• MDM (Mobile Device Management) enrollment required\n'
        '• PIN or biometric lock mandatory\n'
        '• Company data segregation\n\n'
        'BYOD Policy:\n'
        '• Personal devices must meet minimum security standards\n'
        '• Separate work profile required\n'
        '• Company reserves right to remote wipe work data'
    )

    # VPN and Network
    pdf.add_page()
    pdf.chapter_title('5. Network Security')
    pdf.chapter_body(
        'VPN Usage:\n'
        '• Required for all remote work\n'
        '• Required when using public WiFi\n'
        '• Always-on VPN recommended\n\n'
        'WiFi Security:\n'
        '• Never connect to public WiFi without VPN\n'
        '• Home WiFi must use WPA2 or WPA3 encryption\n'
        '• Use guest network for personal devices at home\n\n'
        'Network Access:\n'
        '• No unauthorized devices on corporate network\n'
        '• IoT devices require IT approval'
    )

    # Incident Reporting
    pdf.chapter_title('6. Security Incident Reporting')
    pdf.chapter_body(
        'Report Immediately:\n'
        '• Suspected phishing emails\n'
        '• Lost or stolen devices\n'
        '• Data breaches or unauthorized access\n'
        '• Malware infections\n'
        '• Suspicious system behavior\n\n'
        'How to Report:\n'
        '• Email: security@techcorp.com\n'
        '• Phone: IT Hotline (555-0123)\n'
        '• Response within 1 hour of discovery required\n\n'
        'No Punishment: Good-faith reporting will not result in disciplinary action'
    )

    pdf.output('documents/it_security_guidelines.pdf')
    print("✓ Created it_security_guidelines.pdf")


def create_expense_policy():
    """Create Expense & Travel Policy PDF."""
    pdf = PolicyPDF("Expense & Travel Policy 2026")
    pdf.add_page()

    # Cover
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, 'Expense & Travel Policy', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 10, '2026', 0, 1, 'C')

    # Policy Overview
    pdf.add_page()
    pdf.chapter_title('1. Policy Overview')
    pdf.chapter_body(
        'This policy governs all business-related expenses and travel. All expenses must be:\n\n'
        '• Reasonable and necessary for business purposes\n'
        '• Properly documented with receipts\n'
        '• Submitted within 30 days\n'
        '• Pre-approved when required'
    )

    # Travel Policy
    pdf.chapter_title('2. Travel Arrangements')
    pdf.chapter_body(
        'Flight Policy:\n'
        '• Economy class for flights under 6 hours\n'
        '• Premium economy for 6-12 hour flights\n'
        '• Business class for 12+ hour flights (Director level and above only)\n'
        '• Book 14+ days in advance when possible\n'
        '• Use corporate travel agency for 20% discount\n\n'
        'Hotel Policy:\n'
        '• Up to $200/night in major cities (NYC, SF, LA, etc.)\n'
        '• Up to $150/night in other locations\n'
        '• Must use corporate hotel partners when available\n'
        '• Extended stays (7+ nights): Airbnb or corporate housing allowed\n\n'
        'Ground Transportation:\n'
        '• Airport shuttles preferred\n'
        '• Taxi/rideshare allowed (keep receipts)\n'
        '• Car rental: Mid-size or smaller (unless 3+ travelers)\n'
        '• Mileage reimbursement: $0.67 per mile (current IRS rate)'
    )

    # Meals
    pdf.add_page()
    pdf.chapter_title('3. Meals & Per Diem')
    pdf.chapter_body(
        'Domestic Travel Per Diem:\n'
        '• Breakfast: $15\n'
        '• Lunch: $20\n'
        '• Dinner: $40\n'
        '• Total daily: $75\n\n'
        'International Travel Per Diem:\n'
        '• Europe: €85/day\n'
        '• Asia: $90/day\n'
        '• Other regions: $80/day\n\n'
        'Client Meals:\n'
        '• Individual Contributor: Up to $100/meal (manager approval)\n'
        '• Manager: Up to $200/meal\n'
        '• VP and above: Up to $500/meal\n'
        '• Alcohol: Limited to 2 drinks, reasonable cost\n\n'
        'Receipts required for all meals over $25'
    )

    # Approval Workflows
    pdf.chapter_title('4. Approval Requirements')
    pdf.chapter_body(
        'Pre-Approval Required For:\n'
        '• All international travel\n'
        '• Any expense over $500\n'
        '• Conference registration over $1,000\n'
        '• Car rentals\n\n'
        'Approval Hierarchy:\n'
        '• Under $500: Direct manager\n'
        '• $500 - $2,000: Department head\n'
        '• $2,000 - $5,000: VP\n'
        '• Over $5,000: CFO approval required'
    )

    # Submission
    pdf.add_page()
    pdf.chapter_title('5. Expense Submission')
    pdf.chapter_body(
        'Submission Requirements:\n'
        '• Submit within 30 days of expense date\n'
        '• Late submissions require VP approval\n'
        '• Expenses over 90 days old will not be reimbursed\n\n'
        'Use Expensify Platform with:\n'
        '• Business purpose description\n'
        '• Attendee names (for meals)\n'
        '• Project/client code\n'
        '• Receipt attachment (required for amounts over $25)\n\n'
        'Reimbursement:\n'
        '• Processed within 15 business days of approval\n'
        '• Direct deposit to employee bank account\n'
        '• Currency conversions at submission date rate'
    )

    pdf.output('documents/expense_policy.pdf')
    print("✓ Created expense_policy.pdf")


def create_remote_work_policy():
    """Create Remote Work Policy PDF."""
    pdf = PolicyPDF("Remote Work Policy 2026")
    pdf.add_page()

    # Cover
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, 'Remote Work Policy', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 10, '2026', 0, 1, 'C')

    # Introduction
    pdf.add_page()
    pdf.chapter_title('1. Introduction')
    pdf.chapter_body(
        'This policy establishes guidelines for remote work arrangements. Remote work is '
        'considered a privilege that enables flexibility while maintaining productivity '
        'and collaboration.'
    )

    # Eligibility
    pdf.chapter_title('2. Eligibility Criteria')
    pdf.chapter_body(
        'Employees must meet the following criteria:\n\n'
        '• Employed for at least 6 months\n'
        '• Satisfactory performance rating (3.5 out of 5 or higher)\n'
        '• Role suitable for remote work\n'
        '• Manager approval required\n'
        '• 3-month trial period for new remote workers'
    )

    # Arrangements
    pdf.chapter_title('3. Remote Work Arrangements')
    pdf.chapter_body(
        'Fully Remote: Work from home 5 days per week\n\n'
        'Hybrid: 2-3 days remote, 2-3 days in office\n\n'
        'Occasional: As needed with manager approval\n\n'
        'Office Presence: Required for quarterly all-hands meetings and team events'
    )

    # Work Hours
    pdf.add_page()
    pdf.chapter_title('4. Work Hours and Availability')
    pdf.chapter_body(
        'Core Hours: 10 AM - 4 PM local time (must be available)\n\n'
        'Flexible Hours: Outside core hours at employee discretion\n\n'
        'Response Time Expectations:\n'
        '• Email: Within 4 hours during core hours\n'
        '• Slack: Within 1 hour during core hours\n'
        '• Calendar: Must be kept accurate and up-to-date\n\n'
        'Time Zone Considerations: Distributed teams should coordinate overlap hours'
    )

    # Equipment
    pdf.chapter_title('5. Equipment and Home Office')
    pdf.chapter_body(
        'Company Provided Equipment:\n'
        '• Laptop (MacBook Pro or ThinkPad)\n'
        '• 27" external monitor\n'
        '• Keyboard and mouse\n'
        '• Headset for calls\n'
        '• Docking station\n\n'
        'Optional Equipment (upon request):\n'
        '• Second monitor\n'
        '• Ergonomic chair stipend: Up to $300\n\n'
        'Stipends:\n'
        '• Home office setup: $500 one-time\n'
        '• Internet reimbursement: $50/month\n\n'
        'Home Office Requirements:\n'
        '• Dedicated workspace\n'
        '• Ergonomic setup\n'
        '• Professional background for video calls'
    )

    # Communication
    pdf.add_page()
    pdf.chapter_title('6. Communication Tools')
    pdf.chapter_body(
        'Required Tools:\n'
        '• Slack: Primary messaging platform\n'
        '• Zoom: Video conferencing\n'
        '• Google Workspace: Documents and collaboration\n'
        '• Jira: Project tracking\n\n'
        'Best Practices:\n'
        '• Video on for all meetings\n'
        '• Participate in daily standups\n'
        '• Attend weekly team syncs\n'
        '• Document all decisions in writing\n'
        '• Use async communication when possible'
    )

    # Security
    pdf.chapter_title('7. Security Requirements')
    pdf.chapter_body(
        'Mandatory Security Measures:\n\n'
        '• VPN usage required for all work\n'
        '• Home WiFi must use WPA2/WPA3 encryption\n'
        '• Never work from public WiFi without VPN\n'
        '• Lock workspace when away\n'
        '• Follow confidential information handling procedures\n'
        '• Comply with IT Security Guidelines\n\n'
        'See IT Security Guidelines document for complete requirements'
    )

    # Performance
    pdf.add_page()
    pdf.chapter_title('8. Performance and Accountability')
    pdf.chapter_body(
        'Performance Expectations:\n\n'
        '• Same standards as in-office employees\n'
        '• Outcome-based evaluation (not hours worked)\n'
        '• Weekly 1:1 meetings with manager\n'
        '• Meet productivity metrics and KPIs\n'
        '• Maintain quality and timeliness of deliverables\n\n'
        'Performance issues may result in return to office requirement'
    )

    # Legal
    pdf.chapter_title('9. Legal and Tax Considerations')
    pdf.chapter_body(
        'Work Location:\n'
        '• Must notify HR of any location changes\n'
        '• State tax implications may apply\n'
        '• International remote work requires special approval\n\n'
        'Tax Deductions:\n'
        '• Consult tax professional for home office deductions\n'
        '• Company does not provide tax advice'
    )

    pdf.output('documents/remote_work_policy.pdf')
    print("✓ Created remote_work_policy.pdf")


# Generate all PDFs
if __name__ == "__main__":
    print("Generating company policy PDF documents...\n")

    # Create documents directory if it doesn't exist
    os.makedirs('documents', exist_ok=True)

    create_company_policy_handbook()
    create_hr_handbook()
    create_it_security_guidelines()
    create_expense_policy()
    create_remote_work_policy()

    print("\n✅ All 5 PDF documents created successfully!")
    print(f"Location: {os.path.abspath('documents')}")
