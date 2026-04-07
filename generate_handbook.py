"""
Company Policy Handbook PDF Generator for TechCorp Solutions Inc.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for adding page numbers"""
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
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        page = "Page %d of %d" % (self._pageNumber, page_count)
        self.drawRightString(7.5*inch, 0.5*inch, page)

def create_handbook():
    """Create the Company Policy Handbook PDF"""

    # Create the PDF
    pdf_path = r"D:\Whatsapp analyzer\documents\company_policy.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for the 'Flowable' objects
    story = []

    # Define custom styles
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#003366'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    # Subtitle style
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    # Heading 1 style
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    # Heading 2 style
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    # Body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )

    # Bullet style
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        leading=14
    )

    # ===== COVER PAGE =====
    story.append(Spacer(1, 1.5*inch))

    story.append(Paragraph("TECHCORP SOLUTIONS INC.", title_style))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("Company Policy Handbook",
                          ParagraphStyle('CoverSubtitle', parent=subtitle_style, fontSize=20)))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("2026",
                          ParagraphStyle('Year', parent=subtitle_style, fontSize=16)))
    story.append(Spacer(1, 1*inch))

    # Logo placeholder
    logo_box = Table([[Paragraph("[COMPANY LOGO]",
                                ParagraphStyle('Logo', parent=subtitle_style,
                                             textColor=colors.grey))]],
                     colWidths=[3*inch])
    logo_box.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, -1), 40),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
    ]))
    story.append(logo_box)

    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Effective: January 1, 2026", subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Version 1.0",
                          ParagraphStyle('Version', parent=subtitle_style, fontSize=10)))

    story.append(PageBreak())

    # ===== TABLE OF CONTENTS =====
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(Spacer(1, 0.2*inch))

    toc_data = [
        ["Section 1: Introduction", "3"],
        ["Section 2: Code of Conduct", "4"],
        ["Section 3: Annual Leave Policy", "5"],
        ["Section 4: Sick Leave Policy", "5"],
        ["Section 5: Parental Leave", "6"],
        ["Section 6: Public Holidays", "6"],
        ["Section 7: Work Hours and Attendance", "7"],
        ["Section 8: Performance Management", "8"],
        ["Section 9: Policy Violations", "8"],
        ["Section 10: Acknowledgment", "9"],
    ]

    toc_table = Table(toc_data, colWidths=[5.5*inch, 0.75*inch])
    toc_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(toc_table)

    story.append(PageBreak())

    # ===== SECTION 1: INTRODUCTION =====
    story.append(Paragraph("Section 1: Introduction", h1_style))

    story.append(Paragraph("Welcome Message from the CEO", h2_style))
    story.append(Paragraph(
        "Dear Team Members,<br/><br/>"
        "Welcome to TechCorp Solutions Inc. On behalf of the entire leadership team, "
        "I am delighted to have you as part of our organization. This handbook represents "
        "our commitment to fostering a workplace that values excellence, innovation, and mutual respect. "
        "Our success depends on each team member understanding and embracing the policies and values outlined herein. "
        "I encourage you to read this handbook carefully and refer to it whenever questions arise about our workplace policies.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Together, we will continue to build a company that we can all be proud of.<br/><br/>"
        "Sincerely,<br/>"
        "Michael Chen<br/>"
        "Chief Executive Officer",
        body_style
    ))

    story.append(Paragraph("Company Mission and Values", h2_style))
    story.append(Paragraph(
        "<b>Mission:</b> To deliver innovative technology solutions that empower businesses "
        "to achieve their full potential through cutting-edge software and exceptional service.",
        body_style
    ))
    story.append(Paragraph("<b>Core Values:</b>", body_style))
    story.append(Paragraph("• <b>Innovation:</b> We embrace creative thinking and continuously seek better solutions", bullet_style))
    story.append(Paragraph("• <b>Integrity:</b> We conduct business with honesty and transparency", bullet_style))
    story.append(Paragraph("• <b>Excellence:</b> We strive for the highest quality in everything we do", bullet_style))
    story.append(Paragraph("• <b>Collaboration:</b> We believe in the power of teamwork and mutual support", bullet_style))
    story.append(Paragraph("• <b>Customer Focus:</b> We prioritize our clients' success above all else", bullet_style))

    story.append(Paragraph("Purpose of This Handbook", h2_style))
    story.append(Paragraph(
        "This handbook serves as a comprehensive guide to TechCorp Solutions Inc.'s policies, procedures, "
        "and expectations. It is designed to help you understand your rights and responsibilities as an employee, "
        "and to ensure consistent application of company policies across all departments. While this handbook "
        "covers many important topics, it is not an exhaustive list of all company policies. If you have questions "
        "about any policy not covered here, please contact the Human Resources department.",
        body_style
    ))

    story.append(Paragraph("Policy Governance and Updates", h2_style))
    story.append(Paragraph(
        "TechCorp Solutions Inc. reserves the right to modify, amend, or terminate any policy, benefit, "
        "or practice described in this handbook at any time, with or without notice. When significant changes "
        "are made, employees will be notified via email and updated versions will be available on the company "
        "intranet. This handbook supersedes all previous employee handbooks and policy statements. "
        "The most current version is always maintained by the HR department and is dated on the cover page.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 2: CODE OF CONDUCT =====
    story.append(Paragraph("Section 2: Code of Conduct", h1_style))

    story.append(Paragraph("Professional Behavior Expectations", h2_style))
    story.append(Paragraph(
        "All employees are expected to conduct themselves in a professional manner that reflects positively "
        "on TechCorp Solutions Inc. This includes treating colleagues, clients, vendors, and visitors with "
        "respect and courtesy at all times. Employees should maintain a positive attitude, communicate effectively, "
        "and contribute to a collaborative work environment. Behavior that disrupts the workplace, including "
        "harassment, bullying, or discrimination of any kind, will not be tolerated.",
        body_style
    ))

    story.append(Paragraph("Dress Code", h2_style))
    story.append(Paragraph(
        "TechCorp Solutions Inc. maintains a business casual dress code to present a professional image "
        "to our clients and visitors while allowing employees to work comfortably.",
        body_style
    ))
    story.append(Paragraph("• <b>Monday through Thursday:</b> Business casual attire is required. This includes collared shirts, "
                          "blouses, slacks, skirts, and closed-toe shoes. Jeans are not permitted.", bullet_style))
    story.append(Paragraph("• <b>Casual Friday:</b> Employees may wear neat, clean casual clothing including jeans. "
                          "Athletic wear, shorts, flip-flops, and clothing with offensive graphics are not permitted.", bullet_style))
    story.append(Paragraph("• <b>Client Meetings:</b> Business professional attire is required for all external client meetings "
                          "regardless of the day of the week.", bullet_style))

    story.append(Paragraph("Workplace Respect and Inclusion", h2_style))
    story.append(Paragraph(
        "TechCorp Solutions Inc. is committed to maintaining a diverse and inclusive workplace free from "
        "discrimination and harassment. We value the unique perspectives and contributions of all employees "
        "regardless of race, color, religion, gender, gender identity, sexual orientation, national origin, "
        "age, disability, or veteran status. All employment decisions are made based on merit, qualifications, "
        "and business needs. Employees who believe they have experienced or witnessed discrimination or harassment "
        "should report it immediately to their manager or the HR department.",
        body_style
    ))

    story.append(Paragraph("Conflict of Interest Policy", h2_style))
    story.append(Paragraph(
        "Employees must avoid situations where personal interests conflict or appear to conflict with the "
        "interests of TechCorp Solutions Inc. This includes financial interests in competing companies, "
        "accepting employment or consulting arrangements with competitors or clients, and using company "
        "resources for personal gain. Employees must disclose any potential conflicts of interest in writing "
        "to their manager and the HR department. The company will review each situation individually to "
        "determine appropriate action.",
        body_style
    ))

    story.append(Paragraph("Gifts and Entertainment", h2_style))
    story.append(Paragraph(
        "Employees may accept or provide modest gifts and entertainment in the normal course of business, "
        "provided they do not create an obligation or appearance of impropriety. The following guidelines apply:",
        body_style
    ))
    story.append(Paragraph("• Individual gifts or entertainment valued at <b>$50 or less per instance</b> are generally acceptable", bullet_style))
    story.append(Paragraph("• Gifts or entertainment exceeding $50 must be reported to your manager and approved in advance", bullet_style))
    story.append(Paragraph("• Cash or cash equivalents (gift cards) may never be accepted under any circumstances", bullet_style))
    story.append(Paragraph("• All gifts and entertainment must be accurately recorded in expense reports", bullet_style))

    story.append(Paragraph("Social Media Guidelines", h2_style))
    story.append(Paragraph(
        "While TechCorp Solutions Inc. respects employees' rights to participate in social media, employees "
        "must exercise good judgment and follow these guidelines:",
        body_style
    ))
    story.append(Paragraph("• Do not post confidential company information, trade secrets, or client data", bullet_style))
    story.append(Paragraph("• Make it clear that your views are your own and do not represent the company", bullet_style))
    story.append(Paragraph("• Be respectful and professional in all posts mentioning the company or colleagues", bullet_style))
    story.append(Paragraph("• Do not use company logos or trademarks without prior approval from Marketing", bullet_style))
    story.append(Paragraph("• Report any negative or concerning social media posts about the company to your manager", bullet_style))

    story.append(PageBreak())

    # ===== SECTION 3: ANNUAL LEAVE POLICY =====
    story.append(Paragraph("Section 3: Annual Leave Policy", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. recognizes the importance of work-life balance and provides annual leave "
        "to allow employees to rest, recharge, and attend to personal matters. All regular full-time employees "
        "are eligible for annual leave as outlined below.",
        body_style
    ))

    story.append(Paragraph("Annual Leave Entitlement", h2_style))
    leave_table_data = [
        ["Employee Category", "Years of Service", "Annual Leave Days"],
        ["Standard", "0-3 years", "15 days per year"],
        ["Senior", "3+ years", "20 days per year"],
        ["Executive", "All levels", "25 days per year"],
    ]

    leave_table = Table(leave_table_data, colWidths=[2*inch, 1.75*inch, 2*inch])
    leave_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(leave_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Leave Accrual and Usage", h2_style))
    story.append(Paragraph("• <b>Accrual Rate:</b> Standard employees accrue 1.25 days per month of employment", bullet_style))
    story.append(Paragraph("• <b>Probation Period:</b> Leave accrues during probation but cannot be taken until completion of 90 days", bullet_style))
    story.append(Paragraph("• <b>Maximum Carryover:</b> Employees may carry over a maximum of 5 unused days to the next calendar year", bullet_style))
    story.append(Paragraph("• <b>Carryover Expiration:</b> Carried-over days must be used by March 31 or they will be forfeited", bullet_style))
    story.append(Paragraph("• <b>Payout:</b> Unused leave is not paid out during employment. Upon termination, accrued unused leave is paid at current base salary rate", bullet_style))

    story.append(Paragraph("Blackout Periods", h2_style))
    story.append(Paragraph(
        "To ensure adequate staffing during critical business periods, annual leave requests will generally "
        "not be approved during the following blackout periods:",
        body_style
    ))
    story.append(Paragraph("• Last week of March (Q1 fiscal close)", bullet_style))
    story.append(Paragraph("• Last week of June (Q2 fiscal close)", bullet_style))
    story.append(Paragraph("• Last week of September (Q3 fiscal close)", bullet_style))
    story.append(Paragraph("• Last week of December (Q4 fiscal close)", bullet_style))
    story.append(Paragraph(
        "Exceptions may be granted for emergency situations at the discretion of the department head and HR.",
        body_style
    ))

    story.append(Paragraph("Request Process", h2_style))
    story.append(Paragraph("• Submit leave requests through the HR portal at least <b>2 weeks in advance</b>", bullet_style))
    story.append(Paragraph("• Manager approval is required and must be provided within <b>3 business days</b> of request", bullet_style))
    story.append(Paragraph("• Emergency leave requests should be discussed directly with your manager as soon as possible", bullet_style))
    story.append(Paragraph("• Update your team calendar and arrange coverage for your responsibilities during absence", bullet_style))
    story.append(Paragraph("• Set up an out-of-office email response and voicemail message", bullet_style))

    story.append(PageBreak())

    # ===== SECTION 4: SICK LEAVE POLICY =====
    story.append(Paragraph("Section 4: Sick Leave Policy", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. provides sick leave to support employees when they need time off due to "
        "illness or medical appointments. We encourage employees to prioritize their health and take necessary "
        "time to recover fully before returning to work.",
        body_style
    ))

    story.append(Paragraph("Sick Leave Entitlement", h2_style))
    story.append(Paragraph("• All full-time employees receive <b>12 sick days per calendar year</b>", bullet_style))
    story.append(Paragraph("• Sick leave is available immediately upon hire (no waiting period)", bullet_style))
    story.append(Paragraph("• Part-time employees receive prorated sick leave based on scheduled hours", bullet_style))
    story.append(Paragraph("• <b>Unused sick leave does NOT carry over</b> to the following year", bullet_style))
    story.append(Paragraph("• Unused sick leave is not paid out upon termination", bullet_style))

    story.append(Paragraph("Medical Documentation Requirements", h2_style))
    story.append(Paragraph("• <b>1-2 consecutive days:</b> No doctor's note required", bullet_style))
    story.append(Paragraph("• <b>3+ consecutive days:</b> Doctor's note required upon return to work", bullet_style))
    story.append(Paragraph("• Chronic conditions: Employees may submit a single doctor's note covering ongoing intermittent absences", bullet_style))
    story.append(Paragraph("• Medical documentation should be submitted to HR (not your manager) to maintain privacy", bullet_style))

    story.append(Paragraph("Notification Requirements", h2_style))
    story.append(Paragraph(
        "To ensure proper staffing and workflow management, employees must follow these notification procedures:",
        body_style
    ))
    story.append(Paragraph("• Notify your direct manager <b>before 9:00 AM</b> on the first day of absence", bullet_style))
    story.append(Paragraph("• Notification should be by phone call or direct message (not email)", bullet_style))
    story.append(Paragraph("• Provide an estimated return date if known", bullet_style))
    story.append(Paragraph("• Update your manager daily if absence extends beyond initial estimate", bullet_style))
    story.append(Paragraph("• Log sick time in the HR portal within 24 hours of return", bullet_style))

    story.append(Paragraph("Return-to-Work Procedures", h2_style))
    story.append(Paragraph(
        "After an absence of <b>5 or more consecutive days</b>, employees are required to participate in a "
        "return-to-work meeting with their manager and HR. This meeting ensures the employee is fully recovered "
        "and discusses any accommodations that may be needed. The meeting is also an opportunity to catch up "
        "on any important developments that occurred during the absence.",
        body_style
    ))

    story.append(Paragraph("Sick Leave for Family Care", h2_style))
    story.append(Paragraph(
        "Sick leave may be used to care for an immediate family member (spouse, child, parent) who is ill. "
        "The same notification procedures and documentation requirements apply. If extended family care is needed, "
        "employees should discuss options with HR, including the possibility of unpaid leave or use of annual leave.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 5: PARENTAL LEAVE =====
    story.append(Paragraph("Section 5: Parental Leave", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. supports employees during important family milestones by providing paid "
        "parental leave for the birth or adoption of a child. We recognize that new parents need time to bond "
        "with their children and adjust to their new family dynamics.",
        body_style
    ))

    story.append(Paragraph("Parental Leave Entitlement", h2_style))
    parental_table_data = [
        ["Caregiver Category", "Paid Leave", "Eligibility"],
        ["Primary Caregiver", "12 weeks", "12+ months employment"],
        ["Secondary Caregiver", "4 weeks", "12+ months employment"],
    ]

    parental_table = Table(parental_table_data, colWidths=[2.25*inch, 1.75*inch, 2.25*inch])
    parental_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(parental_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph(
        "<b>Primary Caregiver Definition:</b> The parent who will have primary responsibility for the care of the child. "
        "This typically includes birth mothers and the primary adopting parent.<br/><br/>"
        "<b>Secondary Caregiver Definition:</b> The parent who will share caregiving responsibilities but is not the primary caregiver.",
        body_style
    ))

    story.append(Paragraph("Eligibility Requirements", h2_style))
    story.append(Paragraph("• Must be employed by TechCorp Solutions Inc. for at least <b>12 consecutive months</b>", bullet_style))
    story.append(Paragraph("• Must be a regular full-time employee (contractors and temporary staff are not eligible)", bullet_style))
    story.append(Paragraph("• Leave must be taken within 12 months of the child's birth or adoption placement", bullet_style))
    story.append(Paragraph("• Applies to birth parents, adoptive parents, and foster parents", bullet_style))

    story.append(Paragraph("Flexible Return Options", h2_style))
    story.append(Paragraph(
        "To support a gradual transition back to work, TechCorp Solutions Inc. offers flexible return options:",
        body_style
    ))
    story.append(Paragraph("• Employees may return to work <b>part-time for up to 4 weeks</b> following parental leave", bullet_style))
    story.append(Paragraph("• Part-time schedule must be approved by manager and HR in advance", bullet_style))
    story.append(Paragraph("• Minimum part-time schedule is 20 hours per week (50% of full-time)", bullet_style))
    story.append(Paragraph("• Pay during part-time transition is prorated based on hours worked", bullet_style))
    story.append(Paragraph("• Employee returns to full-time status and full pay after transition period", bullet_style))

    story.append(Paragraph("Notification Requirements", h2_style))
    story.append(Paragraph("• Provide written notice to HR at least <b>30 days before</b> the expected leave start date", bullet_style))
    story.append(Paragraph("• Submit the Parental Leave Request Form available on the HR portal", bullet_style))
    story.append(Paragraph("• Include expected leave start date and anticipated return date", bullet_style))
    story.append(Paragraph("• Update HR if dates change due to early delivery or other circumstances", bullet_style))
    story.append(Paragraph("• Schedule a pre-leave meeting with HR and your manager to discuss transition planning", bullet_style))

    story.append(Paragraph("Benefits During Leave", h2_style))
    story.append(Paragraph(
        "During paid parental leave, employees continue to receive full salary and benefits, including health "
        "insurance, dental insurance, and 401(k) matching. Leave time counts as service time for purposes of "
        "leave accrual and tenure calculations. Employees on parental leave are not expected to check email or "
        "perform work duties unless they specifically choose to do so.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 6: PUBLIC HOLIDAYS =====
    story.append(Paragraph("Section 6: Public Holidays", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. observes the following paid public holidays each year. All regular full-time "
        "and part-time employees are entitled to these holidays with pay. The company's offices are closed on "
        "these days unless otherwise notified.",
        body_style
    ))

    story.append(Paragraph("2026 Public Holiday Schedule", h2_style))

    holiday_table_data = [
        ["Holiday", "Date", "Day of Week"],
        ["New Year's Day", "January 1, 2026", "Thursday"],
        ["Martin Luther King Jr. Day", "January 20, 2026", "Monday"],
        ["Presidents' Day", "February 17, 2026", "Monday"],
        ["Memorial Day", "May 25, 2026", "Monday"],
        ["Independence Day", "July 4, 2026", "Saturday"],
        ["Independence Day (Observed)", "July 6, 2026", "Monday"],
        ["Labor Day", "September 7, 2026", "Monday"],
        ["Thanksgiving Day", "November 26, 2026", "Thursday"],
        ["Day After Thanksgiving", "November 27, 2026", "Friday"],
        ["Christmas Day", "December 25, 2026", "Friday"],
    ]

    holiday_table = Table(holiday_table_data, colWidths=[2.5*inch, 2*inch, 1.75*inch])
    holiday_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    story.append(holiday_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Holiday Policies", h2_style))
    story.append(Paragraph(
        "<b>Weekend Observance:</b> When a holiday falls on a Saturday, it will be observed on the preceding Friday. "
        "When a holiday falls on a Sunday, it will be observed on the following Monday. This ensures that all "
        "employees receive the full benefit of the holiday regardless of their work schedule.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Holiday Pay:</b> Non-exempt employees receive their regular rate of pay for holidays. Exempt employees "
        "receive their regular salary. Employees who are required to work on a company holiday (with prior approval) "
        "will receive holiday pay plus time-and-a-half for hours worked.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Part-Time Employees:</b> Part-time employees receive holiday pay prorated based on their regular "
        "scheduled hours. For example, an employee who regularly works 20 hours per week would receive 4 hours "
        "of holiday pay for each observed holiday.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "<b>Holidays During Leave:</b> Employees on approved leave (annual leave, sick leave, parental leave) "
        "during a company holiday will receive holiday pay and the holiday will not count against their leave balance.",
        body_style
    ))

    story.append(Paragraph("Floating Holidays", h2_style))
    story.append(Paragraph(
        "In addition to the standard public holidays listed above, each employee receives <b>2 floating holidays</b> "
        "per calendar year. These can be used for religious observances, cultural celebrations, or personal days of "
        "significance. Floating holidays must be requested at least 1 week in advance and are subject to manager approval. "
        "Unused floating holidays do not carry over to the next year.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 7: WORK HOURS AND ATTENDANCE =====
    story.append(Paragraph("Section 7: Work Hours and Attendance", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. values both productivity and work-life balance. Our work hours policy is designed "
        "to provide structure while offering some flexibility to accommodate different working styles and personal needs.",
        body_style
    ))

    story.append(Paragraph("Standard Work Hours", h2_style))
    story.append(Paragraph("• <b>Standard Schedule:</b> 9:00 AM to 6:00 PM, Monday through Friday", bullet_style))
    story.append(Paragraph("• <b>Total Hours:</b> 8 hours of work + 1 hour unpaid lunch break = 9 hours on-site", bullet_style))
    story.append(Paragraph("• <b>Weekly Hours:</b> 40 hours per week for full-time employees", bullet_style))
    story.append(Paragraph("• <b>Lunch Break:</b> All employees must take a minimum 30-minute lunch break (1 hour recommended)", bullet_style))

    story.append(Paragraph("Core Hours and Flexible Start Time", h2_style))
    story.append(Paragraph(
        "To provide flexibility while ensuring collaboration, TechCorp Solutions Inc. has implemented core hours:",
        body_style
    ))
    story.append(Paragraph("• <b>Core Hours:</b> 10:00 AM to 4:00 PM - all employees must be present or available", bullet_style))
    story.append(Paragraph("• <b>Flexible Start:</b> Employees may start any time between 8:00 AM and 10:00 AM", bullet_style))
    story.append(Paragraph("• <b>Corresponding End Time:</b> If starting at 8:00 AM, may leave at 5:00 PM (after 8 hours + lunch)", bullet_style))
    story.append(Paragraph("• <b>Consistency Expected:</b> While flexible start is allowed, employees should maintain a generally consistent schedule", bullet_style))
    story.append(Paragraph("• <b>Team Meetings:</b> Must be scheduled within core hours unless all attendees agree otherwise", bullet_style))

    story.append(Paragraph("Time Tracking Requirements", h2_style))
    story.append(Paragraph(
        "Accurate time tracking is mandatory for all employees, both exempt and non-exempt:",
        body_style
    ))
    story.append(Paragraph("• Use the company time tracking system to clock in at start of work day", bullet_style))
    story.append(Paragraph("• Clock out for lunch break and clock back in when returning", bullet_style))
    story.append(Paragraph("• Clock out at end of work day", bullet_style))
    story.append(Paragraph("• Submit timesheets by end of day Friday for weekly review", bullet_style))
    story.append(Paragraph("• Managers review and approve timesheets by Monday 5:00 PM", bullet_style))
    story.append(Paragraph("• Falsifying time records is grounds for immediate termination", bullet_style))

    story.append(Paragraph("Punctuality and Attendance Expectations", h2_style))
    story.append(Paragraph(
        "Regular attendance and punctuality are essential to TechCorp Solutions Inc.'s operations. "
        "Employees are expected to:",
        body_style
    ))
    story.append(Paragraph("• Arrive on time for their scheduled or self-selected start time", bullet_style))
    story.append(Paragraph("• Be prepared to begin work at start time (not just arriving at building)", bullet_style))
    story.append(Paragraph("• Attend all scheduled meetings on time", bullet_style))
    story.append(Paragraph("• Return from lunch breaks on time", bullet_style))
    story.append(Paragraph("• Notify manager immediately if running late due to unforeseen circumstances", bullet_style))

    story.append(Paragraph("Late Arrival Policy", h2_style))
    story.append(Paragraph(
        "While we understand that occasional delays are unavoidable, consistent tardiness affects team "
        "productivity and morale. The following progressive approach applies:",
        body_style
    ))
    story.append(Paragraph("• <b>First and Second Occurrence:</b> Verbal reminder from manager", bullet_style))
    story.append(Paragraph("• <b>Third Occurrence in 30 days:</b> Written warning issued and placed in employee file", bullet_style))
    story.append(Paragraph("• <b>Fourth Occurrence in 30 days:</b> Final written warning and meeting with HR", bullet_style))
    story.append(Paragraph("• <b>Fifth Occurrence in 30 days:</b> Termination may be considered", bullet_style))
    story.append(Paragraph(
        "Note: Arriving more than 15 minutes late without prior notice is considered a late arrival. "
        "Emergency situations are handled on a case-by-case basis.",
        body_style
    ))

    story.append(Paragraph("Remote Work Policy", h2_style))
    story.append(Paragraph(
        "TechCorp Solutions Inc. supports occasional remote work on a case-by-case basis. Employees must request "
        "remote work approval from their manager at least 24 hours in advance. During remote work days, employees "
        "must be available during core hours, attend all scheduled meetings via video conference, and maintain "
        "normal productivity levels. Regular remote work arrangements (e.g., 1-2 days per week) require formal "
        "approval from department head and HR.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 8: PERFORMANCE MANAGEMENT =====
    story.append(Paragraph("Section 8: Performance Management", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. is committed to supporting employee growth and success through regular feedback "
        "and structured performance evaluations. Our performance management process is designed to recognize "
        "achievements, identify development opportunities, and align individual goals with company objectives.",
        body_style
    ))

    story.append(Paragraph("Performance Review Cycle", h2_style))
    story.append(Paragraph("• <b>Quarterly Reviews:</b> Brief check-ins held in March, June, September, and December", bullet_style))
    story.append(Paragraph("• <b>Annual Comprehensive Review:</b> Detailed evaluation conducted each March", bullet_style))
    story.append(Paragraph("• <b>New Employee Reviews:</b> 30-day, 60-day, and 90-day check-ins during probationary period", bullet_style))
    story.append(Paragraph("• <b>Ongoing Feedback:</b> Managers are encouraged to provide real-time feedback throughout the year", bullet_style))

    story.append(Paragraph("Performance Rating Scale", h2_style))
    story.append(Paragraph(
        "TechCorp Solutions Inc. uses a 5-point rating scale for performance evaluations:",
        body_style
    ))

    rating_table_data = [
        ["Rating", "Label", "Description"],
        ["5", "Exceptional", "Consistently exceeds expectations in all areas; demonstrates leadership"],
        ["4", "Exceeds Expectations", "Frequently surpasses goals; produces high-quality work"],
        ["3", "Meets Expectations", "Reliably achieves goals; performs all duties satisfactorily"],
        ["2", "Needs Improvement", "Occasionally falls short of expectations; requires additional support"],
        ["1", "Unsatisfactory", "Consistently fails to meet minimum requirements"],
    ]

    rating_table = Table(rating_table_data, colWidths=[0.75*inch, 1.75*inch, 3.75*inch])
    rating_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
    ]))
    story.append(rating_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Annual Compensation Review", h2_style))
    story.append(Paragraph(
        "Each year in March, TechCorp Solutions Inc. conducts a comprehensive compensation review for all employees. "
        "This review considers performance ratings, market data, internal equity, and budget constraints. Salary "
        "adjustments and bonuses are determined based on these factors and are typically effective April 1st. "
        "Employees rated 3 or higher are eligible for merit increases. The compensation review is separate from, "
        "but informed by, the annual performance review.",
        body_style
    ))

    story.append(Paragraph("Performance Improvement Plans (PIP)", h2_style))
    story.append(Paragraph(
        "Employees who receive a performance rating below 3 (Meets Expectations) may be placed on a Performance "
        "Improvement Plan. A PIP is a structured program designed to help employees improve performance through:",
        body_style
    ))
    story.append(Paragraph("• Clearly defined performance deficiencies and improvement goals", bullet_style))
    story.append(Paragraph("• Specific, measurable objectives to be achieved within 60-90 days", bullet_style))
    story.append(Paragraph("• Regular check-ins with manager (typically weekly or bi-weekly)", bullet_style))
    story.append(Paragraph("• Additional training, resources, or support as needed", bullet_style))
    story.append(Paragraph("• Documentation of progress and any ongoing concerns", bullet_style))
    story.append(Paragraph(
        "At the end of the PIP period, performance is reassessed. Successful completion results in return to good "
        "standing. Failure to improve may result in demotion, reassignment, or termination.",
        body_style
    ))

    story.append(Paragraph("Promotion Criteria and Process", h2_style))
    story.append(Paragraph(
        "TechCorp Solutions Inc. is committed to promoting from within when possible. Promotions are based on:",
        body_style
    ))
    story.append(Paragraph("• Demonstrated performance exceeding current role requirements", bullet_style))
    story.append(Paragraph("• Readiness to assume responsibilities of the target position", bullet_style))
    story.append(Paragraph("• Availability of the position and budget approval", bullet_style))
    story.append(Paragraph("• Minimum of 12 months in current role (exceptions for exceptional circumstances)", bullet_style))
    story.append(Paragraph("• Performance rating of 4 or 5 in most recent annual review", bullet_style))
    story.append(Paragraph(
        "Promotions are typically announced during the annual compensation review period in March, with some "
        "exceptions made throughout the year for business-critical needs.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 9: POLICY VIOLATIONS =====
    story.append(Paragraph("Section 9: Policy Violations", h1_style))

    story.append(Paragraph(
        "TechCorp Solutions Inc. expects all employees to adhere to the policies outlined in this handbook and "
        "to conduct themselves in a professional manner. When policy violations occur, the company will take "
        "appropriate corrective action to address the behavior and prevent recurrence.",
        body_style
    ))

    story.append(Paragraph("Progressive Discipline Process", h2_style))
    story.append(Paragraph(
        "For most policy violations, TechCorp Solutions Inc. follows a progressive discipline approach that "
        "provides employees with opportunities to correct their behavior:",
        body_style
    ))

    story.append(Paragraph("<b>Step 1: Verbal Warning</b>", h2_style))
    story.append(Paragraph(
        "For a first-time or minor violation, the manager will have a private conversation with the employee to "
        "discuss the issue, explain the relevant policy, and clarify expectations. This conversation is documented "
        "by the manager but typically not placed in the employee's formal file.",
        body_style
    ))

    story.append(Paragraph("<b>Step 2: Written Warning</b>", h2_style))
    story.append(Paragraph(
        "If the behavior continues or for more serious violations, a formal written warning is issued. The warning "
        "document details the violation, references previous discussions, states expected corrective actions, and "
        "outlines potential consequences of continued violations. The employee signs the written warning to "
        "acknowledge receipt (signature does not indicate agreement), and it is placed in the employee's personnel file.",
        body_style
    ))

    story.append(Paragraph("<b>Step 3: Final Written Warning</b>", h2_style))
    story.append(Paragraph(
        "For repeated violations or serious misconduct, a final written warning is issued. This document clearly "
        "states that the employee's job is in jeopardy and that any further violations may result in immediate "
        "termination. A meeting is held with the employee, their manager, and an HR representative. The employee "
        "is given a specific timeframe (typically 30 days) to demonstrate sustained improvement.",
        body_style
    ))

    story.append(Paragraph("<b>Step 4: Termination</b>", h2_style))
    story.append(Paragraph(
        "If violations continue after a final written warning, or if the employee fails to demonstrate the required "
        "improvement, employment may be terminated. The decision to terminate is made by the department head in "
        "consultation with HR and is documented thoroughly. In some cases, the employee may be offered the option "
        "to resign in lieu of termination.",
        body_style
    ))

    story.append(Paragraph("Gross Misconduct - Immediate Termination", h2_style))
    story.append(Paragraph(
        "Certain behaviors are considered gross misconduct and may result in immediate termination without "
        "progressive discipline. These include, but are not limited to:",
        body_style
    ))
    story.append(Paragraph("• Theft of company or employee property", bullet_style))
    story.append(Paragraph("• Violence, threats of violence, or intimidation", bullet_style))
    story.append(Paragraph("• Harassment or discrimination based on protected characteristics", bullet_style))
    story.append(Paragraph("• Intentional disclosure of confidential or proprietary information", bullet_style))
    story.append(Paragraph("• Falsification of company records, including timesheets or expense reports", bullet_style))
    story.append(Paragraph("• Being under the influence of alcohol or illegal drugs at work", bullet_style))
    story.append(Paragraph("• Gross insubordination or refusal to perform assigned duties", bullet_style))
    story.append(Paragraph("• Sabotage of company equipment, systems, or data", bullet_style))

    story.append(Paragraph("Investigation Process", h2_style))
    story.append(Paragraph(
        "When a serious policy violation is alleged, TechCorp Solutions Inc. will conduct a prompt and thorough "
        "investigation. During the investigation, the employee may be placed on paid administrative leave. The "
        "investigation will include interviews with relevant parties, review of documentation, and examination of "
        "any physical or electronic evidence. Employees are expected to cooperate fully with investigations. "
        "Failure to cooperate may itself be grounds for discipline.",
        body_style
    ))

    story.append(Paragraph("Appeal Process", h2_style))
    story.append(Paragraph(
        "Employees who believe they have been disciplined unfairly have the right to appeal. The appeal process is:",
        body_style
    ))
    story.append(Paragraph("• Submit a written appeal to HR within <b>5 business days</b> of receiving the disciplinary action", bullet_style))
    story.append(Paragraph("• Include specific reasons why the discipline should be overturned or reduced", bullet_style))
    story.append(Paragraph("• HR will review the appeal and may request additional information or meetings", bullet_style))
    story.append(Paragraph("• A decision will be rendered within 10 business days of receiving the appeal", bullet_style))
    story.append(Paragraph("• The HR Director's decision on the appeal is final", bullet_style))
    story.append(Paragraph(
        "Note: Filing an appeal does not suspend the disciplinary action. The original discipline remains in effect "
        "during the appeal process unless HR specifically grants a stay.",
        body_style
    ))

    story.append(PageBreak())

    # ===== SECTION 10: ACKNOWLEDGMENT =====
    story.append(Paragraph("Section 10: Employee Acknowledgment", h1_style))

    story.append(Paragraph(
        "This acknowledgment form confirms that you have received the TechCorp Solutions Inc. Company Policy Handbook "
        "and understand your responsibilities as an employee.",
        body_style
    ))

    story.append(Spacer(1, 0.3*inch))

    # Create acknowledgment form
    story.append(Paragraph("Employee Acknowledgment and Agreement", h2_style))

    story.append(Paragraph(
        "I acknowledge that I have received a copy of the TechCorp Solutions Inc. Company Policy Handbook dated "
        "January 1, 2026. I understand that it is my responsibility to read and familiarize myself with the policies "
        "and procedures contained in this handbook.",
        body_style
    ))

    story.append(Paragraph(
        "I understand that this handbook is not a contract of employment and that employment with TechCorp Solutions Inc. "
        "is at-will, meaning that either the company or I may terminate the employment relationship at any time, "
        "with or without cause or notice, unless otherwise specified in a written employment contract.",
        body_style
    ))

    story.append(Paragraph(
        "I understand that TechCorp Solutions Inc. reserves the right to modify, supplement, rescind, or revise any "
        "policies, procedures, or benefits described in this handbook as it deems necessary, with or without notice. "
        "I will be notified of significant changes and updated versions will be made available.",
        body_style
    ))

    story.append(Paragraph(
        "I understand that if I have questions about any policies or procedures, I should consult with my manager "
        "or the Human Resources department for clarification.",
        body_style
    ))

    story.append(Paragraph(
        "I agree to comply with all policies and procedures outlined in this handbook and understand that failure "
        "to do so may result in disciplinary action, up to and including termination of employment.",
        body_style
    ))

    story.append(Spacer(1, 0.4*inch))

    # Signature section
    signature_data = [
        ["", ""],
        ["Employee Name (Print):", "_" * 50],
        ["", ""],
        ["Employee Signature:", "_" * 50],
        ["", ""],
        ["Date:", "_" * 50],
        ["", ""],
        ["", ""],
        ["For HR Use Only:", ""],
        ["Received by HR:", "_" * 50],
        ["Date Received:", "_" * 50],
    ]

    signature_table = Table(signature_data, colWidths=[2*inch, 4*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(signature_table)

    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph("Human Resources Contact Information", h2_style))

    hr_contact_data = [
        ["HR Department:", "hr@techcorpsolutions.com"],
        ["Phone:", "(555) 123-4500"],
        ["Office Location:", "Floor 3, Room 301"],
        ["Office Hours:", "Monday - Friday, 9:00 AM - 5:00 PM"],
        ["HR Director:", "Jennifer Martinez"],
        ["Direct Line:", "(555) 123-4501"],
    ]

    hr_table = Table(hr_contact_data, colWidths=[2*inch, 4*inch])
    hr_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(hr_table)

    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph(
        "<i>Please sign and return this acknowledgment page to the HR department within 5 business days of "
        "receiving this handbook. A copy will be placed in your personnel file.</i>",
        ParagraphStyle('Footer', parent=body_style, fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    ))

    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph(
        "Thank you for taking the time to review this handbook. We look forward to working with you!",
        ParagraphStyle('ClosingText', parent=body_style, alignment=TA_CENTER, fontName='Helvetica-Bold')
    ))

    # Build the PDF with custom canvas for page numbers
    doc.build(story, canvasmaker=NumberedCanvas)

    print(f"Company Policy Handbook PDF created successfully at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_handbook()
