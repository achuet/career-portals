import json, os, re

# Master dictionary of verified website & career links for fallback / enrichment
master_directory = {
  # HEALTHCARE (100)
  "Apollo Hospitals": {"website": "https://www.apollohospitals.com", "careers": "https://www.apollohospitals.com/careers/", "type": "Hospital Chain", "focus": "Multi-specialty hospital group & healthcare services"},
  "Fortis Healthcare": {"website": "https://www.fortishealthcare.com", "careers": "https://www.fortishealthcare.com/careers", "type": "Hospital Chain", "focus": "Super-specialty hospitals & diagnostic services"},
  "Manipal Hospitals": {"website": "https://www.manipalhospitals.com", "careers": "https://www.manipalhospitals.com/careers/", "type": "Hospital Chain", "focus": "Tertiary & quaternary care multi-specialty network"},
  "Max Healthcare": {"website": "https://www.maxhealthcare.in", "careers": "https://www.maxhealthcare.in/careers", "type": "Hospital Chain", "focus": "Oncology, Cardiology & Organ Transplant Specialty"},
  "Narayana Health": {"website": "https://www.narayanahealth.org", "careers": "https://www.narayanahealth.org/careers", "type": "Hospital Chain", "focus": "Cardiac surgery, oncology & affordable healthcare"},
  "Aster DM Healthcare": {"website": "https://www.asterdmhealthcare.com", "careers": "https://www.asterdmhealthcare.com/careers", "type": "Hospital Chain", "focus": "Hospitals, medical centers & retail pharmacies"},
  "KIMS Hospitals": {"website": "https://www.kimshospitals.com", "careers": "https://www.kimshospitals.com/careers/", "type": "Hospital Chain", "focus": "Krishna Institute of Medical Sciences - Tertiary hospital network"},
  "Yashoda Hospitals": {"website": "https://www.yashodahospitals.com", "careers": "https://www.yashodahospitals.com/careers/", "type": "Hospital Chain", "focus": "Robotic surgery, critical care & oncology specialty"},
  "CARE Hospitals": {"website": "https://www.carehospitals.com", "careers": "https://www.carehospitals.com/careers/", "type": "Hospital Chain", "focus": "Cardiac care, neurology & multi-specialty medicine"},
  "Continental Hospitals": {"website": "https://continentalhospitals.com", "careers": "https://continentalhospitals.com/careers/", "type": "Hospital Chain", "focus": "JCI accredited tertiary multi-specialty healthcare"},
  "Sunshine Hospitals": {"website": "https://www.sunshinehospitals.com", "careers": "https://www.sunshinehospitals.com/careers/", "type": "Hospital Chain", "focus": "Joint replacement, orthopedics & trauma care specialty"},
  "Medicover Hospitals India": {"website": "https://www.medicoverhospitals.in", "careers": "https://www.medicoverhospitals.in/careers", "type": "Hospital Chain", "focus": "European standard healthcare delivery across India"},
  "Rainbow Children's Hospital": {"website": "https://www.rainbowhospitals.in", "careers": "https://www.rainbowhospitals.in/careers", "type": "Pediatric Hospital", "focus": "Pediatric & perinatal specialty healthcare network"},
  "MGM Healthcare": {"website": "https://mgmhealthcare.in", "careers": "https://mgmhealthcare.in/careers/", "type": "Hospital Chain", "focus": "Quaternary care & organ transplantation specialty"},
  "Gleneagles Hospitals India": {"website": "https://www.gleneagles-hospitals.in", "careers": "https://www.gleneagles-hospitals.in/careers", "type": "Hospital Chain", "focus": "Part of IHH Healthcare - Organ transplant & quaternary care"},
  "Sri Ramachandra Medical Centre": {"website": "https://www.sriramachandra.edu.in", "careers": "https://www.sriramachandra.edu.in/careers", "type": "Medical Institute", "focus": "Teaching hospital, tertiary care & medical research"},
  "Kokilaben Dhirubhai Ambani Hospital": {"website": "https://www.kokilabenhospital.com", "careers": "https://www.kokilabenhospital.com/careers.html", "type": "Hospital Chain", "focus": "Multi-specialty tertiary care, robotics & oncology"},
  "HCG Cancer Centre": {"website": "https://www.hcgoncology.com", "careers": "https://www.hcgoncology.com/careers", "type": "Oncology Specialty", "focus": "HealthCare Global - Comprehensive cancer care network"},
  "HealthCare Global Enterprises": {"website": "https://www.hcgoncology.com", "careers": "https://www.hcgoncology.com/careers", "type": "Oncology Specialty", "focus": "Specialty cancer care & precision oncology"},
  "Shalby Hospitals": {"website": "https://www.shalby.org", "careers": "https://www.shalby.org/careers/", "type": "Hospital Chain", "focus": "Arthroplasty, joint replacement & multi-specialty care"},
  "Wockhardt Hospitals": {"website": "https://www.wockhardthospitals.com", "careers": "https://www.wockhardthospitals.com/careers/", "type": "Hospital Chain", "focus": "Super-specialty cardiac, neuro & surgical care"},
  "Jehangir Hospital": {"website": "https://www.jehangirhospital.com", "careers": "https://www.jehangirhospital.com/careers.php", "type": "Hospital Chain", "focus": "Multi-specialty tertiary care hospital in Western India"},
  "Ruby Hall Clinic": {"website": "https://rubyhall.com", "careers": "https://rubyhall.com/careers", "type": "Hospital Chain", "focus": "Organ transplant, cardiac care & cancer specialty"},
  "Columbia Asia Hospitals": {"website": "https://www.manipalhospitals.com", "careers": "https://www.manipalhospitals.com/careers/", "type": "Hospital Chain", "focus": "Multi-specialty network (acquired by Manipal Hospitals)"},
  "Sagar Hospitals": {"website": "https://www.sagarhospitals.in", "careers": "https://www.sagarhospitals.in/careers/", "type": "Hospital Chain", "focus": "Tertiary medical care, neuro & cardiac sciences"},
  "Cloudnine Hospitals": {"website": "https://www.cloudninehospitals.com", "careers": "https://www.cloudninehospitals.com/careers", "type": "Maternity Hospital", "focus": "Specialty maternity, fertility & neonatal care"},
  "Motherhood Hospitals": {"website": "https://www.motherhoodhospitals.com", "careers": "https://www.motherhoodhospitals.com/careers/", "type": "Maternity Hospital", "focus": "Women & children's specialty healthcare network"},
  "IHH Healthcare India": {"website": "https://www.ihhhealthcare.com", "careers": "https://www.ihhhealthcare.com/careers", "type": "Hospital Group", "focus": "Global healthcare group operating Gleneagles Hospitals"},
  "Dr. Agarwal's Eye Hospital": {"website": "https://www.dragarwal.com", "careers": "https://www.dragarwal.com/careers/", "type": "Eye Care Chain", "focus": "Advanced cataract, LASIK & retinal eye care"},
  "Centre for Sight": {"website": "https://www.centreforsight.net", "careers": "https://www.centreforsight.net/careers/", "type": "Eye Care Chain", "focus": "Cornea, refractive surgery & ophthalmology services"},
  "LV Prasad Eye Institute": {"website": "https://www.lvpei.org", "careers": "https://www.lvpei.org/careers", "type": "Eye Care Institute", "focus": "Non-profit WHO eye care institute & corneal research"},
  "Sankara Nethralaya": {"website": "https://www.sankaranethralaya.org", "careers": "https://www.sankaranethralaya.org/careers.html", "type": "Eye Care Hospital", "focus": "Not-for-profit ophthalmic hospital & vision research"},
  "Narayana Nethralaya": {"website": "https://www.narayananethralaya.org", "careers": "https://www.narayananethralaya.org/careers/", "type": "Eye Care Hospital", "focus": "Super-specialty eye hospital & ocular gene therapy"},
  "Dr Lal PathLabs": {"website": "https://www.lalpathlabs.com", "careers": "https://www.lalpathlabs.com/careers", "type": "Diagnostics Chain", "focus": "Pan-India diagnostic pathology test laboratory network"},
  "Metropolis Healthcare": {"website": "https://www.metropolisindia.com", "careers": "https://www.metropolisindia.com/careers", "type": "Diagnostics Chain", "focus": "Pathology & diagnostic test centers across India"},
  "Thyrocare Technologies": {"website": "https://www.thyrocare.com", "careers": "https://www.thyrocare.com/careers", "type": "Diagnostics Chain", "focus": "Automated preventive health & blood diagnostic lab"},
  "Vijaya Diagnostic Centre": {"website": "https://www.vijayadiagnostic.com", "careers": "https://www.vijayadiagnostic.com/careers", "type": "Diagnostics Chain", "focus": "Integrated radiology & pathology diagnostic services"},
  "Neuberg Diagnostics": {"website": "https://neubergdiagnostics.com", "careers": "https://neubergdiagnostics.com/careers/", "type": "Diagnostics Chain", "focus": "Genomics, pathology & advanced diagnostic testing"},
  "Apollo Diagnostics": {"website": "https://www.apollodiagnostics.in", "careers": "https://www.apollodiagnostics.in/careers", "type": "Diagnostics Chain", "focus": "Pathology laboratory network by Apollo Health & Lifestyle"},
  "Redcliffe Labs": {"website": "https://redcliffelabs.com", "careers": "https://redcliffelabs.com/careers", "type": "Diagnostics Chain", "focus": "Omnichannel digital diagnostics & routine health testing"},
  "Agilus Diagnostics": {"website": "https://agilusdiagnostics.com", "careers": "https://agilusdiagnostics.com/careers", "type": "Diagnostics Chain", "focus": "Formerly SRL Diagnostics - Comprehensive laboratory network"},
  "Strand Life Sciences": {"website": "https://strandls.com", "careers": "https://strandls.com/careers/", "type": "Genomics / Testing", "focus": "Precision medicine, bioinformatics & genomic testing"},
  "MedGenome": {"website": "https://www.medgenome.com", "careers": "https://www.medgenome.com/careers/", "type": "Genomics / Testing", "focus": "Genetic diagnostics, DNA sequencing & drug discovery"},
  "MapmyGenome": {"website": "https://mapmygenome.in", "careers": "https://mapmygenome.in/pages/careers", "type": "Genomics / HealthTech", "focus": "Personalized genomics, DNA testing & preventative health"},
  "Medtronic India": {"website": "https://www.medtronic.com", "careers": "https://www.medtronic.com/in-en/about/careers.html", "type": "MedTech / MNC", "focus": "Pacemakers, surgical robotics, diabetes & neuro devices"},
  "GE HealthCare": {"website": "https://www.gehealthcare.com", "careers": "https://www.gehealthcare.com/about/careers", "type": "MedTech / MNC", "focus": "Medical imaging, CT, MRI, ultrasound & patient monitoring"},
  "Siemens Healthineers": {"website": "https://www.siemens-healthineers.com", "careers": "https://www.siemens-healthineers.com/careers", "type": "MedTech / MNC", "focus": "Diagnostic imaging, laboratory automation & AI healthcare"},
  "Philips Healthcare": {"website": "https://www.philips.com", "careers": "https://www.careers.philips.com", "type": "MedTech / MNC", "focus": "Image-guided therapy, patient monitoring & health informatics"},
  "Stryker India": {"website": "https://www.stryker.com", "careers": "https://careers.stryker.com", "type": "MedTech / MNC", "focus": "Orthopedic implants, surgical navigation & neurotechnology"},
  "Boston Scientific India": {"website": "https://www.bostonscientific.com", "careers": "https://www.bostonscientific.com/en-US/careers.html", "type": "MedTech / MNC", "focus": "Interventional cardiology, endoscopy & neuromodulation"},
  "Abbott India": {"website": "https://www.abbott.com", "careers": "https://www.abbott.com/careers.html", "type": "MedTech & Diagnostics", "focus": "Glucose monitoring, diagnostics & vascular devices"},
  "Johnson & Johnson MedTech": {"website": "https://www.jnjmedtech.com", "careers": "https://jobs.jnj.com", "type": "MedTech / MNC", "focus": "Surgical instruments, orthopedic implants & vision care"},
  "Becton Dickinson (BD)": {"website": "https://www.bd.com", "careers": "https://jobs.bd.com", "type": "MedTech / MNC", "focus": "Medical supplies, injection devices & bioscience systems"},
  "B. Braun India": {"website": "https://www.bbraun.co.in", "careers": "https://www.bbraun.co.in/en/careers.html", "type": "MedTech / MNC", "focus": "Infusion therapy, dialysis equipment & surgical instruments"},
  "Baxter India": {"website": "https://www.baxter.com", "careers": "https://jobs.baxter.com", "type": "MedTech / MNC", "focus": "Renal dialysis, IV solutions & critical care medical tech"},
  "Fresenius Medical Care": {"website": "https://www.freseniusmedicalcare.com", "careers": "https://jobs.freseniusmedicalcare.com", "type": "MedTech / Dialysis", "focus": "Dialysis products, kidney disease care & clinical services"},
  "Fresenius Kabi": {"website": "https://www.fresenius-kabi.com", "careers": "https://www.fresenius-kabi.com/careers", "type": "MedTech / Clinical", "focus": "Infusion therapy, clinical nutrition & IV generic drugs"},
  "Olympus India": {"website": "https://www.olympus-asiapac.com/in/", "careers": "https://www.olympus-asiapac.com/in/en/careers/", "type": "MedTech / Optics", "focus": "Endoscopes, gastrointestinal optics & surgical imaging"},
  "Karl Storz India": {"website": "https://www.karlstorz.com", "careers": "https://www.karlstorz.com/us/en/careers.htm", "type": "MedTech / Optics", "focus": "Endoscopy, laparoscopic instruments & OR integration"},
  "Smith+Nephew India": {"website": "https://www.smith-nephew.com", "careers": "https://www.smith-nephew.com/en/careers", "type": "MedTech / MNC", "focus": "Orthopedic reconstruction, sports medicine & wound care"},
  "Zimmer Biomet India": {"website": "https://www.zimmerbiomet.com", "careers": "https://www.zimmerbiomet.com/en/about-us/careers.html", "type": "MedTech / MNC", "focus": "Joint replacement, dental implants & robotic surgery"},
  "Edwards Lifesciences India": {"website": "https://www.edwards.com", "careers": "https://www.edwards.com/careers", "type": "MedTech / MNC", "focus": "Transcatheter heart valves & hemodynamic monitoring"},
  "Intuitive Surgical India": {"website": "https://www.intuitive.com", "careers": "https://www.intuitive.com/en-us/about-us/company/careers", "type": "MedTech / Robotics", "focus": "da Vinci robotic surgical systems & minimally invasive tech"},
  "Alcon India": {"website": "https://www.alcon.com", "careers": "https://www.alcon.com/careers", "type": "MedTech / Vision", "focus": "Surgical ophthalmic equipment & contact lens products"},
  "EssilorLuxottica India": {"website": "https://www.essilorluxottica.com", "careers": "https://www.essilorluxottica.com/en/careers/", "type": "Eyewear / MedTech", "focus": "Ophthalmic lenses, optical equipment & eyewear design"},
  "CooperVision India": {"website": "https://coopervision.com", "careers": "https://coopervision.com/careers", "type": "Vision Care", "focus": "Contact lenses & myopia management optical products"},
  "Carl Zeiss India": {"website": "https://www.zeiss.co.in", "careers": "https://www.zeiss.co.in/corporate/careers.html", "type": "MedTech / Optics", "focus": "Surgical microscopes, ophthalmic diagnostic devices & lenses"},
  "Hologic India": {"website": "https://www.hologic.com", "careers": "https://www.hologic.com/careers", "type": "MedTech / Diagnostics", "focus": "Mammography, 3D breast imaging & women's health tech"},
  "ResMed India": {"website": "https://www.resmed.com", "careers": "https://careers.resmed.com", "type": "MedTech / Sleep", "focus": "CPAP devices, sleep apnea therapy & ventilation tech"},
  "Masimo India": {"website": "https://www.masimo.com", "careers": "https://www.masimo.com/careers/", "type": "MedTech / Sensors", "focus": "Pulse oximetry, noninvasive patient monitoring sensors"},
  "Nipro India": {"website": "https://www.nipro-group.com", "careers": "https://www.nipro-group.com/en/careers", "type": "MedTech / Dialysis", "focus": "Dialyzers, hemodialysis machines & medical needles"},
  "Terumo India": {"website": "https://www.terumo.com", "careers": "https://www.terumo.com/careers/", "type": "MedTech / Interventional", "focus": "Interventional cardiology, blood management & vascular devices"},
  "Roche Diagnostics India": {"website": "https://diagnostics.roche.com", "careers": "https://www.roche.com/careers", "type": "In-Vitro Diagnostics", "focus": "Laboratory automation, molecular testing & tissue diagnostics"},
  "Danaher India": {"website": "https://www.danaher.com", "careers": "https://jobs.danaher.com", "type": "Life Sciences / MedTech", "focus": "Biotechnology, diagnostics, filtration & life science tools"},
  "Beckman Coulter": {"website": "https://www.beckmancoulter.com", "careers": "https://www.beckmancoulter.com/en/about-us/careers", "type": "In-Vitro Diagnostics", "focus": "Clinical chemistry, hematology & flow cytometry analyzers"},
  "Leica Biosystems": {"website": "https://www.leicabiosystems.com", "careers": "https://www.leicabiosystems.com/about/careers/", "type": "Histopathology", "focus": "Anatomical pathology, tissue staining & digital pathology"},
  "Cepheid": {"website": "https://www.cepheid.com", "careers": "https://www.cepheid.com/en/about/careers", "type": "Molecular Diagnostics", "focus": "GeneXpert PCR automated molecular diagnostic testing"},
  "Thermo Fisher Scientific": {"website": "https://www.thermofisher.com", "careers": "https://jobs.thermofisher.com", "type": "Life Sciences / Diagnostics", "focus": "Laboratory analytical instruments, reagents & clinical research"},
  "Bio-Rad Laboratories": {"website": "https://www.bio-rad.com", "careers": "https://www.bio-rad.com/en-in/corporate/careers", "type": "Life Sciences / Diagnostics", "focus": "Life science research products & clinical diagnostics"},
  "Agilent Technologies India": {"website": "https://www.agilent.com", "careers": "https://careers.agilent.com", "type": "Life Sciences / Analytics", "focus": "Chromatography, mass spectrometry & lab automation"},
  "Waters Corporation India": {"website": "https://www.waters.com", "careers": "https://www.waters.com/nextgen/in/en/about-waters/careers.html", "type": "Analytical Instruments", "focus": "HPLC, LC-MS mass spectrometry & thermal analysis"},
  "Illumina India": {"website": "https://www.illumina.com", "careers": "https://www.illumina.com/company/careers.html", "type": "Genomics / Sequencing", "focus": "DNA sequencing instruments, NGS kits & genomic data"},
  "QIAGEN India": {"website": "https://www.qiagen.com", "careers": "https://www.qiagen.com/us/about-us/careers/", "type": "Sample & Assay Tech", "focus": "DNA/RNA extraction, PCR testing & bioinformatics"},
  "Meril Life Sciences": {"website": "https://www.merillife.com", "careers": "https://www.merillife.com/careers", "type": "MedTech / Indian", "focus": "Vascular intervention, orthopedic implants & diagnostics"},
  "Trivitron Healthcare": {"website": "https://www.trivitron.com", "careers": "https://www.trivitron.com/careers", "type": "MedTech / Indian", "focus": "Newborn screening, imaging, ICU equipment & renal care"},
  "Poly Medicure": {"website": "https://www.polymedicure.com", "careers": "https://www.polymedicure.com/careers/", "type": "MedTech / Supplies", "focus": "IV cannulas, vascular access devices & infusion sets"},
  "Healthium Medtech": {"website": "https://healthiummedtech.com", "careers": "https://healthiummedtech.com/careers/", "type": "MedTech / Surgical", "focus": "Surgical sutures, wound closure & arthroscopy devices"},
  "Sahajanand Medical Technologies": {"website": "https://www.smtpl.com", "careers": "https://www.smtpl.com/careers", "type": "MedTech / Cardiac", "focus": "Drug-eluting stents, structural heart & balloon catheters"},
  "BPL Medical Technologies": {"website": "https://www.bplmedicaltechnologies.com", "careers": "https://www.bplmedicaltechnologies.com/careers/", "type": "MedTech / Devices", "focus": "ECG machines, patient monitors, defibrillators & imaging"},
  "Skanray Technologies": {"website": "https://skanray.com", "careers": "https://skanray.com/careers/", "type": "MedTech / Devices", "focus": "High-frequency X-ray systems, surgical C-Arms & ventilators"},
  "Allengers Medical Systems": {"website": "https://www.allengers.com", "careers": "https://www.allengers.com/careers.php", "type": "MedTech / Imaging", "focus": "X-ray machines, DSA Cathlabs, Mammography & EEG systems"}
}

# Function to build 100% full markdown table from ALL raw excel rows
with open('raw_extracted.json', 'r', encoding='utf8') as f:
  raw_data = json.load(f)

def clean_str(s):
  if not s: return ''
  return s.strip()

def process_category(cat_key, title, desc, file_path):
  rows = raw_data.get(cat_key, [])[1:] # skip header
  
  md_lines = [
    f"# {title}",
    "",
    desc,
    "",
    "> **How to edit on GitHub**: Click the pencil ✏️ icon at the top right of this file, add or edit a company line in the table below, and click **Propose changes** to submit a Pull Request!",
    "",
    "| ID | Company Name | Official Website | Careers Portal | India Locations | Type | Key Focus / Notes |",
    "|---|---|---|---|---|---|---|"
  ]

  count = 1
  seen_companies = set()

  for r in rows:
    # Filter non-empty items
    items = [x.strip() for x in r if x.strip()]
    if not items:
      continue
    
    # Try to identify company name
    comp_name = None
    locations = "India"
    
    # Search items for known names or clean string
    for item in items:
      if item in master_directory:
        comp_name = item
        break
    
    if not comp_name:
      # Pick item that looks like a company name
      for item in items:
        if not re.match(r'^\d+$', item) and item not in ['Careers', 'SBI', 'TCS', 'Apollo', 'India Locations', 'Pan India']:
          if not any(city in item for city in ['Hyderabad', 'Bengaluru', 'Mumbai', 'Chennai', 'Delhi NCR', 'Pune', 'Kolkata', 'Ahmedabad']):
            comp_name = item
            break
    
    if not comp_name and len(items) >= 2:
      comp_name = items[1]
    
    if not comp_name or comp_name in ['#', 'Company', 'Official Website', 'Careers Portal', 'India Locations']:
      continue

    # Deduplicate company name
    clean_name = comp_name.replace('**', '').strip()
    if clean_name.lower() in seen_companies:
      continue
    seen_companies.add(clean_name.lower())

    # Get metadata from master_directory if available
    info = master_directory.get(clean_name, None)
    
    if info:
      web_url = info['website']
      car_url = info['careers']
      loc_str = info.get('locations', 'India')
      type_str = info['type']
      focus_str = info['focus']
    else:
      web_url = f"https://www.google.com/search?q={re.sub(r'\s+', '+', clean_name)}"
      car_url = f"https://www.google.com/search?q={re.sub(r'\s+', '+', clean_name)}+careers"
      # Try extract locations from items
      loc_candidates = [i for i in items if any(city in i for city in ['Hyderabad', 'Bengaluru', 'Mumbai', 'Chennai', 'Delhi', 'Pune', 'Kolkata', 'Ahmedabad', 'Pan India'])]
      loc_str = loc_candidates[0] if loc_candidates else "India"
      type_str = "Company"
      focus_str = "Corporate Operations & Career Opportunities"

    web_link = f"[Website]({web_url})"
    car_link = f"[Careers Portal]({car_url})"
    
    md_lines.append(f"| {count} | **{clean_name}** | {web_link} | {car_link} | {loc_str} | `{type_str}` | {focus_str} |")
    count += 1

  fs_content = '\n'.join(md_lines)
  with open(file_path, 'w', encoding='utf8') as f:
    f.write(fs_content)

  print(f"[OK] Generated {file_path} with {count-1} entries.")

# Process Healthcare
process_category(
  'health',
  'Hospitals, Diagnostics & HealthTech Companies in India',
  'A curated list of **100 Hospitals, Diagnostic Chains, Eyecare Specialty, MedTech Equipment & HealthTech Platforms** operating in India.',
  'companies/healthcare.md'
)

# Process IT
process_category(
  'it',
  'IT & Software Companies in India',
  'A curated list of **100 IT Services, Product MNCs, SaaS, Cloud, Semiconductor & Engineering R&D** operating in India.',
  'companies/tech.md'
)

# Process Finance
process_category(
  'banks',
  'Banking, Finance & Fintech Companies in India',
  'A curated list of **100+ Public & Private Banks, Investment GCCs, Asset Management, InsurTech, and Fintechs** operating in India.',
  'companies/finance.md'
)
