"""Simple PDF generator for company policy documents using reportlab."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os


def create_all_pdfs():
    """Create all 5 company policy PDF documents."""

    print("Creating company policy PDF documents...\n")
    os.makedirs('documents', exist_ok=True)

    # Create each PDF
    create_company_policy()
    create_hr_handbook()
    create_it_security()
    create_expense_policy()
    create_remote_work_policy()

    print("\n✅ All 5 PDF documents created successfully!")
    print(f"Location: {os.path.abspath('documents')}")


def create_pdf(filename, title, content_paragraphs):
    """Helper function to create a PDF with given content."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )


    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', parent=styles['Heading1'], alignment=TA_CENTER))

    story = []

    # Cover page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(title, styles['CenterTitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("TechCorp Solutions Inc.", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("2026", styles['Normal']))
    story.append(PageBreak())

    # Content
    for para in content_paragraphs:
        if para.startswith('###'):  # Section title
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph(para.replace('###', ''), styles['Heading2']))
        elif para.startswith('##'):  # Main title
            story.append(Spacer(1, 0.5*inch))
            story.append(Paragraph(para.replace('##', ''), styles['Heading1']))
        else:
            story.append(Paragraph(para, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

    doc.build(story)


def create_company_policy():
    """Create Company Policy Handbook."""
    content = [
        "## Company Policy Handbook",
        "Welcome to TechCorp Solutions Inc. This handbook outlines our company policies.",

        "### 1. Introduction",
        "All employees are expected to familiarize themselves with these policies and adhere to them.",

        "### 2. Code of Conduct",
        "All employees must maintain professional behavior:<br/>- Dress code: Business casual Monday-Thursday, Casual Friday<br/>- Respect and inclusion for all colleagues<br/>- Conflict of interest must be disclosed<br/>- Gifts and entertainment limited to $50 per instance",

        "### 3. Annual Leave Policy",
        "Annual leave entitlement based on tenure:<br/><br/>Standard (0-3 years): 15 days per year<br/>Senior (3+ years): 20 days per year<br/>Executive level: 25 days per year<br/><br/>Accrual: 1.25 days per month<br/>Carryover: Maximum 5 days to next year (expires March 31)<br/>Blackout Periods: Last week of fiscal quarters<br/>Request Process: Submit at least 2 weeks in advance via HR portal",

        "### 4. Sick Leave Policy",
        "Entitlement: 12 days per year<br/><br/>No doctor's note required for 1-2 days<br/>Doctor's note required for 3+ consecutive days<br/>Unused sick leave does NOT carry over<br/>Notification: Inform manager before 9 AM on first day<br/>Return to Work: Meeting required after 5+ consecutive days off",

        "### 5. Parental Leave",
        "Primary Caregiver: 12 weeks paid leave<br/>Secondary Caregiver: 4 weeks paid leave<br/><br/>Must be employed for 12+ months<br/>Flexible return options (part-time for 4 weeks)<br/>Notice: Inform HR at least 30 days before expected date",

        "### 6. Public Holidays 2026",
        "The following 10 public holidays are observed:<br/><br/>New Year's Day - January 1<br/>Martin Luther King Jr. Day - January 20<br/>Presidents' Day - February 17<br/>Memorial Day - May 25<br/>Independence Day - July 4<br/>Labor Day - September 7<br/>Thanksgiving - November 26-27<br/>Christmas - December 25",

        "### 7. Work Hours",
        "Standard Hours: 9 AM - 6 PM (8 hours + 1 hour lunch)<br/>Core Hours: 10 AM - 4 PM (must be present)<br/>Flexible Start: 8 AM - 10 AM allowed<br/>Time tracking mandatory<br/>Three late arrivals = written warning",

        "### 8. Performance Management",
        "Quarterly performance reviews<br/>Annual compensation review in March<br/><br/>Rating Scale: 5 (Exceptional), 4 (Exceeds), 3 (Meets), 2 (Needs Improvement), 1 (Unsatisfactory)<br/><br/>Ratings below 3 may result in Performance Improvement Plan",
    ]

    create_pdf('documents/company_policy.pdf', 'Company Policy Handbook', content)
    print("[OK] Created company_policy.pdf")


def create_hr_handbook():
    """Create HR Handbook."""
    content = [
        "## Human Resources Handbook",
        "Your guide to employment at TechCorp Solutions Inc.",

        "### 1. Onboarding",
        "5-day onboarding schedule:<br/>Day 1: Orientation, IT setup, ID badge<br/>Days 2-3: Department introductions<br/>Days 4-5: Role-specific training<br/><br/>Probation Period: 6 months<br/>30-60-90 Day Expectations clearly defined",

        "### 2. Compensation",
        "Pay Schedule: Bi-weekly (every other Friday)<br/>Direct Deposit: Mandatory<br/>Pay stubs via employee portal<br/>Overtime: 1.5x for hourly employees (40+ hours)",

        "### 3. Benefits Package",
        "Health Insurance: Company pays 80% of premiums<br/>Coverage starts first day of month after hire<br/><br/>401(k): Eligible after 3 months<br/>Company match: 50% up to 6% of salary<br/>4-year vesting schedule<br/><br/>Life Insurance: 2x annual salary (company-paid)<br/>Disability: Short-term and long-term<br/>EAP: Free confidential counseling",

        "### 4. Professional Development",
        "Annual Learning Budget: $2,000 per employee<br/>Conference Attendance: 1-2 per year (approved)<br/>Certification Reimbursement: 100% for job-related<br/>Tuition Assistance: 50% up to $5,000/year",

        "### 5. Performance Reviews",
        "Quarterly check-ins with manager<br/>Annual comprehensive review (January-February)<br/>360-degree feedback process<br/>SMART goals required<br/><br/>Rating Scale: 5 (Exceptional), 4 (Exceeds), 3 (Meets), 2 (Needs Improvement), 1 (Unsatisfactory)",

        "### 6. Resignation Process",
        "Notice Period: Individual Contributors (2 weeks), Managers (4 weeks), Executives (8 weeks)<br/><br/>Exit Process: Exit interview, return company property, final paycheck within 30 days, COBRA info<br/><br/>References: HR verifies employment dates and title only",
    ]

    create_pdf('documents/hr_handbook.pdf', 'HR Handbook', content)
    print("[OK] Created hr_handbook.pdf")


def create_it_security():
    """Create IT Security Guidelines."""
    content = [
        "## IT Security Guidelines",
        "CONFIDENTIAL - Information Security Best Practices",

        "### 1. Password Policy",
        "Requirements:<br/>- Minimum 12 characters<br/>- Uppercase, lowercase, numbers, special characters<br/>- Change every 90 days<br/>- Cannot reuse last 10 passwords<br/><br/>MFA required for all corporate accounts<br/>Use approved password manager (1Password, LastPass)",

        "### 2. Data Classification",
        "Public: Marketing materials, job postings<br/>Internal: Company memos, org charts<br/>Confidential: Customer data, financial records (encryption required)<br/>Secret: Trade secrets, unreleased products (AES-256 required)",

        "### 3. Email Security",
        "Phishing Red Flags:<br/>- Unexpected attachments or links<br/>- Urgent requests for credentials<br/>- Misspellings or grammar errors<br/><br/>Never click links from unknown senders<br/>Scan all attachments<br/>Use encryption for sensitive data",

        "### 4. Device Security",
        "Laptops: Full disk encryption mandatory, screen lock after 5 minutes, automatic updates, antivirus required<br/><br/>Mobile: MDM enrollment required, PIN/biometric lock, company data segregation<br/><br/>BYOD: Must meet security standards, separate work profile, company can remote wipe",

        "### 5. Network Security",
        "VPN: Required for all remote work and public WiFi<br/>Home WiFi: WPA2/WPA3 encryption required<br/>No unauthorized devices on corporate network<br/>IoT devices require IT approval",

        "### 6. Incident Reporting",
        "Report immediately: Phishing emails, lost/stolen devices, data breaches, malware, unauthorized access<br/><br/>Contact: security@techcorp.com or IT Hotline (555-0123)<br/>Response within 1 hour required<br/>Good-faith reporting = no punishment",
    ]

    create_pdf('documents/it_security_guidelines.pdf', 'IT Security Guidelines', content)
    print("[OK] Created it_security_guidelines.pdf")


def create_expense_policy():
    """Create Expense & Travel Policy."""
    content = [
        "## Expense & Travel Policy",
        "Guidelines for business expenses and travel",

        "### 1. Policy Overview",
        "All expenses must be reasonable, necessary, properly documented, and submitted within 30 days",

        "### 2. Flight Policy",
        "Economy class for flights under 6 hours<br/>Premium economy for 6-12 hour flights<br/>Business class for 12+ hours (Director+ only)<br/>Book 14+ days in advance<br/>Use corporate travel agency for 20% discount",

        "### 3. Hotel Policy",
        "Up to $200/night in major cities (NYC, SF, LA)<br/>Up to $150/night in other locations<br/>Extended stays (7+ nights): Airbnb/corporate housing allowed<br/>Use corporate hotel partners when available",

        "### 4. Per Diem Rates",
        "Domestic: Breakfast $15, Lunch $20, Dinner $40 (Total: $75/day)<br/>Europe: 85 euros/day<br/>Asia: $90/day<br/>Other regions: $80/day<br/><br/>Client Meals: IC ($100), Manager ($200), VP+ ($500)<br/>Alcohol: 2 drinks maximum, reasonable cost<br/>Receipts required for meals over $25",

        "### 5. Ground Transportation",
        "Airport shuttles preferred<br/>Taxi/rideshare allowed (keep receipts)<br/>Car rental: Mid-size or smaller<br/>Mileage reimbursement: $0.67/mile (IRS rate)",

        "### 6. Approval Requirements",
        "Pre-approval required for: International travel, expenses over $500, conference registration over $1,000, car rentals<br/><br/>Approval Hierarchy: Under $500 (manager), $500-$2,000 (dept head), $2,000-$5,000 (VP), Over $5,000 (CFO)",

        "### 7. Submission Process",
        "Submit within 30 days via Expensify<br/>Include: Business purpose, attendees (for meals), project code, receipt<br/>Reimbursement within 15 business days via direct deposit<br/>Late submissions require VP approval<br/>Expenses over 90 days: Not reimbursed",
    ]

    create_pdf('documents/expense_policy.pdf', 'Expense & Travel Policy', content)
    print("[OK] Created expense_policy.pdf")


def create_remote_work_policy():
    """Create Remote Work Policy."""
    content = [
        "## Remote Work Policy",
        "Guidelines for flexible work arrangements",

        "### 1. Introduction",
        "Remote work is a privilege enabling flexibility while maintaining productivity and collaboration",

        "### 2. Eligibility",
        "Requirements: Employed 6+ months, performance rating 3.5+, role suitable for remote, manager approval<br/>Trial period: 3 months",

        "### 3. Arrangements",
        "Fully Remote: 5 days/week from home<br/>Hybrid: 2-3 days remote, 2-3 days in office<br/>Occasional: As needed with approval<br/><br/>Office presence required for quarterly all-hands and team events",

        "### 4. Work Hours",
        "Core Hours: 10 AM - 4 PM local time (must be available)<br/>Flexible hours outside core time<br/><br/>Response Expectations: Email (4 hours), Slack (1 hour during core hours)<br/>Keep calendar accurate and updated",

        "### 5. Equipment",
        "Company Provided: Laptop, 27\" monitor, keyboard, mouse, headset, docking station<br/><br/>Optional: Second monitor, ergonomic chair (up to $300)<br/><br/>Stipends: Home office setup ($500 one-time), Internet ($50/month)<br/><br/>Dedicated workspace required",

        "### 6. Communication Tools",
        "Required: Slack (messaging), Zoom (video), Google Workspace (docs), Jira (tracking)<br/><br/>Best Practices: Video on for meetings, daily standups, weekly syncs, document all decisions",

        "### 7. Security",
        "VPN required for all work<br/>Home WiFi must use WPA2/WPA3<br/>Never work from public WiFi without VPN<br/>Lock workspace when away<br/>Follow IT Security Guidelines",

        "### 8. Performance",
        "Same expectations as in-office employees<br/>Outcome-based evaluation (not hours)<br/>Weekly 1:1s with manager<br/>Meet productivity metrics and KPIs<br/><br/>Performance issues may require return to office",

        "### 9. Legal Considerations",
        "Notify HR of location changes<br/>State tax implications may apply<br/>International remote requires special approval<br/>Consult tax professional for home office deductions",
    ]

    create_pdf('documents/remote_work_policy.pdf', 'Remote Work Policy', content)
    print("[OK] Created remote_work_policy.pdf")


if __name__ == "__main__":
    create_all_pdfs()
