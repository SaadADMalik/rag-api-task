#!/usr/bin/env python3
"""
Generate TechCorp Solutions Inc. Expense & Travel Policy PDF
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime

def create_expense_policy_pdf(filename):
    """Create a comprehensive expense and travel policy PDF"""

    # Create document
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=50
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2c5282'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5282'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        leading=14
    )

    # ==================== COVER PAGE ====================
    elements.append(Spacer(1, 2*inch))

    elements.append(Paragraph("TechCorp Solutions Inc.", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Expense & Travel Policy", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("2026 Edition", subtitle_style))
    elements.append(Spacer(1, 1*inch))

    elements.append(Paragraph(f"Effective Date: January 1, 2026", ParagraphStyle(
        'Date',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER
    )))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Document Version: 1.0", ParagraphStyle(
        'Version',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER
    )))

    elements.append(PageBreak())

    # ==================== TABLE OF CONTENTS ====================
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    toc_items = [
        "1. Policy Overview",
        "2. Expense Categories",
        "3. Travel Arrangements",
        "4. Meals & Per Diem",
        "5. Approval Workflows",
        "6. Receipt Requirements",
        "7. Expense Submission",
        "8. Reimbursement Process",
        "9. Corporate Cards",
        "10. Violations & Consequences",
        "11. Contact Information"
    ]

    for item in toc_items:
        elements.append(Paragraph(item, bullet_style))

    elements.append(PageBreak())

    # ==================== SECTION 1: POLICY OVERVIEW ====================
    elements.append(Paragraph("Section 1: Policy Overview", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>1.1 Purpose and Scope</b>", heading2_style))
    elements.append(Paragraph(
        "This Expense & Travel Policy establishes guidelines for TechCorp Solutions Inc. employees "
        "when incurring business-related expenses. The policy applies to all full-time, part-time, "
        "and contract employees who are authorized to incur expenses on behalf of the company. "
        "The purpose of this policy is to ensure fair, consistent, and fiscally responsible expense "
        "management while enabling employees to conduct business effectively.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>1.2 Compliance Requirements</b>", heading2_style))
    elements.append(Paragraph(
        "All employees must comply with this policy when incurring business expenses. Failure to "
        "comply may result in denial of reimbursement, disciplinary action, or termination. This "
        "policy is designed to comply with IRS regulations, Generally Accepted Accounting Principles "
        "(GAAP), and internal audit requirements. Employees are responsible for understanding and "
        "following all provisions of this policy.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>1.3 Reimbursement Principles</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp Solutions Inc. will reimburse employees for expenses that are:",
        body_style
    ))
    elements.append(Paragraph("• <b>Reasonable:</b> Expenses should reflect prudent spending and cost-consciousness. "
                            "The company expects employees to exercise the same care in incurring expenses as they "
                            "would with their own personal funds.", bullet_style))
    elements.append(Paragraph("• <b>Necessary:</b> Expenses must be essential for conducting company business and "
                            "achieving business objectives. Luxury or convenience items that are not required for "
                            "business purposes are not reimbursable.", bullet_style))
    elements.append(Paragraph("• <b>Business-Related:</b> All expenses must have a clear business purpose and directly "
                            "relate to company activities. Personal expenses, even if incurred during business travel, "
                            "are not reimbursable.", bullet_style))

    elements.append(PageBreak())

    # ==================== SECTION 2: EXPENSE CATEGORIES ====================
    elements.append(Paragraph("Section 2: Expense Categories", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>2.1 Allowable Expenses</b>", heading2_style))
    elements.append(Paragraph(
        "The following categories of expenses are eligible for reimbursement when they meet the "
        "reasonable, necessary, and business-related criteria:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>Business Travel</b>", heading3_style))
    elements.append(Paragraph(
        "Includes airfare, hotel accommodations, ground transportation, and related travel expenses "
        "incurred for business purposes. All travel must be approved in advance by the appropriate "
        "manager. See Section 3 for detailed travel policies and limitations.",
        bullet_style
    ))

    elements.append(Paragraph("<b>Client Meals and Entertainment</b>", heading3_style))
    elements.append(Paragraph(
        "Reasonable expenses for meals and entertainment with clients, prospects, or business partners "
        "are reimbursable when they serve a legitimate business purpose. Employees must document the "
        "business purpose and attendees. See Section 4 for specific limits based on employee level.",
        bullet_style
    ))

    elements.append(Paragraph("<b>Office Supplies</b>", heading3_style))
    elements.append(Paragraph(
        "Necessary office supplies and equipment required to perform job duties. Standard office supplies "
        "should be ordered through approved vendors. Individual purchases over $100 require manager approval.",
        bullet_style
    ))

    elements.append(Paragraph("<b>Professional Development</b>", heading3_style))
    elements.append(Paragraph(
        "Conference registrations, professional certifications, training courses, and educational materials "
        "that enhance job performance and align with career development goals. All professional development "
        "expenses over $1,000 require pre-approval from the department head.",
        bullet_style
    ))

    elements.append(Paragraph("<b>Software and Subscriptions</b>", heading3_style))
    elements.append(Paragraph(
        "Business-related software licenses, SaaS subscriptions, and online tools necessary for job performance. "
        "Monthly subscriptions over $50 require manager approval. Annual subscriptions over $500 require "
        "department head approval.",
        bullet_style
    ))

    elements.append(Paragraph("<b>Phone and Internet (Remote Employees)</b>", heading3_style))
    elements.append(Paragraph(
        "Remote employees may be reimbursed up to $75 per month for phone and internet expenses. Employees "
        "must submit a monthly expense report with supporting documentation. This reimbursement is designed "
        "to offset the cost of maintaining connectivity required for remote work.",
        bullet_style
    ))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>2.2 Non-Reimbursable Expenses</b>", heading2_style))
    elements.append(Paragraph(
        "The following expenses are specifically excluded from reimbursement:",
        body_style
    ))

    elements.append(Paragraph("• <b>Personal Items:</b> Toiletries, clothing, personal entertainment, gym memberships, "
                            "or any other personal purchases are not reimbursable, even if purchased during business travel.",
                            bullet_style))
    elements.append(Paragraph("• <b>Alcoholic Beverages:</b> Alcohol is generally not reimbursable except when consumed "
                            "as part of a client dinner and approved by a VP or higher. Even with approval, alcohol "
                            "reimbursement is limited to two drinks per person at a reasonable cost.",
                            bullet_style))
    elements.append(Paragraph("• <b>Fines and Penalties:</b> Traffic tickets, parking violations, late fees, or any other "
                            "penalties incurred due to employee negligence are not reimbursable.",
                            bullet_style))
    elements.append(Paragraph("• <b>Upgrades Not Pre-Approved:</b> Flight upgrades, hotel room upgrades, or car rental "
                            "upgrades that were not pre-approved are not reimbursable. Any deviation from standard travel "
                            "policy must be approved in advance.",
                            bullet_style))

    elements.append(PageBreak())

    # ==================== SECTION 3: TRAVEL ARRANGEMENTS ====================
    elements.append(Paragraph("Section 3: Travel Arrangements", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>3.1 Flight Policy</b>", heading2_style))
    elements.append(Paragraph(
        "All business air travel must be booked in accordance with the following guidelines:",
        body_style
    ))

    elements.append(Paragraph("• <b>Economy Class:</b> Required for all flights under 6 hours duration, regardless of "
                            "employee level. Employees should select the most cost-effective flight option that meets "
                            "business scheduling requirements.",
                            bullet_style))
    elements.append(Paragraph("• <b>Premium Economy:</b> Permitted for flights between 6 and 12 hours duration for all "
                            "employees. Premium economy provides additional comfort for longer flights while maintaining "
                            "cost efficiency.",
                            bullet_style))
    elements.append(Paragraph("• <b>Business Class:</b> Available only for flights exceeding 12 hours duration and only "
                            "for Director-level employees and above. All business class bookings must be pre-approved by "
                            "the department VP.",
                            bullet_style))
    elements.append(Paragraph("• <b>Advance Booking:</b> Employees are encouraged to book flights at least 14 days in "
                            "advance whenever possible to secure the best rates. Last-minute bookings should be avoided "
                            "except when required by urgent business needs.",
                            bullet_style))
    elements.append(Paragraph("• <b>Corporate Travel Agency:</b> All flights must be booked through our designated corporate "
                            "travel agency, which provides a 20% discount on most routes. Direct bookings are only permitted "
                            "with prior approval from Finance.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>3.2 Hotel Policy</b>", heading2_style))
    elements.append(Paragraph(
        "Hotel accommodations must meet the following standards:",
        body_style
    ))

    elements.append(Paragraph("• <b>Major Cities:</b> Hotel rate limit of $200 per night (excluding taxes and fees) in "
                            "major metropolitan areas including New York, San Francisco, Los Angeles, Chicago, Boston, "
                            "Seattle, and international equivalents.",
                            bullet_style))
    elements.append(Paragraph("• <b>Other Locations:</b> Hotel rate limit of $150 per night (excluding taxes and fees) "
                            "in all other locations. Employees should select clean, safe, and reasonably located hotels "
                            "within this rate limit.",
                            bullet_style))
    elements.append(Paragraph("• <b>Corporate Hotel Partners:</b> Employees must use designated corporate hotel partners "
                            "when available. These partnerships provide preferred rates and benefits. A list of preferred "
                            "hotels is available on the company intranet.",
                            bullet_style))
    elements.append(Paragraph("• <b>Extended Stay:</b> For trips of 7 nights or longer, employees may use Airbnb or "
                            "corporate housing alternatives, which often provide better value for extended periods. Weekly "
                            "or monthly rates may offer significant savings.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>3.3 Ground Transportation</b>", heading2_style))
    elements.append(Paragraph(
        "Ground transportation expenses should be reasonable and cost-effective:",
        body_style
    ))

    elements.append(Paragraph("• <b>Airport Shuttles:</b> Preferred method for airport transfers when available. Many "
                            "hotels offer complimentary shuttle service that should be used when timing permits.",
                            bullet_style))
    elements.append(Paragraph("• <b>Taxi/Rideshare:</b> Permitted when shuttles are unavailable or impractical. Employees "
                            "must retain all receipts for taxi and rideshare expenses. Reasonable tips (15-20%) are included "
                            "in reimbursement.",
                            bullet_style))
    elements.append(Paragraph("• <b>Car Rental:</b> Mid-size vehicles or smaller are standard for all employees. Larger "
                            "vehicles may be rented only when transporting 3 or more people. All car rentals require "
                            "pre-approval and should be booked through the corporate travel agency for insurance coverage.",
                            bullet_style))
    elements.append(Paragraph("• <b>Mileage Reimbursement:</b> Personal vehicle use for business purposes is reimbursed at "
                            "$0.67 per mile (current IRS standard rate). Employees must document starting and ending locations, "
                            "total miles driven, and business purpose.",
                            bullet_style))

    elements.append(PageBreak())

    # ==================== SECTION 4: MEALS & PER DIEM ====================
    elements.append(Paragraph("Section 4: Meals & Per Diem", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>4.1 Domestic Travel Meal Allowances</b>", heading2_style))
    elements.append(Paragraph(
        "Employees traveling within the United States are entitled to the following daily meal allowances:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    # Domestic per diem table
    domestic_data = [
        ['Meal', 'Maximum Allowance', 'Notes'],
        ['Breakfast', '$15', 'Available for overnight travel'],
        ['Lunch', '$20', 'Business days only'],
        ['Dinner', '$40', 'Available for overnight travel'],
        ['Daily Total', '$75', 'Combined maximum per day']
    ]

    domestic_table = Table(domestic_data, colWidths=[1.5*inch, 1.8*inch, 2.5*inch])
    domestic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(domestic_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("<b>4.2 International Travel Meal Allowances</b>", heading2_style))
    elements.append(Paragraph(
        "For international business travel, daily meal allowances vary by region:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    # International per diem table
    intl_data = [
        ['Region', 'Daily Allowance', 'Applicable Countries/Areas'],
        ['Europe', '€85/day', 'All European Union countries, UK, Switzerland, Norway'],
        ['Asia', '$90/day', 'Japan, Singapore, Hong Kong, South Korea, Australia'],
        ['Other Regions', '$80/day', 'All other international destinations']
    ]

    intl_table = Table(intl_data, colWidths=[1.5*inch, 1.5*inch, 2.8*inch])
    intl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(intl_table)
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph("<b>4.3 Client Meals and Entertainment</b>", heading2_style))
    elements.append(Paragraph(
        "Meal expenses with clients, prospects, or business partners are subject to limits based on "
        "employee level and require appropriate documentation:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    # Client meals table
    client_data = [
        ['Employee Level', 'Maximum Per Meal', 'Approval Required'],
        ['Individual Contributor', 'Up to $100', 'Manager approval required'],
        ['Manager', 'Up to $200', 'Self-approved, Director notification'],
        ['VP and Above', 'Up to $500', 'Self-approved, CFO notification']
    ]

    client_table = Table(client_data, colWidths=[2*inch, 1.8*inch, 2*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(client_table)
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("• <b>Alcohol Limit:</b> Alcoholic beverages are limited to 2 drinks per person at a "
                            "reasonable cost, and only when part of client entertainment with VP or higher approval. "
                            "Excessive alcohol expenses will not be reimbursed.",
                            bullet_style))
    elements.append(Paragraph("• <b>Receipt Requirement:</b> Detailed receipts are required for all meal expenses "
                            "exceeding $25. Credit card statements alone are not sufficient. Receipts must show itemized "
                            "charges.",
                            bullet_style))

    elements.append(PageBreak())

    # ==================== SECTION 5: APPROVAL WORKFLOWS ====================
    elements.append(Paragraph("Section 5: Approval Workflows", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>5.1 Pre-Approval Requirements</b>", heading2_style))
    elements.append(Paragraph(
        "Certain expenses require advance approval before being incurred. Failure to obtain pre-approval "
        "may result in denial of reimbursement. The following categories require pre-approval:",
        body_style
    ))

    elements.append(Paragraph("• <b>International Travel:</b> All international business travel must be approved at least "
                            "two weeks in advance by the department head. International travel requests should include "
                            "business justification, itinerary, and estimated costs.",
                            bullet_style))
    elements.append(Paragraph("• <b>Expenses Exceeding $500:</b> Any single expense over $500 requires pre-approval from "
                            "the appropriate authority level (see approval hierarchy below). This includes equipment purchases, "
                            "software licenses, and other significant expenditures.",
                            bullet_style))
    elements.append(Paragraph("• <b>Conference Registration Over $1,000:</b> Professional development conferences with "
                            "registration fees exceeding $1,000 must be pre-approved by the department head. The request "
                            "should include the conference agenda and expected business benefit.",
                            bullet_style))
    elements.append(Paragraph("• <b>Car Rentals:</b> All car rental arrangements require pre-approval from a direct manager. "
                            "The request should justify why other transportation options are insufficient.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>5.2 Approval Hierarchy</b>", heading2_style))
    elements.append(Paragraph(
        "Expense approvals are required based on the total amount of the expense or expense report:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    # Approval hierarchy table
    approval_data = [
        ['Expense Amount', 'Required Approver', 'Expected Turnaround'],
        ['Less than $500', 'Direct Manager', '2 business days'],
        ['$500 - $2,000', 'Department Head', '3 business days'],
        ['$2,000 - $5,000', 'Vice President', '5 business days'],
        ['Over $5,000', 'Chief Financial Officer', '7 business days']
    ]

    approval_table = Table(approval_data, colWidths=[1.8*inch, 2*inch, 2*inch])
    approval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(approval_table)
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph(
        "Approvers are expected to review expense submissions within the turnaround times listed above. "
        "Employees should plan accordingly and submit expenses well in advance of any reimbursement deadlines.",
        body_style
    ))

    elements.append(PageBreak())

    # ==================== SECTION 6: RECEIPT REQUIREMENTS ====================
    elements.append(Paragraph("Section 6: Receipt Requirements", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>6.1 Receipt Documentation Standards</b>", heading2_style))
    elements.append(Paragraph(
        "Proper receipt documentation is essential for expense reimbursement and tax compliance. "
        "All employees must adhere to the following receipt requirements:",
        body_style
    ))

    elements.append(Paragraph("• <b>Threshold:</b> All expenses exceeding $25 require a detailed receipt. Expenses under "
                            "$25 may be submitted without a receipt but must include a complete description of the purchase "
                            "and business purpose.",
                            bullet_style))
    elements.append(Paragraph("• <b>Digital Photos Acceptable:</b> Employees may photograph receipts using their smartphone "
                            "or scanner. Digital images must be clear, legible, and show all relevant information including "
                            "merchant name, date, items purchased, and total amount.",
                            bullet_style))
    elements.append(Paragraph("• <b>Credit Card Statements Insufficient:</b> Credit card statements or transaction summaries "
                            "alone are not acceptable as receipt documentation. Itemized receipts showing specific purchases "
                            "are required for all expenses over $25.",
                            bullet_style))
    elements.append(Paragraph("• <b>Missing Receipts:</b> If a receipt is lost or unavailable, employees must complete an "
                            "Expense Affidavit form providing details of the expense. The affidavit requires manager approval "
                            "and should be used only in exceptional circumstances.",
                            bullet_style))
    elements.append(Paragraph("• <b>Retention Policy:</b> While employees are required to submit receipts with expense reports, "
                            "the Expensify system automatically retains all receipts for seven years in compliance with IRS "
                            "requirements. Employees do not need to maintain personal copies.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>6.2 Required Receipt Information</b>", heading2_style))
    elements.append(Paragraph(
        "All receipts must clearly display the following information to be acceptable for reimbursement:",
        body_style
    ))

    elements.append(Paragraph("• Merchant or vendor name", bullet_style))
    elements.append(Paragraph("• Transaction date", bullet_style))
    elements.append(Paragraph("• Itemized list of goods or services purchased", bullet_style))
    elements.append(Paragraph("• Total amount paid, including taxes and tips", bullet_style))
    elements.append(Paragraph("• Payment method (for verification purposes)", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "For meal receipts, employees must also annotate the receipt or expense report with the names "
        "of all attendees and the business purpose of the meal. This information is required for IRS "
        "compliance and internal audit purposes.",
        body_style
    ))

    elements.append(PageBreak())

    # ==================== SECTION 7: EXPENSE SUBMISSION ====================
    elements.append(Paragraph("Section 7: Expense Submission", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>7.1 Submission Deadlines</b>", heading2_style))
    elements.append(Paragraph(
        "Timely expense submission is critical for accurate financial reporting and ensures prompt "
        "reimbursement. The following deadlines apply:",
        body_style
    ))

    elements.append(Paragraph("• <b>Standard Deadline:</b> All expenses must be submitted within 30 days of the expense date. "
                            "This deadline ensures that expenses are recorded in the appropriate accounting period and allows "
                            "for efficient processing.",
                            bullet_style))
    elements.append(Paragraph("• <b>Late Submissions:</b> Expense reports submitted between 30 and 90 days after the expense "
                            "date require VP approval. Late submissions create accounting challenges and may be subject to "
                            "additional scrutiny.",
                            bullet_style))
    elements.append(Paragraph("• <b>Expired Expenses:</b> Expenses more than 90 days old will not be reimbursed under any "
                            "circumstances. This policy is firm and applies to all employees regardless of level. Employees "
                            "are responsible for managing their expense submissions within the allowable timeframe.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>7.2 Expensify Platform</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp Solutions Inc. uses Expensify as the official expense management platform. All expense "
        "reports must be submitted through Expensify. The platform offers several features:",
        body_style
    ))

    elements.append(Paragraph("• Mobile app for on-the-go expense submission and receipt capture", bullet_style))
    elements.append(Paragraph("• Automatic credit card transaction import for corporate card holders", bullet_style))
    elements.append(Paragraph("• Integration with company accounting systems for seamless processing", bullet_style))
    elements.append(Paragraph("• Real-time approval workflow and status tracking", bullet_style))
    elements.append(Paragraph("• Automated policy compliance checking", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "New employees will receive Expensify training during onboarding. Additional support resources "
        "are available on the company intranet and through the IT help desk.",
        body_style
    ))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>7.3 Required Information</b>", heading2_style))
    elements.append(Paragraph(
        "Each expense report submission must include the following information:",
        body_style
    ))

    elements.append(Paragraph("• <b>Business Purpose:</b> A clear, concise description of the business reason for the expense. "
                            "Generic descriptions like 'business meal' or 'client meeting' are insufficient. Provide specific "
                            "details such as 'Dinner with ABC Corp to discuss Q2 partnership agreement.'",
                            bullet_style))
    elements.append(Paragraph("• <b>Attendees:</b> For meal and entertainment expenses, list all attendees including their "
                            "company affiliation. Internal-only meals require department head approval.",
                            bullet_style))
    elements.append(Paragraph("• <b>Project/Client Code:</b> All expenses must be assigned to the appropriate project or "
                            "client code for accurate cost allocation. Employees should consult with their manager if unsure "
                            "of the correct code.",
                            bullet_style))
    elements.append(Paragraph("• <b>Receipt Attachment:</b> Digital copy of the receipt must be attached to each expense line "
                            "item in Expensify. The system will flag missing receipts for expenses over $25.",
                            bullet_style))

    elements.append(PageBreak())

    # ==================== SECTION 8: REIMBURSEMENT PROCESS ====================
    elements.append(Paragraph("Section 8: Reimbursement Process", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>8.1 Processing Timeline</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp Solutions Inc. is committed to processing approved expense reimbursements in a timely manner:",
        body_style
    ))

    elements.append(Paragraph("• <b>Standard Processing:</b> Expense reimbursements will be processed within 15 business days "
                            "of final approval. This timeline assumes the expense report is complete, accurate, and compliant "
                            "with all policy requirements.",
                            bullet_style))
    elements.append(Paragraph("• <b>Payment Method:</b> Reimbursements are made via direct deposit to the employee's designated "
                            "bank account on file with Payroll. Employees must ensure their banking information is current in "
                            "the HR system.",
                            bullet_style))
    elements.append(Paragraph("• <b>Payment Schedule:</b> Reimbursement payments are processed twice per month on the 15th "
                            "and last business day of each month. Expenses approved after the cut-off date will be included "
                            "in the next payment cycle.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>8.2 Currency and Foreign Exchange</b>", heading2_style))
    elements.append(Paragraph(
        "For international expenses incurred in foreign currencies:",
        body_style
    ))

    elements.append(Paragraph("• <b>Reimbursement Currency:</b> All reimbursements are paid in U.S. Dollars (USD) regardless "
                            "of the original expense currency.",
                            bullet_style))
    elements.append(Paragraph("• <b>Exchange Rate:</b> Foreign currency expenses are converted to USD using the exchange rate "
                            "in effect on the date the expense report is submitted (not the date the expense was incurred). "
                            "The company uses the XE.com daily rates for all currency conversions.",
                            bullet_style))
    elements.append(Paragraph("• <b>Exchange Rate Fluctuations:</b> Employees who delay submitting expense reports assume the "
                            "risk of exchange rate fluctuations. This policy reinforces the importance of timely expense submission.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>8.3 Tax Implications</b>", heading2_style))
    elements.append(Paragraph(
        "Most business expense reimbursements are not considered taxable income. However, employees are "
        "responsible for understanding and reporting any tax implications of expense reimbursements if applicable "
        "under IRS regulations. Employees should consult with a tax professional if they have questions about "
        "the taxability of specific reimbursements. The company does not provide tax advice to employees.",
        body_style
    ))

    elements.append(PageBreak())

    # ==================== SECTION 9: CORPORATE CARDS ====================
    elements.append(Paragraph("Section 9: Corporate Cards", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>9.1 Eligibility and Application</b>", heading2_style))
    elements.append(Paragraph(
        "Corporate credit cards are available to employees who frequently incur business expenses:",
        body_style
    ))

    elements.append(Paragraph("• <b>Eligible Employees:</b> Manager-level employees and above, or employees who travel "
                            "frequently for business (defined as at least once per month), are eligible for a corporate "
                            "credit card.",
                            bullet_style))
    elements.append(Paragraph("• <b>Application Process:</b> Employees should submit a corporate card request through the "
                            "Finance portal. Requests require manager approval and are typically processed within 10 business days.",
                            bullet_style))
    elements.append(Paragraph("• <b>Card Features:</b> Corporate cards offer rewards points, travel insurance, and purchase "
                            "protection. All rewards earned on corporate cards belong to the company and will be used to offset "
                            "travel expenses.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>9.2 Credit Limits</b>", heading2_style))
    elements.append(Paragraph(
        "Corporate card credit limits are assigned based on employee level and business needs:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    # Credit limit table
    card_limit_data = [
        ['Employee Level', 'Monthly Credit Limit', 'Increase Process'],
        ['Manager', '$5,000', 'Department head approval required'],
        ['Director', '$10,000', 'VP approval required'],
        ['VP and Above', '$25,000', 'CFO approval for increases']
    ]

    card_limit_table = Table(card_limit_data, colWidths=[2*inch, 2*inch, 2*inch])
    card_limit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(card_limit_table)
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>9.3 Payment Responsibility</b>", heading2_style))
    elements.append(Paragraph(
        "Important: Corporate credit cards are issued in the employee's name, and the employee is legally "
        "responsible for payment. While the company reimburses approved business expenses, employees must "
        "pay the credit card bill by the due date to avoid interest charges and late fees, which are not "
        "reimbursable. The company processes reimbursements on the standard schedule outlined in Section 8.",
        body_style
    ))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>9.4 Prohibited Uses</b>", heading2_style))
    elements.append(Paragraph(
        "Corporate credit cards must be used exclusively for business expenses as defined in this policy. "
        "Personal charges on corporate cards are strictly prohibited and may result in:",
        body_style
    ))

    elements.append(Paragraph("• Immediate card revocation", bullet_style))
    elements.append(Paragraph("• Disciplinary action up to and including termination", bullet_style))
    elements.append(Paragraph("• Requirement to reimburse the company for personal charges plus administrative fees", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>9.5 Lost or Stolen Cards</b>", heading2_style))
    elements.append(Paragraph(
        "If a corporate credit card is lost or stolen, employees must immediately:",
        body_style
    ))

    elements.append(Paragraph("1. Call the card issuer's 24-hour customer service number (printed on the back of the card)", bullet_style))
    elements.append(Paragraph("2. Report the loss to finance@techcorp.com within 24 hours", bullet_style))
    elements.append(Paragraph("3. Complete a Lost/Stolen Card Incident Report", bullet_style))

    elements.append(Paragraph(
        "A replacement card will be issued within 5-7 business days. Employees are not responsible for "
        "fraudulent charges if reported promptly.",
        body_style
    ))

    elements.append(PageBreak())

    # ==================== SECTION 10: VIOLATIONS & CONSEQUENCES ====================
    elements.append(Paragraph("Section 10: Violations & Consequences", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>10.1 Expense Audits</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp Solutions Inc. maintains a comprehensive expense audit program to ensure policy compliance "
        "and prevent fraud:",
        body_style
    ))

    elements.append(Paragraph("• <b>Random Audits:</b> Approximately 10% of all expense submissions are randomly selected "
                            "for detailed audit each month. Audits may include verification of receipts, business purpose, "
                            "and compliance with policy limits.",
                            bullet_style))
    elements.append(Paragraph("• <b>Targeted Audits:</b> Expense reports that exceed certain thresholds or exhibit unusual "
                            "patterns may be selected for targeted audit. The Finance team uses data analytics to identify "
                            "potential compliance issues.",
                            bullet_style))
    elements.append(Paragraph("• <b>Audit Cooperation:</b> Employees selected for audit must cooperate fully with the audit "
                            "process, including providing additional documentation or clarification as requested. Failure to "
                            "cooperate may result in denial of reimbursement and disciplinary action.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>10.2 Policy Violations</b>", heading2_style))
    elements.append(Paragraph(
        "Policy violations are taken seriously and may result in progressive disciplinary action:",
        body_style
    ))

    elements.append(Paragraph("• <b>Minor Violations:</b> Occasional errors or minor policy deviations (such as missing "
                            "receipt annotations or delayed submissions) will typically result in a request for correction "
                            "without formal discipline. However, patterns of minor violations may lead to progressive discipline.",
                            bullet_style))
    elements.append(Paragraph("• <b>First Violation:</b> Documented warning plus mandatory expense policy training. The "
                            "employee's manager will conduct a review session to ensure understanding of policy requirements.",
                            bullet_style))
    elements.append(Paragraph("• <b>Second Violation:</b> Written warning, mandatory training, and revocation of corporate "
                            "card privileges for a minimum of 6 months. Future expenses must be paid personally and submitted "
                            "for reimbursement.",
                            bullet_style))
    elements.append(Paragraph("• <b>Third Violation:</b> Final written warning with consideration for termination of employment. "
                            "The employee will be placed on a 90-day performance improvement plan with monthly expense reviews.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>10.3 Fraudulent Expenses</b>", heading2_style))
    elements.append(Paragraph(
        "Expense fraud is a serious offense that will result in immediate and severe consequences:",
        body_style
    ))

    elements.append(Paragraph("• <b>Definition:</b> Fraudulent expenses include, but are not limited to: submitting fake "
                            "receipts, claiming personal expenses as business expenses, inflating expense amounts, duplicate "
                            "submissions, or any intentional misrepresentation.",
                            bullet_style))
    elements.append(Paragraph("• <b>Immediate Termination:</b> Any employee found to have submitted fraudulent expenses will "
                            "be immediately terminated for cause. There is zero tolerance for expense fraud.",
                            bullet_style))
    elements.append(Paragraph("• <b>Legal Action:</b> The company reserves the right to pursue legal action, including criminal "
                            "prosecution, against employees who commit expense fraud. The company will seek full restitution plus "
                            "legal fees and damages.",
                            bullet_style))
    elements.append(Paragraph("• <b>Reference Checks:</b> Termination for expense fraud will be disclosed to future employers "
                            "conducting reference checks, as permitted by law.",
                            bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>10.4 Reporting Violations</b>", heading2_style))
    elements.append(Paragraph(
        "Employees who become aware of policy violations or suspected fraud should report concerns to:",
        body_style
    ))

    elements.append(Paragraph("• Their direct manager or department head", bullet_style))
    elements.append(Paragraph("• The Finance Department at finance@techcorp.com", bullet_style))
    elements.append(Paragraph("• The anonymous Ethics Hotline at 1-800-555-0123", bullet_style))

    elements.append(Paragraph(
        "TechCorp Solutions Inc. prohibits retaliation against employees who report suspected violations in "
        "good faith. All reports will be investigated confidentially to the extent possible.",
        body_style
    ))

    elements.append(PageBreak())

    # ==================== SECTION 11: CONTACT INFORMATION ====================
    elements.append(Paragraph("Section 11: Contact Information", heading1_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>11.1 Department Contacts</b>", heading2_style))
    elements.append(Paragraph(
        "For questions or assistance with expense and travel matters, please contact the appropriate department:",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>Finance Team</b>", heading3_style))
    elements.append(Paragraph("Email: finance@techcorp.com", bullet_style))
    elements.append(Paragraph("Phone: (555) 123-4567", bullet_style))
    elements.append(Paragraph("Hours: Monday-Friday, 8:00 AM - 5:00 PM PST", bullet_style))
    elements.append(Paragraph(
        "Contact the Finance team for questions about expense policy interpretation, approval status, "
        "reimbursement timing, corporate cards, or general expense-related inquiries.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>Travel Desk</b>", heading3_style))
    elements.append(Paragraph("Email: travel@techcorp.com", bullet_style))
    elements.append(Paragraph("Phone: (555) 123-4568", bullet_style))
    elements.append(Paragraph("Hours: Monday-Friday, 7:00 AM - 7:00 PM PST", bullet_style))
    elements.append(Paragraph(
        "The Travel Desk assists with booking flights, hotels, and car rentals through our preferred vendors. "
        "They can also provide guidance on travel policy compliance and help with travel emergencies.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>Expensify Support</b>", heading3_style))
    elements.append(Paragraph("Platform: https://expensify.techcorp.com", bullet_style))
    elements.append(Paragraph("Support: help@expensify.com", bullet_style))
    elements.append(Paragraph("Knowledge Base: https://help.expensify.com", bullet_style))
    elements.append(Paragraph(
        "For technical issues with the Expensify platform, refer to the knowledge base or contact Expensify "
        "support directly. For policy-related questions, contact the Finance team.",
        bullet_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("<b>11.2 Additional Resources</b>", heading2_style))
    elements.append(Paragraph(
        "Additional expense and travel resources are available on the company intranet:",
        body_style
    ))

    elements.append(Paragraph("• Expense Policy FAQ", bullet_style))
    elements.append(Paragraph("• Expensify Video Tutorials", bullet_style))
    elements.append(Paragraph("• Preferred Vendor Directory", bullet_style))
    elements.append(Paragraph("• Travel Safety Guidelines", bullet_style))
    elements.append(Paragraph("• Currency Exchange Calculator", bullet_style))
    elements.append(Paragraph("• Expense Affidavit Template", bullet_style))

    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("<b>11.3 Policy Updates</b>", heading2_style))
    elements.append(Paragraph(
        "This policy is reviewed annually and updated as needed to reflect business requirements, regulatory "
        "changes, and best practices. Employees will be notified of policy updates via email and must acknowledge "
        "receipt. The current policy version is always available on the company intranet.",
        body_style
    ))

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(
        "For questions about this policy or suggested improvements, please contact the Finance Department.",
        body_style
    ))

    elements.append(Spacer(1, 0.5*inch))

    # Footer
    elements.append(Paragraph("***", ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.grey
    )))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "TechCorp Solutions Inc. | Expense & Travel Policy 2026 | Version 1.0",
        ParagraphStyle(
            'Footer2',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
    ))
    elements.append(Paragraph(
        "This document is confidential and intended for TechCorp Solutions Inc. employees only.",
        ParagraphStyle(
            'Footer3',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
    ))

    # Build PDF
    doc.build(elements)
    print(f"PDF successfully created: {filename}")

if __name__ == "__main__":
    output_file = r"D:\Whatsapp analyzer\documents\expense_policy.pdf"
    create_expense_policy_pdf(output_file)
