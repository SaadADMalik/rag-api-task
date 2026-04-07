#!/usr/bin/env python3
"""
HR Handbook PDF Generator for TechCorp Solutions Inc.
Creates a professional, multi-page HR handbook with proper formatting
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus import KeepTogether
from reportlab.pdfgen import canvas
from datetime import datetime

# Define company colors
CORPORATE_BLUE = HexColor('#1e3a8a')
LIGHT_BLUE = HexColor('#3b82f6')
GRAY = HexColor('#6b7280')
LIGHT_GRAY = HexColor('#f3f4f6')

class NumberedCanvas(canvas.Canvas):
    """Custom canvas to add page numbers and footer"""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page_num = self._pageNumber
        # Skip page number on first page (cover)
        if page_num > 1:
            self.setFont("Helvetica", 9)
            self.setFillColor(GRAY)
            # Page number at bottom center
            self.drawCentredString(4.25 * inch, 0.5 * inch, f"Page {page_num - 1}")
            # Footer text
            self.setFont("Helvetica-Oblique", 8)
            self.drawCentredString(4.25 * inch, 0.35 * inch,
                                 "Confidential - For Employee Use Only")


def create_hr_handbook():
    """Generate the complete HR Handbook PDF"""

    output_file = r"D:\Whatsapp analyzer\documents\hr_handbook.pdf"

    # Create document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=1*inch
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=CORPORATE_BLUE,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=20,
        textColor=LIGHT_BLUE,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    company_style = ParagraphStyle(
        'CompanyName',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=CORPORATE_BLUE,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=CORPORATE_BLUE,
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=LIGHT_BLUE,
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=CORPORATE_BLUE,
        spaceAfter=6,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=black,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=black,
        spaceAfter=4,
        leftIndent=20,
        fontName='Helvetica'
    )

    # =========================
    # COVER PAGE
    # =========================
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("TechCorp Solutions Inc.", company_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Human Resources Handbook", title_style))
    elements.append(Paragraph("2026 Edition", subtitle_style))
    elements.append(Spacer(1, 1*inch))

    # Cover page info box
    cover_info = [
        ["Effective Date:", "January 1, 2026"],
        ["Version:", "3.2"],
        ["Department:", "Human Resources"],
        ["Last Updated:", "April 2026"]
    ]

    cover_table = Table(cover_info, colWidths=[2*inch, 3*inch])
    cover_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('TEXTCOLOR', (0, 0), (0, -1), CORPORATE_BLUE),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(cover_table)
    elements.append(Spacer(1, 1*inch))

    elements.append(Paragraph(
        "This handbook provides essential information about TechCorp Solutions Inc.'s policies, "
        "benefits, and expectations. All employees are expected to read and understand the "
        "contents of this handbook. Please consult with Human Resources if you have any questions.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # TABLE OF CONTENTS
    # =========================
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    toc_items = [
        "1. Welcome & Onboarding",
        "2. Employment Classification",
        "3. Compensation & Payroll",
        "4. Benefits Package",
        "5. Professional Development",
        "6. Performance Reviews",
        "7. Career Progression",
        "8. Leave Policies",
        "9. Offboarding & Resignation",
        "10. Employee Relations"
    ]

    for item in toc_items:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(PageBreak())

    # =========================
    # SECTION 1: WELCOME & ONBOARDING
    # =========================
    elements.append(Paragraph("Section 1: Welcome & Onboarding", heading1_style))

    elements.append(Paragraph(
        "Welcome to TechCorp Solutions Inc.! We are thrilled to have you join our team. "
        "This section outlines what you can expect during your first days, weeks, and months with us.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("New Hire Onboarding Process", heading2_style))
    elements.append(Paragraph(
        "Our comprehensive 5-day onboarding program is designed to set you up for success:",
        body_style
    ))

    onboarding_schedule = [
        ["Day", "Activities"],
        ["Day 1", "• Welcome session with HR\n• IT setup and equipment distribution\n• Office tour and introductions\n• Review company culture and values"],
        ["Day 2", "• Department overview and team introductions\n• Role-specific training begins\n• Set up development environment\n• Lunch with your buddy/mentor"],
        ["Day 3", "• Benefits enrollment session\n• Security and compliance training\n• First team meeting\n• Review of key projects and roadmap"],
        ["Day 4", "• Shadowing team members\n• Access to learning resources\n• Introduction to tools and systems\n• One-on-one with direct manager"],
        ["Day 5", "• First small assignment or task\n• 30-60-90 day plan review\n• Questions and feedback session\n• Week 1 check-in with HR"]
    ]

    schedule_table = Table(onboarding_schedule, colWidths=[1*inch, 5.5*inch])
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CORPORATE_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY])
    ]))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(schedule_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("First Day Checklist", heading2_style))
    checklist_items = [
        "Complete all required HR paperwork (I-9, W-4, tax forms)",
        "Receive employee ID badge and building access card",
        "Laptop, monitor, and necessary equipment setup",
        "Email and system account creation",
        "Emergency contact information submitted",
        "Parking pass or transit benefits enrollment (if applicable)",
        "Introduction to employee portal and self-service tools"
    ]

    for item in checklist_items:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("30-60-90 Day Expectations", heading2_style))

    expectations_data = [
        ["Period", "Goals & Expectations"],
        ["First 30 Days", "• Learn company culture, values, and organizational structure\n• Complete all required training modules\n• Understand your role, responsibilities, and immediate team\n• Begin contributing to team projects with guidance\n• Establish relationships with key stakeholders"],
        ["60 Days", "• Demonstrate growing independence in core responsibilities\n• Complete first substantial project or deliverable\n• Actively participate in team meetings and discussions\n• Identify areas for process improvement\n• Seek and incorporate feedback from manager"],
        ["90 Days", "• Operate independently in primary job functions\n• Take ownership of projects and initiatives\n• Contribute innovative ideas and solutions\n• Build cross-functional relationships\n• Complete probationary period review with manager"]
    ]

    expectations_table = Table(expectations_data, colWidths=[1.2*inch, 5.3*inch])
    expectations_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ]))

    elements.append(expectations_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Buddy/Mentor Program", heading2_style))
    elements.append(Paragraph(
        "Each new hire is paired with an experienced team member who serves as your buddy for the "
        "first 90 days. Your buddy will help you navigate the company, answer questions, and provide "
        "informal guidance. This is separate from your manager and provides a safe space to learn "
        "and grow. Your buddy will reach out within your first week to schedule regular check-ins.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("Probationary Period", heading2_style))
    elements.append(Paragraph(
        "All new employees are subject to a 6-month probationary period. During this time, both "
        "you and TechCorp can assess the fit of the role. Performance will be evaluated at 30, "
        "60, and 90 days, with a final review at the end of the probationary period. Successful "
        "completion of probation is required for full employment status and eligibility for certain benefits.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 2: EMPLOYMENT CLASSIFICATION
    # =========================
    elements.append(Paragraph("Section 2: Employment Classification", heading1_style))

    elements.append(Paragraph(
        "TechCorp Solutions Inc. employs individuals under various classifications, each with "
        "different terms, conditions, and benefits. Understanding your employment classification "
        "is important for knowing your rights and benefits.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    classification_data = [
        ["Classification", "Description", "Benefits Eligibility"],
        ["Full-Time\nEmployees", "Regular employees working 40 hours per week on a consistent schedule. Eligible for all company benefits and programs.", "Full benefits package including health insurance, 401(k), PTO, and all other company benefits."],
        ["Part-Time\nEmployees", "Employees working fewer than 30 hours per week. May have variable schedules based on business needs.", "Prorated PTO and limited benefits. Health insurance available if working 20+ hours/week (employee pays 60% of premium)."],
        ["Contractors &\nConsultants", "Independent professionals engaged for specific projects or time periods. Not considered employees for tax or benefit purposes.", "Not eligible for employee benefits. Paid per contract terms. Responsible for own taxes and insurance."],
        ["Intern\nPrograms", "Students or recent graduates in temporary learning positions (typically 10-12 weeks). May be paid or unpaid based on program.", "Paid interns receive hourly compensation. Not eligible for standard benefits. May receive stipends for housing or transportation."]
    ]

    classification_table = Table(classification_data, colWidths=[1.3*inch, 2.6*inch, 2.6*inch])
    classification_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CORPORATE_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white, LIGHT_GRAY])
    ]))

    elements.append(classification_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph(
        "Your employment classification is specified in your offer letter and employment agreement. "
        "If you have questions about your classification or wish to discuss a change in status, "
        "please contact Human Resources.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 3: COMPENSATION & PAYROLL
    # =========================
    elements.append(Paragraph("Section 3: Compensation & Payroll", heading1_style))

    elements.append(Paragraph("Pay Schedule", heading2_style))
    elements.append(Paragraph(
        "TechCorp operates on a bi-weekly pay schedule. Employees are paid every other Friday "
        "for the two-week period ending the previous Sunday. Your first paycheck will be "
        "issued on the second scheduled payday following your start date to allow for "
        "payroll processing.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Salary Bands by Level", heading2_style))
    elements.append(Paragraph(
        "TechCorp maintains competitive salary bands aligned with market rates and adjusted "
        "annually for cost of living and market conditions. Salary ranges by level:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    salary_data = [
        ["Level", "Years Experience", "Salary Range (Annual)"],
        ["Junior", "0-2 years", "$65,000 - $85,000"],
        ["Mid-Level", "2-5 years", "$85,000 - $120,000"],
        ["Senior", "5-8 years", "$120,000 - $160,000"],
        ["Lead", "8-12 years", "$160,000 - $200,000"],
        ["Principal", "12+ years", "$200,000 - $280,000+"]
    ]

    salary_table = Table(salary_data, colWidths=[1.5*inch, 2*inch, 3*inch])
    salary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white, LIGHT_GRAY, white])
    ]))

    elements.append(salary_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph(
        "<i>Note: Actual compensation is determined by role, location, experience, and performance. "
        "Ranges shown are for general reference and may vary by department and specialization.</i>",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Direct Deposit", heading2_style))
    elements.append(Paragraph(
        "Direct deposit is mandatory for all employees. You will need to provide your banking "
        "information during onboarding or through the employee self-service portal. Funds are "
        "typically available in your account by 6:00 AM on payday. You can split your deposit "
        "between multiple accounts if desired.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Pay Stub Access", heading2_style))
    elements.append(Paragraph(
        "Pay stubs are available electronically through the employee portal at portal.techcorp.com. "
        "You will receive an email notification when each pay stub is available. Pay stubs include "
        "detailed information about earnings, deductions, taxes, and year-to-date totals. Please "
        "review your pay stub each pay period and report any discrepancies to HR immediately.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Overtime Policy", heading2_style))
    elements.append(Paragraph(
        "Non-exempt hourly employees are eligible for overtime compensation at 1.5 times their "
        "regular hourly rate for all hours worked beyond 40 in a single workweek. Overtime must "
        "be approved in advance by your manager. Salaried exempt employees are not eligible for "
        "overtime pay but may be eligible for compensatory time off at manager discretion. "
        "All work time must be accurately recorded in the timekeeping system.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 4: BENEFITS PACKAGE
    # =========================
    elements.append(Paragraph("Section 4: Benefits Package", heading1_style))

    elements.append(Paragraph(
        "TechCorp Solutions Inc. is committed to providing a comprehensive and competitive benefits "
        "package that supports the health, wellbeing, and financial security of our employees and "
        "their families.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Health Insurance", heading2_style))
    elements.append(Paragraph("• <b>Company Contribution:</b> TechCorp pays 80% of health insurance premiums for employee coverage", bullet_style))
    elements.append(Paragraph("• <b>Coverage Start Date:</b> First day of the month following your hire date", bullet_style))
    elements.append(Paragraph("• <b>Family Coverage:</b> Spouses and dependents may be added to your plan (employee pays difference)", bullet_style))
    elements.append(Paragraph("• <b>Plan Options:</b> PPO and High-Deductible Health Plan (HDHP) with HSA option", bullet_style))
    elements.append(Paragraph("• <b>Coverage Includes:</b> Medical, prescription drugs, preventive care, mental health services", bullet_style))
    elements.append(Paragraph("• <b>Networks:</b> Nationwide coverage with preferred provider networks", bullet_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Dental & Vision Insurance", heading2_style))
    elements.append(Paragraph("• <b>Company Contribution:</b> TechCorp pays 50% of premiums for employee coverage", bullet_style))
    elements.append(Paragraph("• <b>Dental Coverage:</b> Two cleanings per year, X-rays, fillings, major dental work", bullet_style))
    elements.append(Paragraph("• <b>Vision Coverage:</b> Annual eye exam, frames or contacts, lens coverage", bullet_style))
    elements.append(Paragraph("• <b>Family Plans Available:</b> Add dependents at employee expense", bullet_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("401(k) Retirement Plan", heading2_style))
    elements.append(Paragraph("• <b>Eligibility:</b> You become eligible after 3 months of employment", bullet_style))
    elements.append(Paragraph("• <b>Company Match:</b> TechCorp matches 50% of your contributions up to 6% of your salary", bullet_style))
    elements.append(Paragraph("  <i>Example: If you contribute 6% of salary, TechCorp adds 3% for total of 9%</i>", bullet_style))
    elements.append(Paragraph("• <b>Vesting Schedule:</b> Company contributions vest over 4 years (25% per year)", bullet_style))
    elements.append(Paragraph("• <b>Employee Contributions:</b> Your contributions are always 100% vested immediately", bullet_style))
    elements.append(Paragraph("• <b>Investment Options:</b> Diverse selection of funds including target-date, index, and managed options", bullet_style))
    elements.append(Paragraph("• <b>Roth 401(k):</b> After-tax contribution option available", bullet_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Life Insurance", heading2_style))
    elements.append(Paragraph(
        "TechCorp provides company-paid basic life insurance coverage equal to 2x your annual "
        "salary at no cost to you. You may purchase supplemental life insurance for yourself "
        "and your dependents through payroll deduction. Beneficiary designation is required "
        "during enrollment.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Disability Insurance", heading2_style))
    elements.append(Paragraph(
        "Both short-term and long-term disability insurance are provided at no cost to employees:",
        body_style
    ))
    elements.append(Paragraph("• <b>Short-Term Disability (STD):</b> 60% of salary for up to 90 days after 7-day waiting period", bullet_style))
    elements.append(Paragraph("• <b>Long-Term Disability (LTD):</b> 60% of salary after 90 days, up to age 65 or recovery", bullet_style))
    elements.append(Paragraph("• <b>Coverage:</b> Protects your income in case of illness or injury preventing work", bullet_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Employee Assistance Program (EAP)", heading2_style))
    elements.append(Paragraph(
        "Free, confidential counseling and support services are available 24/7 to all employees "
        "and their immediate family members. The EAP provides:",
        body_style
    ))
    elements.append(Paragraph("• Up to 6 free counseling sessions per issue per year", bullet_style))
    elements.append(Paragraph("• Mental health and emotional wellbeing support", bullet_style))
    elements.append(Paragraph("• Legal and financial consultation services", bullet_style))
    elements.append(Paragraph("• Work-life balance resources and referrals", bullet_style))
    elements.append(Paragraph("• Crisis intervention and support", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "All EAP services are completely confidential. Contact information: 1-800-EAP-HELP",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 5: PROFESSIONAL DEVELOPMENT
    # =========================
    elements.append(Paragraph("Section 5: Professional Development", heading1_style))

    elements.append(Paragraph(
        "TechCorp Solutions Inc. believes in investing in our employees' growth and development. "
        "We offer numerous opportunities and resources to help you advance your skills and career.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Annual Learning Budget", heading2_style))
    elements.append(Paragraph(
        "Every full-time employee receives a $2,000 annual learning and development budget. "
        "This budget can be used for:",
        body_style
    ))
    elements.append(Paragraph("• Online courses and training platforms (Udemy, Coursera, LinkedIn Learning, etc.)", bullet_style))
    elements.append(Paragraph("• Technical books and educational materials", bullet_style))
    elements.append(Paragraph("• Professional workshops and seminars", bullet_style))
    elements.append(Paragraph("• Industry certifications and exam fees", bullet_style))
    elements.append(Paragraph("• Conference registrations and attendance", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Unused budget does not roll over to the following year. Submit requests through the "
        "employee portal with manager approval.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Conference Attendance", heading2_style))
    elements.append(Paragraph(
        "TechCorp supports attendance at 1-2 industry conferences per year (subject to manager "
        "approval and business needs). Conference attendance may cover:",
        body_style
    ))
    elements.append(Paragraph("• Registration fees (covered by learning budget or separate approval)", bullet_style))
    elements.append(Paragraph("• Travel and accommodation expenses (company-paid, separate from learning budget)", bullet_style))
    elements.append(Paragraph("• Meals and incidentals per company travel policy", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Employees attending conferences are encouraged to share key learnings with their teams "
        "upon return through presentations or written summaries.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Certification Reimbursement", heading2_style))
    elements.append(Paragraph(
        "TechCorp provides 100% reimbursement for job-related professional certifications upon "
        "successful completion. This includes:",
        body_style
    ))
    elements.append(Paragraph("• Exam and testing fees", bullet_style))
    elements.append(Paragraph("• Study materials and prep courses", bullet_style))
    elements.append(Paragraph("• Certification renewal fees", bullet_style))
    elements.append(Paragraph("• Training required for certification eligibility", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Examples of supported certifications: AWS Solutions Architect, PMP, CPA, CISSP, "
        "Certified ScrumMaster, and other industry-recognized credentials relevant to your role.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Internal Training Programs", heading2_style))
    elements.append(Paragraph(
        "TechCorp offers various internal training opportunities at no cost to employees:",
        body_style
    ))
    elements.append(Paragraph("• Monthly lunch-and-learn sessions on technical and professional topics", bullet_style))
    elements.append(Paragraph("• Leadership development program for managers and aspiring leaders", bullet_style))
    elements.append(Paragraph("• Technical skills workshops (coding, cloud technologies, data science, etc.)", bullet_style))
    elements.append(Paragraph("• Soft skills training (communication, presentation, time management)", bullet_style))
    elements.append(Paragraph("• Diversity, equity, and inclusion training", bullet_style))
    elements.append(Paragraph("• New technology demos and knowledge sharing sessions", bullet_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Tuition Assistance", heading2_style))
    elements.append(Paragraph(
        "Employees pursuing undergraduate or graduate degrees at accredited institutions may be "
        "eligible for tuition assistance:",
        body_style
    ))
    elements.append(Paragraph("• <b>Coverage:</b> Up to 50% of tuition costs, maximum $5,000 per calendar year", bullet_style))
    elements.append(Paragraph("• <b>Eligibility:</b> Must be employed for at least 1 year and in good standing", bullet_style))
    elements.append(Paragraph("• <b>Grade Requirement:</b> Must maintain a B average or higher", bullet_style))
    elements.append(Paragraph("• <b>Approval:</b> Program must be relevant to current role or career progression at TechCorp", bullet_style))
    elements.append(Paragraph("• <b>Commitment:</b> Employees must remain with company for 2 years after completion or repay benefits", bullet_style))

    elements.append(PageBreak())

    # =========================
    # SECTION 6: PERFORMANCE REVIEWS
    # =========================
    elements.append(Paragraph("Section 6: Performance Reviews", heading1_style))

    elements.append(Paragraph(
        "TechCorp has a structured performance management process designed to provide regular "
        "feedback, recognize achievements, identify development opportunities, and ensure alignment "
        "with company goals.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Quarterly Check-ins", heading2_style))
    elements.append(Paragraph(
        "All employees participate in quarterly one-on-one check-ins with their direct manager. "
        "These are informal conversations focused on:",
        body_style
    ))
    elements.append(Paragraph("• Progress on current goals and projects", bullet_style))
    elements.append(Paragraph("• Challenges and roadblocks", bullet_style))
    elements.append(Paragraph("• Development needs and learning opportunities", bullet_style))
    elements.append(Paragraph("• Career aspirations and growth paths", bullet_style))
    elements.append(Paragraph("• Feedback (both directions)", bullet_style))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Annual Performance Review Cycle", heading2_style))
    elements.append(Paragraph(
        "Formal annual performance reviews are conducted each January-February for the previous "
        "calendar year. The process includes:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    review_timeline = [
        ["Phase", "Timeline", "Activities"],
        ["Self-Assessment", "Early January", "Employees complete self-evaluation reflecting on accomplishments, challenges, and goals"],
        ["360 Feedback", "Mid January", "Peers, direct reports (if applicable), and cross-functional partners provide feedback"],
        ["Manager Review", "Late January", "Manager completes performance evaluation and rating"],
        ["Calibration", "Early February", "Leadership team reviews ratings for consistency and fairness"],
        ["Review Meeting", "Mid February", "Manager and employee meet to discuss review, rating, and development plan"],
        ["Goal Setting", "Late February", "New goals established for upcoming year"]
    ]

    review_table = Table(review_timeline, colWidths=[1.3*inch, 1.2*inch, 4*inch])
    review_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CORPORATE_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white, LIGHT_GRAY, white, LIGHT_GRAY])
    ]))

    elements.append(review_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("360-Degree Feedback Process", heading2_style))
    elements.append(Paragraph(
        "TechCorp uses a 360-degree feedback approach where employees receive input from multiple "
        "perspectives. Feedback providers are selected by the employee and manager and typically include:",
        body_style
    ))
    elements.append(Paragraph("• Direct manager (required)", bullet_style))
    elements.append(Paragraph("• 3-5 peers and colleagues", bullet_style))
    elements.append(Paragraph("• Direct reports (for managers)", bullet_style))
    elements.append(Paragraph("• Cross-functional partners or stakeholders", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "All feedback is collected confidentially and aggregated to provide comprehensive insights "
        "while protecting individual anonymity.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Goal Setting - SMART Goals", heading2_style))
    elements.append(Paragraph(
        "All performance goals should follow the SMART framework:",
        body_style
    ))
    elements.append(Paragraph("• <b>Specific:</b> Clear and well-defined, not vague", bullet_style))
    elements.append(Paragraph("• <b>Measurable:</b> Quantifiable outcomes or success criteria", bullet_style))
    elements.append(Paragraph("• <b>Achievable:</b> Realistic and attainable given resources and constraints", bullet_style))
    elements.append(Paragraph("• <b>Relevant:</b> Aligned with team and company objectives", bullet_style))
    elements.append(Paragraph("• <b>Time-bound:</b> Has a clear deadline or timeframe", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Employees typically set 3-5 major goals for the year, reviewed and adjusted during "
        "quarterly check-ins as needed.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Performance Rating Scale", heading2_style))
    elements.append(Paragraph(
        "Performance is evaluated on a 5-point scale:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    rating_data = [
        ["Rating", "Level", "Description"],
        ["5", "Exceptional", "Consistently exceeds expectations in all areas. Delivers outstanding results that significantly impact the organization. Demonstrates leadership and innovation."],
        ["4", "Exceeds\nExpectations", "Frequently exceeds expectations in most areas. Delivers high-quality work and often goes above and beyond core responsibilities."],
        ["3", "Meets\nExpectations", "Consistently meets all expectations and job requirements. Delivers solid, reliable performance. This is the expected standard for the role."],
        ["2", "Needs\nImprovement", "Meets some but not all expectations. Performance gaps identified that require improvement. Development plan created."],
        ["1", "Unsatisfactory", "Does not meet basic job requirements. Significant performance issues that must be addressed immediately. May result in performance improvement plan."]
    ]

    rating_table = Table(rating_data, colWidths=[0.6*inch, 1.2*inch, 4.7*inch])
    rating_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ]))

    elements.append(rating_table)
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Performance ratings are used to determine annual merit increases, bonuses, and "
        "promotion eligibility. Most employees receive a rating of 3 (Meets Expectations), "
        "which represents solid, successful performance.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 7: CAREER PROGRESSION
    # =========================
    elements.append(Paragraph("Section 7: Career Progression", heading1_style))

    elements.append(Paragraph(
        "TechCorp is committed to supporting employee career growth and providing clear pathways "
        "for advancement within the organization.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Promotion Criteria and Timelines", heading2_style))
    elements.append(Paragraph(
        "Promotions at TechCorp are based on demonstrated performance, skills growth, and business "
        "need—not just tenure. However, general guidelines for time-in-role expectations are:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    promotion_data = [
        ["Current Level", "Typical Time in Role", "Promotion Criteria"],
        ["Junior → Mid", "18-24 months", "• Demonstrates independence in core responsibilities\n• Takes on increasing complexity\n• Mentors newer team members\n• Consistently meets expectations"],
        ["Mid → Senior", "2-3 years", "• Operates autonomously with minimal oversight\n• Leads projects and initiatives\n• Makes significant technical/functional contributions\n• Demonstrates expertise in specialized areas"],
        ["Senior → Lead", "3-4 years", "• Provides technical/strategic leadership\n• Drives team and organizational outcomes\n• Mentors and develops others\n• Influences beyond immediate team"],
        ["Lead → Principal", "4-5 years", "• Recognized expert in domain\n• Drives company-wide initiatives\n• Shapes strategy and long-term direction\n• Develops organizational capabilities"]
    ]

    promotion_table = Table(promotion_data, colWidths=[1.3*inch, 1.3*inch, 3.9*inch])
    promotion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CORPORATE_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white, LIGHT_GRAY])
    ]))

    elements.append(promotion_table)
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "All promotions require manager recommendation, peer validation, and leadership approval. "
        "Promotion decisions are typically made during annual review cycles but may occur "
        "off-cycle for exceptional circumstances.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Career Ladder Frameworks", heading2_style))
    elements.append(Paragraph(
        "TechCorp maintains detailed career ladder frameworks for each job family (Engineering, "
        "Product, Design, Sales, Marketing, Operations, etc.). These frameworks outline:",
        body_style
    ))
    elements.append(Paragraph("• Expected skills and competencies at each level", bullet_style))
    elements.append(Paragraph("• Scope of responsibility and impact", bullet_style))
    elements.append(Paragraph("• Technical and behavioral expectations", bullet_style))
    elements.append(Paragraph("• Example projects and deliverables", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Career ladders are available on the company intranet and should be reviewed with your "
        "manager during performance conversations to understand expectations for advancement.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Internal Mobility and Transfers", heading2_style))
    elements.append(Paragraph(
        "TechCorp encourages internal mobility and cross-functional movement. Employees interested "
        "in exploring different roles or teams should:",
        body_style
    ))
    elements.append(Paragraph("• Discuss career interests with your current manager first", bullet_style))
    elements.append(Paragraph("• Have been in current role for at least 12 months (exceptions possible)", bullet_style))
    elements.append(Paragraph("• Be in good performance standing (meeting expectations or above)", bullet_style))
    elements.append(Paragraph("• Apply through the internal job posting system", bullet_style))
    elements.append(Paragraph("• Coordinate transition timeline with both current and prospective managers", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Internal candidates are given priority consideration for open positions. HR can provide "
        "guidance on the internal transfer process.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Succession Planning", heading2_style))
    elements.append(Paragraph(
        "TechCorp maintains succession plans for critical roles to ensure business continuity and "
        "provide development opportunities. High-potential employees may be identified as successors "
        "for key positions and will receive targeted development and exposure. Succession planning "
        "discussions happen annually at the leadership level and are confidential until transitions occur.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 8: LEAVE POLICIES
    # =========================
    elements.append(Paragraph("Section 8: Leave Policies", heading1_style))

    elements.append(Paragraph(
        "This section provides a summary of TechCorp's leave policies. For complete details, "
        "please refer to the Company Policy Handbook or contact Human Resources.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    leave_summary = [
        ["Leave Type", "Entitlement", "Notes"],
        ["Paid Time Off\n(PTO)", "• Junior/Mid: 15 days/year\n• Senior/Lead: 20 days/year\n• Principal: 25 days/year", "Accrues bi-weekly. Can rollover up to 5 days to next year. Must be approved by manager."],
        ["Sick Leave", "10 days per year", "Separate from PTO. Use for illness or medical appointments. Doctor's note required for 3+ consecutive days."],
        ["Holidays", "12 company holidays", "Includes New Year's, Memorial Day, Independence Day, Labor Day, Thanksgiving, Christmas, etc. Published annually."],
        ["Bereavement\nLeave", "3-5 paid days", "3 days for extended family, 5 days for immediate family (spouse, parent, child, sibling). Additional unpaid leave available."],
        ["Jury Duty", "Fully paid", "Full salary continuation for duration of jury service. Must provide jury summons documentation."],
        ["Military Leave", "As per law", "Unpaid leave for military service obligations. Position held per USERRA requirements."],
        ["Parental Leave", "See policy handbook", "12 weeks paid for birth/adoption. Gender-neutral policy. Additional unpaid leave available under FMLA."],
        ["Sabbatical", "4 weeks after 5 years", "Unpaid sabbatical available to employees with 5+ years tenure. Must be approved 6 months in advance."]
    ]

    leave_table = Table(leave_summary, colWidths=[1.2*inch, 2.2*inch, 3.1*inch])
    leave_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), CORPORATE_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white, LIGHT_GRAY, white, LIGHT_GRAY, white, LIGHT_GRAY])
    ]))

    elements.append(leave_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph(
        "All leave requests should be submitted through the employee portal with advance notice "
        "when possible. PTO requests require manager approval. Sick leave can be used immediately "
        "as needed with notification to your manager. For extended medical leave, FMLA or state "
        "leave laws may apply—contact HR for guidance.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 9: OFFBOARDING & RESIGNATION
    # =========================
    elements.append(Paragraph("Section 9: Offboarding & Resignation", heading1_style))

    elements.append(Paragraph(
        "When you decide to leave TechCorp Solutions Inc., we want to ensure a smooth transition "
        "for you, your team, and the company. This section outlines the offboarding process and "
        "your responsibilities.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Notice Period Requirements", heading2_style))
    elements.append(Paragraph(
        "Professional courtesy and business continuity require adequate notice when resigning. "
        "Required notice periods by role level:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    notice_data = [
        ["Role Level", "Required Notice", "Rationale"],
        ["Individual\nContributor", "2 weeks (10 business days)", "Standard notice period allowing for knowledge transfer and immediate task handoff"],
        ["Manager/Lead", "4 weeks (20 business days)", "Additional time needed for team transition, responsibilities redistribution, and hiring planning"],
        ["Executive/\nSenior Leader", "8 weeks (40 business days)", "Extended notice for strategic planning, stakeholder transition, and succession planning"]
    ]

    notice_table = Table(notice_data, colWidths=[1.3*inch, 2*inch, 3.2*inch])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white])
    ]))

    elements.append(notice_table)
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Resignations should be submitted in writing (email acceptable) to your direct manager "
        "and copied to Human Resources. While we understand that circumstances vary, providing "
        "adequate notice helps maintain positive professional relationships.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Exit Interview Process", heading2_style))
    elements.append(Paragraph(
        "All departing employees are invited to participate in a confidential exit interview with "
        "Human Resources. This is an opportunity to:",
        body_style
    ))
    elements.append(Paragraph("• Share feedback about your experience at TechCorp", bullet_style))
    elements.append(Paragraph("• Discuss reasons for leaving", bullet_style))
    elements.append(Paragraph("• Provide suggestions for company improvement", bullet_style))
    elements.append(Paragraph("• Ask questions about the separation process", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Exit interviews are typically conducted during your final week and help us continuously "
        "improve our workplace culture and practices. Your honest feedback is valued and appreciated.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Final Paycheck Timing", heading2_style))
    elements.append(Paragraph(
        "Your final paycheck will include:",
        body_style
    ))
    elements.append(Paragraph("• Salary/wages through your last day of work", bullet_style))
    elements.append(Paragraph("• Payout of accrued, unused PTO (up to maximum rollover limit)", bullet_style))
    elements.append(Paragraph("• Any outstanding expense reimbursements", bullet_style))
    elements.append(Paragraph("• Prorated bonus if applicable and eligible", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Final paychecks are issued on the next regularly scheduled payday following your "
        "termination date or as required by state law. Deductions may include unreturned "
        "equipment, outstanding loans, or other authorized deductions.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Benefits Continuation (COBRA)", heading2_style))
    elements.append(Paragraph(
        "Under federal COBRA law, you and your covered dependents may continue health insurance "
        "coverage for up to 18 months after employment ends. Important details:",
        body_style
    ))
    elements.append(Paragraph("• Coverage continues at your expense (both employee and employer portions plus 2% admin fee)", bullet_style))
    elements.append(Paragraph("• You will receive COBRA election materials within 14 days of separation", bullet_style))
    elements.append(Paragraph("• You have 60 days to elect COBRA coverage", bullet_style))
    elements.append(Paragraph("• Coverage is retroactive to your termination date if elected timely", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Other benefits (life insurance, disability, FSA) typically end on your last day of "
        "employment. Your 401(k) account remains yours—contact the plan administrator for options.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Return of Company Property", heading2_style))
    elements.append(Paragraph(
        "All company property must be returned on or before your last day of employment:",
        body_style
    ))
    elements.append(Paragraph("• Laptop, monitors, keyboards, and all computer equipment", bullet_style))
    elements.append(Paragraph("• Mobile phone and accessories (if company-provided)", bullet_style))
    elements.append(Paragraph("• Employee ID badge and building access cards", bullet_style))
    elements.append(Paragraph("• Company credit cards", bullet_style))
    elements.append(Paragraph("• Keys, parking passes, or other access devices", bullet_style))
    elements.append(Paragraph("• Any company documents, files, or proprietary information", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "IT will assist with data backup of personal files and email forwarding setup. Failure to "
        "return company property may result in deductions from your final paycheck as permitted by law.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Non-Disclosure and Non-Compete Agreements", heading2_style))
    elements.append(Paragraph(
        "Your obligations under any signed non-disclosure agreements (NDAs), confidentiality "
        "agreements, and non-compete agreements (where applicable and enforceable) continue after "
        "employment ends. This includes:",
        body_style
    ))
    elements.append(Paragraph("• Protecting TechCorp's confidential and proprietary information", bullet_style))
    elements.append(Paragraph("• Not soliciting TechCorp employees or clients (if applicable)", bullet_style))
    elements.append(Paragraph("• Honoring intellectual property assignments", bullet_style))
    elements.append(Paragraph("• Complying with any restrictive covenants in your employment agreement", bullet_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "Questions about post-employment obligations should be directed to Human Resources or "
        "Legal. We appreciate your continued professionalism and confidentiality.",
        body_style
    ))

    elements.append(PageBreak())

    # =========================
    # SECTION 10: EMPLOYEE RELATIONS
    # =========================
    elements.append(Paragraph("Section 10: Employee Relations", heading1_style))

    elements.append(Paragraph(
        "TechCorp Solutions Inc. is committed to maintaining a respectful, inclusive, and safe "
        "workplace for all employees. This section outlines resources and processes for addressing "
        "workplace concerns.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Grievance Procedure", heading2_style))
    elements.append(Paragraph(
        "If you have a workplace concern, complaint, or dispute, we encourage you to address it "
        "through the following steps:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>Step 1: Direct Communication</b>", body_style))
    elements.append(Paragraph(
        "When appropriate and comfortable, address the issue directly with the person involved. "
        "Many concerns can be resolved through respectful, direct conversation.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.05*inch))

    elements.append(Paragraph("<b>Step 2: Manager Involvement</b>", body_style))
    elements.append(Paragraph(
        "If direct communication doesn't resolve the issue or isn't appropriate, bring the concern "
        "to your direct manager. They can help mediate, provide guidance, or escalate as needed.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.05*inch))

    elements.append(Paragraph("<b>Step 3: Human Resources</b>", body_style))
    elements.append(Paragraph(
        "If your concern involves your manager or isn't resolved at the manager level, contact "
        "Human Resources. HR will investigate confidentially and work toward resolution.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.05*inch))

    elements.append(Paragraph("<b>Step 4: Executive Leadership</b>", body_style))
    elements.append(Paragraph(
        "For serious matters or if prior steps haven't resulted in resolution, you may escalate "
        "to executive leadership or the Chief People Officer.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Harassment and Discrimination Reporting", heading2_style))
    elements.append(Paragraph(
        "TechCorp has zero tolerance for harassment, discrimination, or retaliation of any kind. "
        "If you experience or witness harassment or discrimination based on:",
        body_style
    ))
    elements.append(Paragraph("• Race, color, national origin, or ethnicity", bullet_style))
    elements.append(Paragraph("• Sex, gender, gender identity, or gender expression", bullet_style))
    elements.append(Paragraph("• Sexual orientation", bullet_style))
    elements.append(Paragraph("• Religion or religious beliefs", bullet_style))
    elements.append(Paragraph("• Age", bullet_style))
    elements.append(Paragraph("• Disability or medical condition", bullet_style))
    elements.append(Paragraph("• Veteran or military status", bullet_style))
    elements.append(Paragraph("• Pregnancy or parental status", bullet_style))
    elements.append(Paragraph("• Any other protected characteristic", bullet_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>Report immediately to:</b>", body_style))
    elements.append(Paragraph("• Your manager or any manager", bullet_style))
    elements.append(Paragraph("• Human Resources: hr@techcorp.com or (555) 123-4567", bullet_style))
    elements.append(Paragraph("• Anonymous hotline: 1-800-ETHICS-1 (available 24/7)", bullet_style))
    elements.append(Paragraph("• Online reporting form: techcorp.com/ethics-report", bullet_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph(
        "All reports are taken seriously and investigated promptly and confidentially. Retaliation "
        "against anyone who reports in good faith is strictly prohibited and will result in "
        "disciplinary action up to and including termination.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("Whistleblower Protection", heading2_style))
    elements.append(Paragraph(
        "TechCorp encourages employees to report any suspected violations of law, regulations, "
        "company policies, or ethical standards. Protected disclosures include:",
        body_style
    ))
    elements.append(Paragraph("• Financial fraud or accounting irregularities", bullet_style))
    elements.append(Paragraph("• Violations of securities laws or regulations", bullet_style))
    elements.append(Paragraph("• Misuse of company assets or resources", bullet_style))
    elements.append(Paragraph("• Health and safety violations", bullet_style))
    elements.append(Paragraph("• Environmental violations", bullet_style))
    elements.append(Paragraph("• Violations of company policies or code of conduct", bullet_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph(
        "Employees who report suspected violations in good faith are protected from retaliation. "
        "Reports can be made anonymously through the ethics hotline or reporting portal. The "
        "company will investigate all reports and take appropriate action.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("HR Contact Information and Office Hours", heading2_style))
    elements.append(Paragraph(
        "The Human Resources team is here to support you. We're available for questions about "
        "benefits, policies, workplace concerns, or any other employment-related matters.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))

    contact_data = [
        ["Contact Method", "Details"],
        ["Email", "hr@techcorp.com (monitored during business hours)"],
        ["Phone", "(555) 123-4567"],
        ["Office Location", "Building A, 3rd Floor, Suite 300"],
        ["Office Hours", "Monday - Friday, 8:00 AM - 5:00 PM Pacific Time"],
        ["Emergency After-Hours", "(555) 123-9999 (urgent matters only)"],
        ["Employee Portal", "portal.techcorp.com/hr"],
        ["Anonymous Hotline", "1-800-ETHICS-1 (24/7)"]
    ]

    contact_table = Table(contact_data, colWidths=[2*inch, 4.5*inch])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY, white, LIGHT_GRAY, white, LIGHT_GRAY, white])
    ]))

    elements.append(contact_table)
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph(
        "HR team members are also available for walk-in appointments during office hours, though "
        "scheduling ahead is recommended for complex matters requiring extended time.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))

    # Closing statement
    elements.append(Paragraph("Thank You", heading2_style))
    elements.append(Paragraph(
        "Thank you for being part of the TechCorp Solutions Inc. team. This handbook is designed "
        "to support your success and answer common questions about working here. As our company "
        "grows and evolves, this handbook will be updated periodically. You'll be notified of any "
        "significant changes.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "We're excited to have you on this journey with us. If you have suggestions for improving "
        "this handbook or any of our policies and practices, please share them with Human Resources. "
        "Your feedback helps us create a better workplace for everyone.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "<b>Welcome to TechCorp!</b>",
        body_style
    ))

    # Build PDF
    doc.build(elements, canvasmaker=NumberedCanvas)

    return output_file


if __name__ == "__main__":
    try:
        pdf_path = create_hr_handbook()
        print(f"HR Handbook successfully created: {pdf_path}")
    except Exception as e:
        print(f"Error creating HR Handbook: {str(e)}")
        raise
