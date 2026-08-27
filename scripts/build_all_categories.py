import os, json, re

# ==============================================================================
# ENRICHMENT DICTIONARY FOR BANKS & FINANCE
# ==============================================================================
banks_enrichment = {
  "State Bank of India": {"website": "https://sbi.co.in", "careers": "https://sbi.co.in/web/careers", "type": "Public Bank", "locations": "Pan India, Mumbai, Hyderabad, Bengaluru", "focus": "India's largest public sector bank & financial services conglomerate"},
  "HDFC Bank": {"website": "https://www.hdfcbank.com", "careers": "https://www.hdfcbank.com/personal/about-us/careers", "type": "Private Bank", "locations": "Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pan India", "focus": "Largest private sector bank providing retail & wholesale banking"},
  "ICICI Bank": {"website": "https://www.icicibank.com", "careers": "https://www.icicicareers.com", "type": "Private Bank", "locations": "Mumbai, Hyderabad, Bengaluru, Delhi NCR, Pan India", "focus": "Leading private bank with strong digital banking & wealth management"},
  "Axis Bank": {"website": "https://www.axisbank.com", "careers": "https://www.axisbank.com/careers", "type": "Private Bank", "locations": "Mumbai, Bengaluru, Hyderabad, Delhi NCR, Pan India", "focus": "Private sector bank providing retail, corporate & treasury banking"},
  "Kotak Mahindra Bank": {"website": "https://www.kotak.com", "careers": "https://www.kotak.com/en/careers.html", "type": "Private Bank", "locations": "Mumbai, Bengaluru, Hyderabad, Delhi NCR, Pan India", "focus": "Commercial banking, wealth management & investment services"},
  "IndusInd Bank": {"website": "https://www.indusind.com", "careers": "https://www.indusind.com/in/en/personal/careers.html", "type": "Private Bank", "locations": "Mumbai, Pune, Gurugram, Bengaluru, Pan India", "focus": "Consumer banking, vehicle finance & corporate banking"},
  "IDFC FIRST Bank": {"website": "https://www.idfcfirstbank.com", "careers": "https://www.idfcfirstbank.com/careers", "type": "Private Bank", "locations": "Mumbai, Bengaluru, Hyderabad, Chennai, Pan India", "focus": "Tech-first retail banking, credit cards & MSME loans"},
  "YES BANK": {"website": "https://www.yesbank.in", "careers": "https://www.yesbank.in/life-at-yes-bank/careers", "type": "Private Bank", "locations": "Mumbai, Gurugram, Bengaluru, Hyderabad, Pan India", "focus": "Corporate, retail & digital transaction banking"},
  "Federal Bank": {"website": "https://www.federalbank.co.in", "careers": "https://www.federalbank.co.in/careers", "type": "Private Bank", "locations": "Kochi, Bengaluru, Chennai, Mumbai, Hyderabad", "focus": "Retail & commercial banking with strong NRI services"},
  "RBL Bank": {"website": "https://www.rblbank.com", "careers": "https://www.rblbank.com/careers", "type": "Private Bank", "locations": "Mumbai, Pune, Bengaluru, Delhi NCR", "focus": "Commercial banking, credit cards & branch banking"},
  "Bandhan Bank": {"website": "https://bandhanbank.com", "careers": "https://bandhanbank.com/careers", "type": "Private Bank", "locations": "Kolkata, Mumbai, Bengaluru, Pan India", "focus": "Microfinance, retail banking & inclusive banking"},
  "South Indian Bank": {"website": "https://www.southindianbank.com", "careers": "https://www.southindianbank.com/careers", "type": "Private Bank", "locations": "Thrissur, Bengaluru, Chennai, Hyderabad, Mumbai", "focus": "Retail banking, MSME loans & personal financial services"},
  "City Union Bank": {"website": "https://www.cityunionbank.com", "careers": "https://www.cityunionbank.com/careers", "type": "Private Bank", "locations": "Kumbakonam, Chennai, Bengaluru, Hyderabad", "focus": "SME & retail banking services in South India"},
  "Karur Vysya Bank": {"website": "https://www.kvb.co.in", "careers": "https://www.kvb.co.in/careers/", "type": "Private Bank", "locations": "Karur, Chennai, Bengaluru, Hyderabad", "focus": "Commercial banking, agricultural & MSME loans"},
  "DCB Bank": {"website": "https://www.dcbbank.com", "careers": "https://www.dcbbank.com/careers", "type": "Private Bank", "locations": "Mumbai, Hyderabad, Bengaluru, Pan India", "focus": "Micro-SME, small business & retail banking"},
  "Dhanlaxmi Bank": {"website": "https://www.dhanbank.com", "careers": "https://www.dhanbank.com/careers", "type": "Private Bank", "locations": "Thrissur, Kochi, Bengaluru, Chennai", "focus": "Personal, corporate & microfinance banking"},
  "Tamilnad Mercantile Bank": {"website": "https://www.tmb.in", "careers": "https://www.tmb.in/careers", "type": "Private Bank", "locations": "Tuticorin, Chennai, Madurai, Bengaluru", "focus": "MSME, agricultural & retail banking services"},
  "Karnataka Bank": {"website": "https://karnatakabank.com", "careers": "https://karnatakabank.com/careers", "type": "Private Bank", "locations": "Mangaluru, Bengaluru, Hyderabad, Mumbai", "focus": "Commercial, retail & agricultural banking"},
  "Jammu & Kashmir Bank": {"website": "https://www.jkbank.com", "careers": "https://www.jkbank.com/careers", "type": "Private Bank", "locations": "Srinagar, Jammu, Delhi NCR, Mumbai", "focus": "Universal banking & government treasury banking"},
  "CSB Bank": {"website": "https://www.csb.co.in", "careers": "https://www.csb.co.in/careers", "type": "Private Bank", "locations": "Thrissur, Kochi, Chennai, Bengaluru, Mumbai", "focus": "SME, retail & gold loans banking"},
  "IDBI Bank": {"website": "https://www.idbibank.in", "careers": "https://www.idbibank.in/idbi-bank-careers.aspx", "type": "Public Bank", "locations": "Mumbai, Hyderabad, Bengaluru, Pan India", "focus": "Infrastructure financing, retail & corporate banking"},
  "Bank of Baroda": {"website": "https://www.bankofbaroda.in", "careers": "https://www.bankofbaroda.in/career", "type": "Public Bank", "locations": "Vadodara, Mumbai, Bengaluru, Hyderabad, Pan India", "focus": "Public sector banking & international operations"},
  "Punjab National Bank": {"website": "https://www.pnbindia.in", "careers": "https://www.pnbindia.in/recruitment.html", "type": "Public Bank", "locations": "New Delhi, Mumbai, Hyderabad, Pan India", "focus": "Public sector banking & corporate credit"},
  "Canara Bank": {"website": "https://canarabank.com", "careers": "https://canarabank.com/careers", "type": "Public Bank", "locations": "Bengaluru, Hyderabad, Mumbai, Pan India", "focus": "Public sector commercial banking & treasury"},
  "Union Bank of India": {"website": "https://www.unionbankofindia.co.in", "careers": "https://www.unionbankofindia.co.in/english/recruitment.aspx", "type": "Public Bank", "locations": "Mumbai, Hyderabad, Bengaluru, Pan India", "focus": "Public sector retail, MSME & agricultural banking"},
  "Bank of India": {"website": "https://bankofindia.co.in", "careers": "https://bankofindia.co.in/career", "type": "Public Bank", "locations": "Mumbai, Hyderabad, Bengaluru, Pan India", "focus": "Commercial & international banking"},
  "Indian Bank": {"website": "https://www.indianbank.in", "careers": "https://www.indianbank.in/career/", "type": "Public Bank", "locations": "Chennai, Hyderabad, Bengaluru, Pan India", "focus": "Public sector banking & microfinance"},
  "Central Bank of India": {"website": "https://www.centralbankofindia.co.in", "careers": "https://www.centralbankofindia.co.in/en/recruitment", "type": "Public Bank", "locations": "Mumbai, Hyderabad, Delhi NCR, Pan India", "focus": "Public commercial banking & retail credit"},
  "Indian Overseas Bank": {"website": "https://www.iob.in", "careers": "https://www.iob.in/Careers", "type": "Public Bank", "locations": "Chennai, Hyderabad, Bengaluru, Pan India", "focus": "Public banking & foreign exchange services"},
  "UCO Bank": {"website": "https://www.ucobank.com", "careers": "https://www.ucobank.com/english/job-opportunities.aspx", "type": "Public Bank", "locations": "Kolkata, Delhi NCR, Mumbai, Pan India", "focus": "Public commercial & international banking"},
  "Bank of Maharashtra": {"website": "https://bankofmaharashtra.in", "careers": "https://bankofmaharashtra.in/careers", "type": "Public Bank", "locations": "Pune, Mumbai, Hyderabad, Pan India", "focus": "Public retail & agricultural banking"},
  "Punjab & Sind Bank": {"website": "https://punjabandsindbank.co.in", "careers": "https://punjabandsindbank.co.in/content/recruitment", "type": "Public Bank", "locations": "New Delhi, Chandigarh, Pan India", "focus": "Public commercial banking"},
  "JPMorgan Chase": {"website": "https://www.jpmorganchase.com", "careers": "https://careers.jpmorganchase.com", "type": "Global Investment GCC", "locations": "Mumbai, Bengaluru, Hyderabad", "focus": "Investment Banking, Quantitative Finance & Tech GCC"},
  "Goldman Sachs": {"website": "https://www.goldmansachs.com", "careers": "https://www.goldmansachs.com/careers/", "type": "Global Investment GCC", "locations": "Bengaluru, Hyderabad", "focus": "Investment Banking, Asset Management & Engineering GCC"},
  "Morgan Stanley": {"website": "https://www.morganstanley.com", "careers": "https://www.morganstanley.com/about-us/careers", "type": "Global Investment GCC", "locations": "Mumbai, Bengaluru", "focus": "Wealth Management, Tech Platform Engineering & Analytics"},
  "Citi": {"website": "https://www.citigroup.com", "careers": "https://jobs.citi.com", "type": "Global Bank GCC", "locations": "Mumbai, Pune, Chennai, Bengaluru", "focus": "Institutional Clients Group, Consumer Banking & Tech GCC"},
  "Bank of America": {"website": "https://www.bankofamerica.com", "careers": "https://careers.bankofamerica.com", "type": "Global Bank GCC", "locations": "Hyderabad, Mumbai, Gurugram, Chennai", "focus": "Global Technology & Operations (BofA Securities GCC)"},
  "Barclays": {"website": "https://home.barclays", "careers": "https://search.jobs.barclays", "type": "Global Bank GCC", "locations": "Pune, Chennai, Mumbai", "focus": "Global Technology Centre, Investment Banking & Operations"},
  "HSBC": {"website": "https://www.hsbc.com", "careers": "https://www.hsbc.com/careers", "type": "Global Bank GCC", "locations": "Hyderabad, Bengaluru, Pune, Gurugram, Mumbai", "focus": "Global Service Centres, Digital Banking & Risk Tech"},
  "Standard Chartered": {"website": "https://www.sc.com", "careers": "https://www.sc.com/en/careers/", "type": "Global Bank GCC", "locations": "Chennai, Bengaluru, Mumbai", "focus": "Global Business Services, Wealth Management & Tech"},
  "Deutsche Bank": {"website": "https://www.db.com", "careers": "https://www.db.com/careers", "type": "Global Bank GCC", "locations": "Pune, Bengaluru, Mumbai", "focus": "Corporate Bank, Investment Bank Tech & Operations"},
  "UBS": {"website": "https://www.ubs.com", "careers": "https://www.ubs.com/global/en/careers.html", "type": "Global Investment GCC", "locations": "Pune, Mumbai, Hyderabad", "focus": "Global Wealth Management, Risk & Financial Engineering"},
  "BNP Paribas": {"website": "https://group.bnpparibas", "careers": "https://group.bnpparibas/en/careers", "type": "Global Bank GCC", "locations": "Mumbai, Chennai, Bengaluru", "focus": "Corporate & Institutional Banking GCC"},
  "Societe Generale": {"website": "https://www.societegenerale.com", "careers": "https://careers.societegenerale.com", "type": "Global Bank GCC", "locations": "Bengaluru, Chennai", "focus": "Global Solution Centre, Investment Banking & Cloud Tech"},
  "Credit Suisse / UBS": {"website": "https://www.credit-suisse.com", "careers": "https://www.credit-suisse.com/careers", "type": "Global Investment GCC", "locations": "Pune, Mumbai", "focus": "Private Banking, Wealth Management & Technology"},
  "Wells Fargo": {"website": "https://www.wellsfargo.com", "careers": "https://www.wellsfargo.com/about/careers/", "type": "Global Bank GCC", "locations": "Hyderabad, Bengaluru", "focus": "Enterprise Global Services, AI/ML & Core Banking Tech"},
  "Fidelity Investments": {"website": "https://www.fidelity.com", "careers": "https://jobs.fidelity.com", "type": "Global Asset Mgmt GCC", "locations": "Bengaluru, Chennai", "focus": "Investment Technology, Asset Management & Operations"},
  "Northern Trust": {"website": "https://www.northerntrust.com", "careers": "https://careers.northerntrust.com", "type": "Global Asset Mgmt GCC", "locations": "Bengaluru, Pune", "focus": "Asset Servicing, Wealth Management & Financial Tech"},
  "State Street": {"website": "https://www.statestreet.com", "careers": "https://www.statestreet.com/en/careers", "type": "Global Asset Mgmt GCC", "locations": "Bengaluru, Hyderabad, Mumbai", "focus": "Custody Banking, Asset Servicing & Investment Analytics"},
  "BNY Mellon": {"website": "https://www.bnymellon.com", "careers": "https://www.bnymellon.com/us/en/careers.html", "type": "Global Asset Mgmt GCC", "locations": "Pune, Chennai", "focus": "Investment Management, Asset Servicing & Technology"},
  "BlackRock": {"website": "https://www.blackrock.com", "careers": "https://careers.blackrock.com", "type": "Global Asset Mgmt GCC", "locations": "Gurugram, Mumbai, Bengaluru", "focus": "Aladdin Platform Engineering, Risk Analytics & Asset Mgmt"},
  "Razorpay": {"website": "https://razorpay.com", "careers": "https://razorpay.com/jobs/", "type": "Fintech", "locations": "Bengaluru", "focus": "Payment Gateway, Neobanking, Payroll & Corporate Credit"},
  "PhonePe": {"website": "https://www.phonepe.com", "careers": "https://www.phonepe.com/careers/", "type": "Fintech", "locations": "Bengaluru, Pune", "focus": "UPI Payments, Insurance Tech, Mutual Funds & Merchant Solutions"},
  "Paytm": {"website": "https://paytm.com", "careers": "https://paytm.com/careers", "type": "Fintech", "locations": "Noida, Bengaluru, Mumbai", "focus": "Digital Payments, Soundbox POS & Financial Services"},
  "BharatPe": {"website": "https://bharatpe.com", "careers": "https://bharatpe.com/careers", "type": "Fintech", "locations": "Delhi NCR, Bengaluru", "focus": "Merchant QR Payments, POS & Small Business Loans"},
  "CRED": {"website": "https://cred.club", "careers": "https://cred.club/careers", "type": "Fintech", "locations": "Bengaluru", "focus": "Credit Card Payments, Premium Rewards & Financial Tech"},
  "Policybazaar": {"website": "https://www.policybazaar.com", "careers": "https://www.policybazaar.com/careers/", "type": "InsurTech", "locations": "Gurugram, Mumbai", "focus": "Insurance Aggregation, Health & Life Insurance Platform"},
  "Groww": {"website": "https://groww.in", "careers": "https://groww.in/careers", "type": "Fintech", "locations": "Bengaluru", "focus": "Direct Mutual Funds, Stock Broking & Wealth Management"},
  "Zerodha": {"website": "https://zerodha.com", "careers": "https://zerodha.com/careers", "type": "Fintech", "locations": "Bengaluru", "focus": "Discount Broking, Kite Trading Platform & Financial Literacy"},
  "Pine Labs": {"website": "https://www.pinelabs.com", "careers": "https://www.pinelabs.com/careers", "type": "Fintech", "locations": "Noida, Mumbai, Bengaluru", "focus": "Merchant Commerce Solutions, Buy Now Pay Later (BNPL)"},
  "Slice": {"website": "https://sliceit.com", "careers": "https://sliceit.com/careers", "type": "Fintech", "locations": "Bengaluru", "focus": "Consumer Credit Cards & Digital Banking Apps"},
  "Mswipe": {"website": "https://www.mswipe.com", "careers": "https://www.mswipe.com/careers", "type": "Fintech", "locations": "Mumbai, Bengaluru", "focus": "POS Terminal Devices & Merchant Payment Solutions"},
  "Acko Insurance": {"website": "https://www.acko.com", "careers": "https://www.acko.com/careers/", "type": "InsurTech", "locations": "Bengaluru, Mumbai", "focus": "Digital Motor, Health & Micro Insurance Products"},
  "Digit Insurance": {"website": "https://www.godigit.com", "careers": "https://www.godigit.com/careers", "type": "InsurTech", "locations": "Bengaluru, Pune", "focus": "General Insurance Products & Tech-Driven Claims Processing"}
}

# ==============================================================================
# ENRICHMENT DICTIONARY FOR IT & TECH
# ==============================================================================
it_enrichment = {
  "Tata Consultancy Services (TCS)": {"website": "https://www.tcs.com", "careers": "https://www.tcs.com/careers", "type": "IT Services", "locations": "Mumbai, Bengaluru, Hyderabad, Chennai, Pune", "focus": "Global IT Consulting, Enterprise Cloud, AI & Digital Solutions"},
  "Infosys": {"website": "https://www.infosys.com", "careers": "https://www.infosys.com/careers.html", "type": "IT Services", "locations": "Bengaluru, Mysuru, Hyderabad, Pune, Chennai", "focus": "Next-Gen Digital Services, AI Platforms & Cloud Consulting"},
  "HCLTech": {"website": "https://www.hcltech.com", "careers": "https://www.hcltech.com/careers", "type": "IT Services", "locations": "Noida, Bengaluru, Chennai, Hyderabad, Pune", "focus": "Engineering & R&D Services, Software Products & Digital Tech"},
  "Wipro": {"website": "https://www.wipro.com", "careers": "https://careers.wipro.com", "type": "IT Services", "locations": "Bengaluru, Hyderabad, Chennai, Pune, Noida", "focus": "Cognitive Computing, Cybersecurity, Cloud & Infrastructure"},
  "Tech Mahindra": {"website": "https://www.techmahindra.com", "careers": "https://careers.techmahindra.com", "type": "IT Services", "locations": "Pune, Hyderabad, Bengaluru, Mumbai, Chennai", "focus": "5G Telecom Networks, AI Solutions & Digital Transformation"},
  "LTIMindtree": {"website": "https://www.ltimindtree.com", "careers": "https://www.ltimindtree.com/careers/", "type": "IT Services", "locations": "Mumbai, Bengaluru, Pune, Hyderabad, Chennai", "focus": "Enterprise Cloud, Data Analytics & Digital Engineering"},
  "Mphasis": {"website": "https://www.mphasis.com", "careers": "https://www.mphasis.com/home/careers.html", "type": "IT Services", "locations": "Bengaluru, Pune, Mumbai, Hyderabad, Chennai", "focus": "Cloud & Cognitive Services for Banking & Capital Markets"},
  "Persistent Systems": {"website": "https://www.persistent.com", "careers": "https://www.persistent.com/careers/", "type": "IT Services", "locations": "Pune, Hyderabad, Bengaluru, Goa, Nagpur", "focus": "Digital Product Engineering, Cloud & Enterprise AI"},
  "Coforge": {"website": "https://www.coforge.com", "careers": "https://www.coforge.com/careers", "type": "IT Services", "locations": "Noida, Bengaluru, Hyderabad, Mumbai, Pune", "focus": "Insurance, Banking & Travel Technology Solutions"},
  "Hexaware Technologies": {"website": "https://hexaware.com", "careers": "https://hexaware.com/careers/", "type": "IT Services", "locations": "Mumbai, Chennai, Bengaluru, Pune, Noida", "focus": "Automation-Led IT & Business Process Services"},
  "Cyient": {"website": "https://www.cyient.com", "careers": "https://www.cyient.com/careers", "type": "Engineering R&D", "locations": "Hyderabad, Bengaluru, Pune, Visakhapatnam", "focus": "Intelligent Engineering, Aerospace, Telecom & Geospatial"},
  "Birlasoft": {"website": "https://www.birlasoft.com", "careers": "https://www.birlasoft.com/careers", "type": "IT Services", "locations": "Pune, Noida, Hyderabad, Bengaluru", "focus": "Enterprise ERP (SAP/Oracle), Cloud & Digital Transformation"},
  "Zensar Technologies": {"website": "https://www.zensar.com", "careers": "https://www.zensar.com/careers", "type": "IT Services", "locations": "Pune, Bengaluru, Hyderabad", "focus": "Digital Engineering, Experience Services & Data Engineering"},
  "Sonata Software": {"website": "https://www.sonata-software.com", "careers": "https://www.sonata-software.com/careers", "type": "IT Services", "locations": "Bengaluru, Hyderabad", "focus": "Modernization Engineering, Cloud & Retail Technology"},
  "Tata Elxsi": {"website": "https://www.tataelxsi.com", "careers": "https://www.tataelxsi.com/careers", "type": "Engineering R&D", "locations": "Bengaluru, Trivandrum, Pune, Hyderabad, Chennai", "focus": "Automotive Design, Autonomous Driving, Broadcast & Healthcare Tech"},
  "KPIT Technologies": {"website": "https://www.kpit.com", "careers": "https://www.kpit.com/careers/", "type": "Automotive Tech", "locations": "Pune, Bengaluru, Kochi", "focus": "Software-Defined Vehicles (SDV), EV Power Train & Autonomous"},
  "Mastek": {"website": "https://www.mastek.com", "careers": "https://www.mastek.com/careers/", "type": "IT Services", "locations": "Mumbai, Pune, Ahmedabad, Chennai", "focus": "Digital Commerce, Oracle Cloud Solutions & Public Sector IT"},
  "Happiest Minds": {"website": "https://www.happiestminds.com", "careers": "https://www.happiestminds.com/careers/", "type": "IT Services", "locations": "Bengaluru, Pune, Hyderabad", "focus": "AI, Internet of Things (IoT), Cloud & Cybersecurity"},
  "ITC Infotech": {"website": "https://www.itcinfotech.com", "careers": "https://www.itcinfotech.com/careers/", "type": "IT Services", "locations": "Bengaluru, Kolkata, Pune", "focus": "Digital Supply Chain, Industry 4.0 & Enterprise Automation"},
  "Accenture": {"website": "https://www.accenture.com", "careers": "https://www.accenture.com/in-en/careers", "type": "Global Consulting", "locations": "Bengaluru, Hyderabad, Mumbai, Pune, Chennai", "focus": "Strategy, Technology Consulting, AI Platforms & Cloud Operations"},
  "Cognizant": {"website": "https://www.cognizant.com", "careers": "https://careers.cognizant.com/in/en", "type": "Global IT Services", "locations": "Chennai, Bengaluru, Hyderabad, Pune, Kolkata", "focus": "Digital Business Transformation, Healthcare IT & AI Engineering"},
  "Capgemini": {"website": "https://www.capgemini.com", "careers": "https://www.capgemini.com/in-en/careers/", "type": "Global IT Services", "locations": "Mumbai, Bengaluru, Pune, Hyderabad, Chennai", "focus": "Custom Systems Integration, Cloud & Intelligent Industry"},
  "IBM India": {"website": "https://www.ibm.com", "careers": "https://www.ibm.com/in-en/careers", "type": "Global Product & Consulting", "locations": "Bengaluru, Hyderabad, Pune, Kochi, Cyberabad", "focus": "Hybrid Cloud (Red Hat), Mainframe, Quantum & Watson AI"},
  "Microsoft India": {"website": "https://www.microsoft.com", "careers": "https://careers.microsoft.com", "type": "Global Product", "locations": "Hyderabad, Bengaluru, Noida", "focus": "Azure Cloud, Copilot AI, Developer Tools & Windows"},
  "Google India": {"website": "https://about.google", "careers": "https://careers.google.com", "type": "Global Product", "locations": "Bengaluru, Hyderabad, Gurugram, Mumbai", "focus": "Google Cloud, Search, Android, AI/ML & Infrastructure"},
  "Amazon Development Centre": {"website": "https://www.amazon.jobs", "careers": "https://www.amazon.jobs", "type": "Global Product", "locations": "Bengaluru, Hyderabad, Chennai, Delhi NCR", "focus": "AWS Cloud Services, E-commerce Logistics, Alexa & AI"},
  "Oracle India": {"website": "https://www.oracle.com", "careers": "https://www.oracle.com/corporate/careers/", "type": "Global Product", "locations": "Bengaluru, Hyderabad, Noida, Pune", "focus": "Oracle Cloud Infrastructure (OCI), Database Engines & ERP"},
  "SAP Labs India": {"website": "https://www.sap.com", "careers": "https://jobs.sap.com", "type": "Global Product", "locations": "Bengaluru, Gurugram, Pune, Hyderabad", "focus": "S/4HANA ERP, Business AI & Cloud Platform Solutions"},
  "Adobe India": {"website": "https://www.adobe.com", "careers": "https://www.adobe.com/careers.html", "type": "Global Product", "locations": "Noida, Bengaluru", "focus": "Creative Cloud, Photoshop, Document Cloud & Experience Platform"},
  "Cisco Systems India": {"website": "https://www.cisco.com", "careers": "https://jobs.cisco.com", "type": "Global Product", "locations": "Bengaluru, Pune, Hyderabad", "focus": "Networking Hardware, Webex, Cybersecurity & Cloud Mesh"},
  "Intel India": {"website": "https://www.intel.com", "careers": "https://jobs.intel.com", "type": "Semiconductor / Hardware", "locations": "Bengaluru, Hyderabad", "focus": "Processor Design, Silicon R&D, Graphics & AI Chips"},
  "AMD India": {"website": "https://www.amd.com", "careers": "https://jobs.amd.com", "type": "Semiconductor / Hardware", "locations": "Bengaluru, Hyderabad", "focus": "CPU/GPU Hardware Design, Ryzen, EPYC & AI Accelerators"},
  "NVIDIA India": {"website": "https://www.nvidia.com", "careers": "https://www.nvidia.com/en-us/about-nvidia/careers/", "type": "Semiconductor / AI", "locations": "Bengaluru, Pune, Hyderabad", "focus": "GPU Compute Architecture, CUDA, Autonomous Vehicles & AI"},
  "Qualcomm India": {"website": "https://www.qualcomm.com", "careers": "https://www.qualcomm.com/company/careers", "type": "Semiconductor / Telecom", "locations": "Hyderabad, Bengaluru, Chennai", "focus": "Snapdragon Chips, 5G Wireless Modem R&D & IoT Silicon"},
  "Salesforce India": {"website": "https://www.salesforce.com", "careers": "https://careers.salesforce.com", "type": "SaaS / Cloud", "locations": "Hyderabad, Bengaluru, Mumbai", "focus": "CRM Cloud, Customer 360, Einstein AI & Slack Integration"},
  "ServiceNow India": {"website": "https://www.servicenow.com", "careers": "https://careers.servicenow.com", "type": "SaaS / Cloud", "locations": "Hyderabad, Bengaluru", "focus": "IT Service Management (ITSM), Workflow Automation & AI"},
  "Intuit India": {"website": "https://www.intuit.com", "careers": "https://www.intuit.com/careers/", "type": "SaaS / Product", "locations": "Bengaluru", "focus": "TurboTax, QuickBooks, Mailchimp & Credit Karma Platform"},
  "Atlassian India": {"website": "https://www.atlassian.com", "careers": "https://www.atlassian.com/company/careers", "type": "SaaS / Product", "locations": "Bengaluru", "focus": "Jira, Confluence, Trello, Bitbucket & Developer Tools"},
  "Zoho Corporation": {"website": "https://www.zoho.com", "careers": "https://www.zoho.com/careers/", "type": "SaaS / Product", "locations": "Chennai, Tenkasi, Bengaluru", "focus": "Zoho CRM, Workplace Suite, Books & Cloud Business Operating System"},
  "Freshworks": {"website": "https://www.freshworks.com", "careers": "https://www.freshworks.com/careers/", "type": "SaaS / Product", "locations": "Chennai, Bengaluru", "focus": "Freshdesk, Freshservice, Customer Service & ITSM SaaS"},
  "Postman": {"website": "https://www.postman.com", "careers": "https://www.postman.com/careers/", "type": "SaaS / Product", "locations": "Bengaluru", "focus": "API Development Platform & Developer Collaboration Suite"},
  "BrowserStack": {"website": "https://www.browserstack.com", "careers": "https://www.browserstack.com/careers", "type": "SaaS / Product", "locations": "Mumbai, Bengaluru", "focus": "Cross-Browser Testing Cloud & Mobile App Automation"}
}

# ==============================================================================
# ENRICHMENT DICTIONARY FOR HEALTHCARE
# ==============================================================================
health_enrichment = {
  "Apollo Hospitals": {"website": "https://www.apollohospitals.com", "careers": "https://www.apollohospitals.com/careers/", "type": "Hospital Chain", "locations": "Hyderabad, Chennai, Bengaluru, Mumbai, Delhi NCR, Pan India", "focus": "Asia's largest healthcare group providing multi-specialty hospital care"},
  "Fortis Healthcare": {"website": "https://www.fortishealthcare.com", "careers": "https://www.fortishealthcare.com/careers", "type": "Hospital Chain", "locations": "Delhi NCR, Bengaluru, Mumbai, Hyderabad, Pan India", "focus": "Integrated healthcare delivery service provider with super-specialty hospitals"},
  "Manipal Hospitals": {"website": "https://www.manipalhospitals.com", "careers": "https://www.manipalhospitals.com/careers/", "type": "Hospital Chain", "locations": "Bengaluru, Hyderabad, Pune, Delhi NCR, Mumbai, Pan India", "focus": "Leading multi-specialty healthcare network with tertiary care facilities"},
  "Max Healthcare": {"website": "https://www.maxhealthcare.in", "careers": "https://www.maxhealthcare.in/careers", "type": "Hospital Chain", "locations": "Delhi NCR, Mumbai, Dehradun, Pan India", "focus": "Premier medical care in Oncology, Cardiology & Transplant Surgeries"},
  "Narayana Health": {"website": "https://www.narayanahealth.org", "careers": "https://www.narayanahealth.org/careers", "type": "Hospital Chain", "locations": "Bengaluru, Hyderabad, Kolkata, Jaipur, Pan India", "focus": "Affordable cardiac care, organ transplants & multi-specialty medicine"},
  "Aster DM Healthcare": {"website": "https://www.asterdmhealthcare.com", "careers": "https://www.asterdmhealthcare.com/careers", "type": "Hospital Chain", "locations": "Bengaluru, Hyderabad, Kerala, Mumbai", "focus": "Integrated healthcare network with hospitals, clinics & pharmacies"},
  "KIMS Hospitals": {"website": "https://www.kimshospitals.com", "careers": "https://www.kimshospitals.com/careers/", "type": "Hospital Chain", "locations": "Hyderabad, Secunderabad, Visakhapatnam, Bengaluru", "focus": "Krishna Institute of Medical Sciences - Leading tertiary hospital network"},
  "Yashoda Hospitals": {"website": "https://www.yashodahospitals.com", "careers": "https://www.yashodahospitals.com/careers/", "type": "Hospital Chain", "locations": "Hyderabad, Secunderabad", "focus": "Super-specialty medical care, robotics surgery & oncology"},
  "CARE Hospitals": {"website": "https://www.carehospitals.com", "careers": "https://www.carehospitals.com/careers/", "type": "Hospital Chain", "locations": "Hyderabad, Bengaluru, Bhubaneswar, Raipur, Vizag", "focus": "Multi-specialty cardiac care, neurology & critical care medicine"},
  "Continental Hospitals": {"website": "https://continentalhospitals.com", "careers": "https://continentalhospitals.com/careers/", "type": "Hospital Chain", "locations": "Hyderabad", "focus": "JCI accredited super-specialty tertiary care hospital"},
  "Sunshine Hospitals": {"website": "https://www.sunshinehospitals.com", "careers": "https://www.sunshinehospitals.com/careers/", "type": "Hospital Chain", "locations": "Hyderabad, Secunderabad", "focus": "Joint replacement, orthopedics & trauma care specialty"},
  "Medicover Hospitals India": {"website": "https://www.medicoverhospitals.in", "careers": "https://www.medicoverhospitals.in/careers", "type": "Hospital Chain", "locations": "Hyderabad, Pune, Bengaluru, Vizag, Nashik", "focus": "European standard healthcare delivery network in South & West India"},
  "Rainbow Children's Hospital": {"website": "https://www.rainbowhospitals.in", "careers": "https://www.rainbowhospitals.in/careers", "type": "Pediatric Hospital", "locations": "Hyderabad, Bengaluru, Chennai, Delhi NCR", "focus": "India's leading pediatric & perinatal specialty hospital chain"},
  "MGM Healthcare": {"website": "https://mgmhealthcare.in", "careers": "https://mgmhealthcare.in/careers/", "type": "Hospital Chain", "locations": "Chennai, Pondicherry", "focus": "Quaternary care super-specialty hospital & heart-lung transplantation"},
  "Gleneagles Hospitals India": {"website": "https://www.gleneagles-hospitals.in", "careers": "https://www.gleneagles-hospitals.in/careers", "type": "Hospital Chain", "locations": "Mumbai, Hyderabad, Bengaluru, Chennai", "focus": "Part of IHH Healthcare - Quaternary medical services & organ transplant"},
  "Cloudnine Hospitals": {"website": "https://www.cloudninehospitals.com", "careers": "https://www.cloudninehospitals.com/careers", "type": "Maternity Hospital", "locations": "Bengaluru, Hyderabad, Mumbai, Pune, Chennai, Delhi NCR", "focus": "Specialty maternity, fertility & pediatric healthcare chain"},
  "Motherhood Hospitals": {"website": "https://www.motherhoodhospitals.com", "careers": "https://www.motherhoodhospitals.com/careers/", "type": "Maternity Hospital", "locations": "Bengaluru, Hyderabad, Chennai, Pune, Mumbai", "focus": "Women & children's specialty health network"},
  "Dr. Agarwal's Eye Hospital": {"website": "https://www.dragarwal.com", "careers": "https://www.dragarwal.com/careers/", "type": "Eye Care Chain", "locations": "Chennai, Hyderabad, Bengaluru, Pan India", "focus": "Ophthalmology chain offering advanced cataract & LASIK surgery"},
  "Centre for Sight": {"website": "https://www.centreforsight.net", "careers": "https://www.centreforsight.net/careers/", "type": "Eye Care Chain", "locations": "Delhi NCR, Hyderabad, Bengaluru, Pan India", "focus": "Specialty eye care, cornea treatment & refractive surgery"},
  "LV Prasad Eye Institute": {"website": "https://www.lvpei.org", "careers": "https://www.lvpei.org/careers", "type": "Non-Profit Eye Institute", "locations": "Hyderabad, Bhubaneswar, Visakhapatnam, Vijayawada", "focus": "WHO collaborating center for eye care, corneal transplantation & research"},
  "Dr Lal PathLabs": {"website": "https://www.lalpathlabs.com", "careers": "https://www.lalpathlabs.com/careers", "type": "Diagnostics Chain", "locations": "Delhi NCR, Pan India", "focus": "India's largest diagnostic test laboratory network"},
  "Metropolis Healthcare": {"website": "https://www.metropolisindia.com", "careers": "https://www.metropolisindia.com/careers", "type": "Diagnostics Chain", "locations": "Mumbai, Bengaluru, Hyderabad, Chennai, Pan India", "focus": "Pathology & diagnostic centers offering comprehensive health checks"},
  "Thyrocare Technologies": {"website": "https://www.thyrocare.com", "careers": "https://www.thyrocare.com/careers", "type": "Diagnostics Chain", "locations": "Mumbai, Pan India", "focus": "Automated preventive health diagnostic lab operator"},
  "Vijaya Diagnostic Centre": {"website": "https://www.vijayadiagnostic.com", "careers": "https://www.vijayadiagnostic.com/careers", "type": "Diagnostics Chain", "locations": "Hyderabad, Bengaluru, Chennai, Vizag", "focus": "Integrated pathology & radiology diagnostic services"},
  "PharmEasy": {"website": "https://pharmeasy.in", "careers": "https://pharmeasy.in/careers", "type": "HealthTech / E-Pharmacy", "locations": "Mumbai, Bengaluru", "focus": "Online pharmacy delivery, teleconsultation & diagnostic test booking"},
  "Tata 1mg": {"website": "https://www.1mg.com", "careers": "https://www.1mg.com/jobs", "type": "HealthTech / E-Pharmacy", "locations": "Gurugram, Bengaluru", "focus": "Digital healthcare platform, medicine delivery & lab testing"},
  "Cult.fit": {"website": "https://www.cult.fit", "careers": "https://www.cult.fit/careers", "type": "HealthTech / Fitness", "locations": "Bengaluru", "focus": "Fitness centers, digital wellness apps & sports nutrition"}
}

def build_category_md(title, description, file_path, enrichment_map, raw_data_list):
  md_lines = [
    f"# {title}",
    "",
    description,
    "",
    "> **How to edit on GitHub**: Click the pencil ✏️ icon at the top right of this file, add or edit a company line in the table below, and click **Propose changes** to submit a Pull Request!",
    "",
    "| ID | Company Name | Official Website | Careers Portal | India Locations | Type | Key Focus / Notes |",
    "|---|---|---|---|---|---|---|"
  ]

  count = 1
  seen_names = set()

  # First process enriched items
  for name, info in enrichment_map.items():
    if name in seen_names:
      continue
    seen_names.add(name)
    
    web_link = f"[Website]({info['website']})"
    car_link = f"[Careers Portal]({info['careers']})"
    type_badge = f"`{info['type']}`"
    
    md_lines.append(f"| {count} | **{name}** | {web_link} | {car_link} | {info['locations']} | {type_badge} | {info['focus']} |")
    count += 1

  fs_content = '\n'.join(md_lines)
  with open(file_path, 'w', encoding='utf8') as f:
    f.write(fs_content)

  print(f"[OK] Generated {file_path} with {count-1} entries.")

# Generate finance.md, tech.md, healthcare.md
os.makedirs('companies', exist_ok=True)

build_category_md(
  "Banking, Finance & Fintech Companies in India",
  "A curated list of top **Public & Private Banks, Global Investment GCCs, Asset Management, InsurTech, and Fintechs** operating in India with verified career links and office locations.",
  "companies/finance.md",
  banks_enrichment,
  []
)

build_category_md(
  "IT & Software Companies in India",
  "A curated list of top **IT Services, Product MNCs, SaaS, Cloud, Semiconductor & Engineering R&D** operating in India with verified career links and GCC office locations.",
  "companies/tech.md",
  it_enrichment,
  []
)

build_category_md(
  "Hospitals, Diagnostics & HealthTech Companies in India",
  "A curated list of top **Hospital Chains, Diagnostic Networks, Eyecare Specialty, MedTech Equipment & HealthTech Platforms** operating in India.",
  "companies/healthcare.md",
  health_enrichment,
  []
)

