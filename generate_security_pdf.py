from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime

def create_it_security_pdf():
    # Create PDF
    pdf_path = "D:/Whatsapp analyzer/documents/it_security_guidelines.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    confidential_style = ParagraphStyle(
        'Confidential',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.red,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2b6cb0'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=6,
        leftIndent=20,
        bulletIndent=10,
        leading=14
    )

    # ========== COVER PAGE ==========
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("TechCorp Solutions Inc.", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("IT Security Guidelines", title_style))
    elements.append(Paragraph("2026", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("CONFIDENTIAL", confidential_style))
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph(f"Effective Date: January 1, 2026<br/>Last Updated: {datetime.now().strftime('%B %d, %Y')}",
                             subtitle_style))
    elements.append(PageBreak())

    # ========== TABLE OF CONTENTS ==========
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    toc_data = [
        ["Section 1:", "Introduction", "3"],
        ["Section 2:", "Password Policy", "3"],
        ["Section 3:", "Data Classification", "4"],
        ["Section 4:", "Email Security", "4"],
        ["Section 5:", "Device Security", "5"],
        ["Section 6:", "Network Security", "6"],
        ["Section 7:", "Physical Security", "6"],
        ["Section 8:", "Incident Response", "7"],
        ["Section 9:", "Acceptable Use Policy", "7"],
        ["Section 10:", "Penalties and Enforcement", "8"],
    ]

    for item in toc_data:
        elements.append(Paragraph(f"<b>{item[0]}</b> {item[1]} {'.' * 50} Page {item[2]}", body_style))

    elements.append(PageBreak())

    # ========== SECTION 1: INTRODUCTION ==========
    elements.append(Paragraph("Section 1: Introduction", heading1_style))

    elements.append(Paragraph("<b>Purpose and Scope</b>", heading2_style))
    elements.append(Paragraph(
        "Information security is a critical foundation of TechCorp Solutions Inc.'s operations. "
        "This document establishes mandatory security guidelines to protect our company's data, "
        "systems, and reputation. All employees, contractors, and third-party users with access "
        "to TechCorp resources must comply with these policies.",
        body_style
    ))

    elements.append(Paragraph("<b>Shared Responsibility Model</b>", heading2_style))
    elements.append(Paragraph(
        "Security is everyone's responsibility. While the IT Security team provides tools and "
        "infrastructure, each employee must actively protect company assets through vigilant "
        "security practices. This includes safeguarding credentials, recognizing threats, and "
        "promptly reporting suspicious activities.",
        body_style
    ))

    elements.append(Paragraph("<b>Compliance Requirements</b>", heading2_style))
    elements.append(Paragraph("TechCorp maintains compliance with multiple regulatory frameworks:", body_style))
    elements.append(Paragraph("• <b>SOC 2 Type II:</b> Annual audits of security controls and processes", bullet_style))
    elements.append(Paragraph("• <b>GDPR:</b> Protection of EU citizen data and privacy rights", bullet_style))
    elements.append(Paragraph("• <b>HIPAA:</b> Safeguarding protected health information (where applicable)", bullet_style))
    elements.append(Paragraph("• <b>Industry Standards:</b> PCI-DSS for payment processing, ISO 27001 frameworks", bullet_style))

    elements.append(Paragraph("<b>Security Incident Reporting</b>", heading2_style))
    elements.append(Paragraph(
        "Immediately report any security concerns to security@techcorp.com or call the IT Security "
        "Hotline at extension 5500. Early reporting minimizes damage and enables rapid response. "
        "TechCorp maintains a no-blame culture for good-faith security reports.",
        body_style
    ))

    # ========== SECTION 2: PASSWORD POLICY ==========
    elements.append(Paragraph("Section 2: Password Policy", heading1_style))

    elements.append(Paragraph(
        "Strong passwords are the first line of defense against unauthorized access. "
        "All TechCorp passwords must meet the following requirements:",
        body_style
    ))

    elements.append(Paragraph("<b>Password Requirements</b>", heading2_style))
    elements.append(Paragraph("• <b>Minimum Length:</b> 12 characters (16+ characters recommended)", bullet_style))
    elements.append(Paragraph("• <b>Complexity:</b> Must include uppercase letters, lowercase letters, numbers, and special characters (!@#$%^&*)", bullet_style))
    elements.append(Paragraph("• <b>Rotation:</b> Passwords must be changed every 90 days", bullet_style))
    elements.append(Paragraph("• <b>No Reuse:</b> Cannot reuse any of your last 10 passwords", bullet_style))
    elements.append(Paragraph("• <b>Prohibited Content:</b> No dictionary words, company name (TechCorp), your name, or personal information (birthdays, addresses)", bullet_style))

    elements.append(Paragraph("<b>Password Managers</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp strongly recommends using a password manager to generate and securely store "
        "unique passwords for each account. Approved solutions include:",
        body_style
    ))
    elements.append(Paragraph("• 1Password (Enterprise license available)", bullet_style))
    elements.append(Paragraph("• LastPass Business", bullet_style))
    elements.append(Paragraph("• Bitwarden Teams", bullet_style))

    elements.append(Paragraph("<b>Multi-Factor Authentication (MFA)</b>", heading2_style))
    elements.append(Paragraph("MFA is mandatory for all corporate accounts and systems:", body_style))
    elements.append(Paragraph("• <b>Required:</b> All email, VPN, cloud services, and administrative access", bullet_style))
    elements.append(Paragraph("• <b>Preferred Method:</b> Authenticator apps (Microsoft Authenticator, Google Authenticator, Authy)", bullet_style))
    elements.append(Paragraph("• <b>Acceptable:</b> Hardware security keys (YubiKey)", bullet_style))
    elements.append(Paragraph("• <b>Discouraged:</b> SMS-based authentication (vulnerable to SIM swapping attacks)", bullet_style))

    elements.append(PageBreak())

    # ========== SECTION 3: DATA CLASSIFICATION ==========
    elements.append(Paragraph("Section 3: Data Classification", heading1_style))

    elements.append(Paragraph(
        "All TechCorp data is classified into four levels based on sensitivity. "
        "Employees must handle data according to its classification level.",
        body_style
    ))

    elements.append(Paragraph("<b>Classification Levels</b>", heading2_style))

    elements.append(Paragraph("<b>PUBLIC:</b>", body_style))
    elements.append(Paragraph("• Examples: Marketing materials, press releases, job postings, public website content", bullet_style))
    elements.append(Paragraph("• Handling: Can be freely shared with external parties", bullet_style))
    elements.append(Paragraph("• Encryption: Not required", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>INTERNAL:</b>", body_style))
    elements.append(Paragraph("• Examples: Internal memos, organizational charts, policies, meeting notes", bullet_style))
    elements.append(Paragraph("• Handling: For TechCorp employees and authorized contractors only", bullet_style))
    elements.append(Paragraph("• Encryption: Required for transmission outside company network", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>CONFIDENTIAL:</b>", body_style))
    elements.append(Paragraph("• Examples: Customer data, financial records, employee information, contracts", bullet_style))
    elements.append(Paragraph("• Handling: Need-to-know basis only, written approval required for external sharing", bullet_style))
    elements.append(Paragraph("• Encryption: AES-256 encryption mandatory for storage and transmission", bullet_style))
    elements.append(Paragraph("• Access: Logged and audited quarterly", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>SECRET:</b>", body_style))
    elements.append(Paragraph("• Examples: Trade secrets, unreleased products, merger/acquisition plans, encryption keys", bullet_style))
    elements.append(Paragraph("• Handling: Executive approval required for access, NDAs mandatory", bullet_style))
    elements.append(Paragraph("• Encryption: AES-256 encryption with additional access controls", bullet_style))
    elements.append(Paragraph("• Access: Real-time monitoring and alerting", bullet_style))

    # ========== SECTION 4: EMAIL SECURITY ==========
    elements.append(Paragraph("Section 4: Email Security", heading1_style))

    elements.append(Paragraph(
        "Email remains the primary attack vector for cybercriminals. Exercise caution with all "
        "incoming messages, especially from external senders.",
        body_style
    ))

    elements.append(Paragraph("<b>Phishing Awareness</b>", heading2_style))
    elements.append(Paragraph("Be alert for these phishing red flags:", body_style))
    elements.append(Paragraph("• Urgent or threatening language (\"Account will be suspended!\")", bullet_style))
    elements.append(Paragraph("• Requests for passwords, credentials, or financial information", bullet_style))
    elements.append(Paragraph("• Suspicious sender addresses (slight misspellings, unfamiliar domains)", bullet_style))
    elements.append(Paragraph("• Unexpected attachments or links, especially from unknown senders", bullet_style))
    elements.append(Paragraph("• Generic greetings (\"Dear Customer\") instead of your name", bullet_style))
    elements.append(Paragraph("• Poor grammar or spelling errors", bullet_style))

    elements.append(Paragraph("<b>Link and Attachment Safety</b>", heading2_style))
    elements.append(Paragraph("• Hover over links before clicking to verify the actual URL destination", bullet_style))
    elements.append(Paragraph("• Never download attachments from unknown senders", bullet_style))
    elements.append(Paragraph("• All attachments are automatically scanned, but remain cautious", bullet_style))
    elements.append(Paragraph("• When in doubt, verify requests through alternate communication channels (phone call)", bullet_style))

    elements.append(Paragraph("<b>Email Encryption and Usage</b>", heading2_style))
    elements.append(Paragraph("• Use email encryption for CONFIDENTIAL or SECRET data", bullet_style))
    elements.append(Paragraph("• Auto-forwarding to external email addresses is prohibited", bullet_style))
    elements.append(Paragraph("• Personal email use on company devices allowed only for incidental personal needs", bullet_style))
    elements.append(Paragraph("• Never send company data to personal email accounts", bullet_style))

    elements.append(PageBreak())

    # ========== SECTION 5: DEVICE SECURITY ==========
    elements.append(Paragraph("Section 5: Device Security", heading1_style))

    elements.append(Paragraph("<b>Laptop Security</b>", heading2_style))
    elements.append(Paragraph("• <b>Full Disk Encryption:</b> Mandatory on all company laptops (BitLocker for Windows, FileVault for macOS)", bullet_style))
    elements.append(Paragraph("• <b>Screen Lock:</b> Automatic lock after 5 minutes of inactivity", bullet_style))
    elements.append(Paragraph("• <b>Automatic Updates:</b> Operating system and security patches must be enabled", bullet_style))
    elements.append(Paragraph("• <b>Antivirus/EDR:</b> Company-approved endpoint detection and response software must remain active", bullet_style))
    elements.append(Paragraph("• <b>Lost/Stolen Devices:</b> Report immediately to IT Security (extension 5500) for remote wipe capability", bullet_style))
    elements.append(Paragraph("• <b>Physical Security:</b> Never leave laptops unattended in vehicles or public spaces", bullet_style))

    elements.append(Paragraph("<b>Mobile Devices</b>", heading2_style))
    elements.append(Paragraph("• <b>MDM Enrollment:</b> All devices accessing company email must enroll in Mobile Device Management", bullet_style))
    elements.append(Paragraph("• <b>Device Lock:</b> PIN (minimum 6 digits) or biometric authentication mandatory", bullet_style))
    elements.append(Paragraph("• <b>Data Segregation:</b> Company data stored in separate, encrypted container", bullet_style))
    elements.append(Paragraph("• <b>Lost Devices:</b> Can be remotely wiped to protect company data", bullet_style))
    elements.append(Paragraph("• <b>Updates:</b> Keep mobile OS and apps updated to latest versions", bullet_style))

    elements.append(Paragraph("<b>BYOD (Bring Your Own Device) Policy</b>", heading2_style))
    elements.append(Paragraph(
        "Personal devices may access company resources under the following conditions:",
        body_style
    ))
    elements.append(Paragraph("• Must meet minimum security standards (encryption, screen lock, updated OS)", bullet_style))
    elements.append(Paragraph("• Separate work profile required (enforced through MDM)", bullet_style))
    elements.append(Paragraph("• TechCorp reserves the right to remotely wipe work data only (not personal data)", bullet_style))
    elements.append(Paragraph("• Device must pass security compliance checks before access is granted", bullet_style))
    elements.append(Paragraph("• Employee responsible for device costs and maintenance", bullet_style))

    # ========== SECTION 6: NETWORK SECURITY ==========
    elements.append(Paragraph("Section 6: Network Security", heading1_style))

    elements.append(Paragraph("<b>VPN Usage</b>", heading2_style))
    elements.append(Paragraph("Virtual Private Network (VPN) usage is mandatory in these situations:", body_style))
    elements.append(Paragraph("• <b>Remote Work:</b> All connections to company resources from home or remote locations", bullet_style))
    elements.append(Paragraph("• <b>Public WiFi:</b> Any connection from coffee shops, airports, hotels, or public spaces", bullet_style))
    elements.append(Paragraph("• <b>Always-On VPN:</b> Preferred configuration for remote workers (automatically connects)", bullet_style))
    elements.append(Paragraph("• <b>Approved Clients:</b> Use only company-provided VPN software (Cisco AnyConnect, GlobalProtect)", bullet_style))

    elements.append(Paragraph("<b>WiFi Security</b>", heading2_style))
    elements.append(Paragraph("• <b>Public WiFi:</b> Never access company resources without VPN protection", bullet_style))
    elements.append(Paragraph("• <b>Home WiFi:</b> Must use WPA2 or WPA3 encryption (WEP and WPA are insecure)", bullet_style))
    elements.append(Paragraph("• <b>Default Passwords:</b> Change default router passwords to strong, unique passwords", bullet_style))
    elements.append(Paragraph("• <b>Guest Network:</b> Use separate guest network for personal/IoT devices at home", bullet_style))
    elements.append(Paragraph("• <b>SSID Broadcasting:</b> Hiding network name provides minimal security benefit", bullet_style))

    elements.append(Paragraph("<b>Network Access Controls</b>", heading2_style))
    elements.append(Paragraph("• <b>Authorized Devices Only:</b> Only company-approved devices may connect to corporate network", bullet_style))
    elements.append(Paragraph("• <b>Network Segmentation:</b> Guest WiFi is isolated from corporate resources", bullet_style))
    elements.append(Paragraph("• <b>IoT Devices:</b> Smart devices (cameras, thermostats) require IT approval before network connection", bullet_style))
    elements.append(Paragraph("• <b>Rogue Access Points:</b> Unauthorized WiFi routers/hotspots are strictly prohibited", bullet_style))

    elements.append(PageBreak())

    # ========== SECTION 7: PHYSICAL SECURITY ==========
    elements.append(Paragraph("Section 7: Physical Security", heading1_style))

    elements.append(Paragraph(
        "Physical security controls protect against unauthorized access to facilities and information. "
        "Digital security is ineffective if physical access is compromised.",
        body_style
    ))

    elements.append(Paragraph("<b>Clean Desk Policy</b>", heading2_style))
    elements.append(Paragraph("• Lock away sensitive documents when not in active use", bullet_style))
    elements.append(Paragraph("• Clear desk at end of day (no papers, USB drives, or notes left out)", bullet_style))
    elements.append(Paragraph("• Confidential printouts must be retrieved immediately from printers", bullet_style))
    elements.append(Paragraph("• Whiteboards with sensitive information must be erased after meetings", bullet_style))

    elements.append(Paragraph("<b>Visitor Management</b>", heading2_style))
    elements.append(Paragraph("• All visitors must sign in and receive visitor badges", bullet_style))
    elements.append(Paragraph("• Visitors must be escorted at all times in non-public areas", bullet_style))
    elements.append(Paragraph("• Visitors cannot access restricted areas (server rooms, data centers)", bullet_style))
    elements.append(Paragraph("• Challenge unescorted or unbadged individuals politely", bullet_style))

    elements.append(Paragraph("<b>Restricted Area Access</b>", heading2_style))
    elements.append(Paragraph("• <b>Server Rooms:</b> Authorized IT personnel only, badge access logged", bullet_style))
    elements.append(Paragraph("• <b>Data Centers:</b> Multi-factor authentication required (badge + PIN/biometric)", bullet_style))
    elements.append(Paragraph("• <b>Access Reviews:</b> Quarterly review of personnel with server room access", bullet_style))

    elements.append(Paragraph("<b>Document Disposal</b>", heading2_style))
    elements.append(Paragraph("• <b>Shredding Required:</b> All documents containing INTERNAL or higher classification", bullet_style))
    elements.append(Paragraph("• <b>Cross-Cut Shredders:</b> Available on each floor", bullet_style))
    elements.append(Paragraph("• <b>Media Destruction:</b> Hard drives and USB storage destroyed (not just deleted) before disposal", bullet_style))
    elements.append(Paragraph("• <b>Secure Bins:</b> Use locked disposal bins for documents awaiting shredding", bullet_style))

    elements.append(Paragraph("<b>Workspace Security</b>", heading2_style))
    elements.append(Paragraph("• Lock screens when stepping away from desk (Windows+L or Ctrl+Cmd+Q)", bullet_style))
    elements.append(Paragraph("• Do not share access badges or hold doors for unknown individuals", bullet_style))
    elements.append(Paragraph("• Report lost or stolen badges immediately", bullet_style))

    # ========== SECTION 8: INCIDENT RESPONSE ==========
    elements.append(Paragraph("Section 8: Incident Response", heading1_style))

    elements.append(Paragraph(
        "Quick reporting and response minimizes the impact of security incidents. "
        "TechCorp maintains a 24/7 incident response capability.",
        body_style
    ))

    elements.append(Paragraph("<b>What to Report</b>", heading2_style))
    elements.append(Paragraph("Report any of the following immediately:", body_style))
    elements.append(Paragraph("• <b>Phishing Attempts:</b> Suspicious emails requesting credentials or containing malicious links", bullet_style))
    elements.append(Paragraph("• <b>Lost/Stolen Devices:</b> Laptops, phones, tablets, USB drives, or access badges", bullet_style))
    elements.append(Paragraph("• <b>Data Breaches:</b> Unauthorized access, disclosure, or loss of company data", bullet_style))
    elements.append(Paragraph("• <b>Malware Infections:</b> Virus warnings, ransomware, unusual system behavior", bullet_style))
    elements.append(Paragraph("• <b>Unauthorized Access:</b> Suspicious login attempts, unknown users in systems", bullet_style))
    elements.append(Paragraph("• <b>Social Engineering:</b> Suspicious phone calls or visits requesting sensitive information", bullet_style))
    elements.append(Paragraph("• <b>System Anomalies:</b> Unexpected system crashes, slow performance, unusual network traffic", bullet_style))

    elements.append(Paragraph("<b>How to Report</b>", heading2_style))
    elements.append(Paragraph("• <b>Email:</b> security@techcorp.com (monitored 24/7)", bullet_style))
    elements.append(Paragraph("• <b>Phone:</b> IT Security Hotline - Extension 5500", bullet_style))
    elements.append(Paragraph("• <b>Phishing Button:</b> Use the \"Report Phishing\" button in Outlook", bullet_style))
    elements.append(Paragraph("• <b>Emergency After Hours:</b> Call main number and ask for on-call security engineer", bullet_style))

    elements.append(Paragraph("<b>Response Timeframe</b>", heading2_style))
    elements.append(Paragraph("• Report incidents within 1 hour of discovery", body_style))
    elements.append(Paragraph("• Critical incidents (data breach, ransomware) require immediate reporting", body_style))
    elements.append(Paragraph("• Do not attempt to investigate or remediate on your own - contact IT Security", body_style))

    elements.append(Paragraph("<b>No-Blame Reporting Culture</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp maintains a no-blame culture for good-faith security reports. Employees will not "
        "face penalties for accidentally clicking phishing links or reporting potential incidents that "
        "turn out to be false alarms. Early reporting is valued and encouraged.",
        body_style
    ))

    elements.append(PageBreak())

    # ========== SECTION 9: ACCEPTABLE USE ==========
    elements.append(Paragraph("Section 9: Acceptable Use Policy", heading1_style))

    elements.append(Paragraph(
        "TechCorp provides technology resources primarily for business purposes. "
        "Limited personal use is permitted within the guidelines below.",
        body_style
    ))

    elements.append(Paragraph("<b>Permitted Personal Use</b>", heading2_style))
    elements.append(Paragraph("• Incidental personal use during breaks (checking personal email, news)", bullet_style))
    elements.append(Paragraph("• Brief personal calls or messages", bullet_style))
    elements.append(Paragraph("• Personal use must not interfere with work responsibilities", bullet_style))
    elements.append(Paragraph("• Personal use must not consume significant bandwidth or storage", bullet_style))

    elements.append(Paragraph("<b>Prohibited Activities</b>", heading2_style))
    elements.append(Paragraph("The following activities are strictly forbidden on TechCorp systems:", body_style))
    elements.append(Paragraph("• <b>Illegal Content:</b> Accessing, storing, or distributing illegal materials", bullet_style))
    elements.append(Paragraph("• <b>Pirated Software:</b> Installing or using unlicensed software or media", bullet_style))
    elements.append(Paragraph("• <b>Torrenting/P2P:</b> File sharing applications and torrenting", bullet_style))
    elements.append(Paragraph("• <b>Cryptocurrency Mining:</b> Using company resources for cryptocurrency mining", bullet_style))
    elements.append(Paragraph("• <b>Offensive Material:</b> Accessing or distributing offensive, discriminatory, or harassing content", bullet_style))
    elements.append(Paragraph("• <b>Unauthorized Access:</b> Attempting to bypass security controls or access restricted systems", bullet_style))
    elements.append(Paragraph("• <b>Unauthorized Disclosure:</b> Sharing confidential company information externally", bullet_style))
    elements.append(Paragraph("• <b>Malicious Activity:</b> Deliberately introducing malware or disrupting systems", bullet_style))

    elements.append(Paragraph("<b>Monitoring Notice</b>", heading2_style))
    elements.append(Paragraph(
        "TechCorp reserves the right to monitor all activity on company systems and networks to ensure "
        "compliance with policies and investigate security incidents. Employees have no expectation of "
        "privacy when using company resources. Monitoring may include:",
        body_style
    ))
    elements.append(Paragraph("• Email content and metadata", bullet_style))
    elements.append(Paragraph("• Internet browsing history and downloads", bullet_style))
    elements.append(Paragraph("• Network traffic and bandwidth usage", bullet_style))
    elements.append(Paragraph("• File access and modifications", bullet_style))
    elements.append(Paragraph("• Application usage and performance", bullet_style))

    elements.append(Paragraph("<b>Software Installation</b>", heading2_style))
    elements.append(Paragraph("• Only IT-approved software may be installed on company devices", bullet_style))
    elements.append(Paragraph("• Submit software requests through IT Service Portal", bullet_style))
    elements.append(Paragraph("• All software must be properly licensed", bullet_style))
    elements.append(Paragraph("• Browser extensions require approval for security review", bullet_style))

    # ========== SECTION 10: PENALTIES ==========
    elements.append(Paragraph("Section 10: Penalties and Enforcement", heading1_style))

    elements.append(Paragraph(
        "Compliance with these security guidelines is mandatory. Violations will be addressed "
        "through the progressive discipline process outlined below.",
        body_style
    ))

    elements.append(Paragraph("<b>Progressive Discipline</b>", heading2_style))

    elements.append(Paragraph("<b>First Violation (Unintentional):</b>", body_style))
    elements.append(Paragraph("• Mandatory security awareness training (4-hour course)", bullet_style))
    elements.append(Paragraph("• Documented counseling session with manager", bullet_style))
    elements.append(Paragraph("• Violation recorded in employee file", bullet_style))
    elements.append(Paragraph("• 30-day probationary period with increased monitoring", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Second Violation:</b>", body_style))
    elements.append(Paragraph("• Written warning placed in employee file", bullet_style))
    elements.append(Paragraph("• Additional security training and certification required", bullet_style))
    elements.append(Paragraph("• 90-day probationary period", bullet_style))
    elements.append(Paragraph("• Potential restriction of system access privileges", bullet_style))
    elements.append(Paragraph("• Manager and HR consultation regarding performance", bullet_style))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>Third Violation:</b>", body_style))
    elements.append(Paragraph("• Consideration for termination of employment", bullet_style))
    elements.append(Paragraph("• Review by HR and Legal departments", bullet_style))
    elements.append(Paragraph("• Potential suspension pending investigation", bullet_style))

    elements.append(Paragraph("<b>Immediate Termination Offenses</b>", heading2_style))
    elements.append(Paragraph("The following violations may result in immediate termination without progressive discipline:", body_style))
    elements.append(Paragraph("• Intentional data breaches or theft of company information", bullet_style))
    elements.append(Paragraph("• Deliberately introducing malware or sabotaging systems", bullet_style))
    elements.append(Paragraph("• Sharing credentials or providing unauthorized access to external parties", bullet_style))
    elements.append(Paragraph("• Illegal activities using company resources", bullet_style))
    elements.append(Paragraph("• Gross negligence resulting in significant security incident", bullet_style))
    elements.append(Paragraph("• Repeated violations after written warning", bullet_style))

    elements.append(Paragraph("<b>Legal Consequences</b>", heading2_style))
    elements.append(Paragraph(
        "Certain security violations may also result in civil or criminal liability. TechCorp will "
        "cooperate with law enforcement investigations and may pursue legal action to recover damages "
        "caused by willful security policy violations.",
        body_style
    ))

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("<b>Acknowledgment</b>", heading2_style))
    elements.append(Paragraph(
        "All employees must acknowledge receipt and understanding of these IT Security Guidelines "
        "annually. Acknowledgment forms are managed through the HR portal. Questions regarding these "
        "policies should be directed to security@techcorp.com or your direct manager.",
        body_style
    ))

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("_______________________________________________", body_style))
    elements.append(Paragraph("<i>This document is classified as INTERNAL and is intended for TechCorp employees only.</i>",
                             ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
                                          textColor=colors.HexColor('#666666'), alignment=TA_CENTER)))

    # Build PDF
    doc.build(elements)
    print(f"PDF successfully created: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_it_security_pdf()
