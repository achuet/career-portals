const fs = require('fs');
const path = require('path');

// Dictionary of enriched data for pharma companies
const enrichedData = {
  "Novartis": { website: "https://www.novartis.com", careers: "https://www.novartis.com/careers", type: "Global MNC", focus: "Innovative Pharmaceuticals, Gene Therapy & Oncology" },
  "AstraZeneca": { website: "https://www.astrazeneca.com", careers: "https://careers.astrazeneca.com", type: "Global MNC", focus: "Oncology, Cardiovascular, Renal & Metabolism, Respiratory" },
  "Pfizer": { website: "https://www.pfizer.com", careers: "https://www.pfizer.com/about/careers", type: "Global MNC", focus: "Vaccines, Oncology, Immunology & Rare Diseases" },
  "Eli Lilly": { website: "https://www.lilly.com", careers: "https://careers.lilly.com", type: "Global MNC", focus: "Diabetes Care, Oncology, Immunology & Neurodegeneration" },
  "Roche": { website: "https://www.roche.com", careers: "https://www.roche.com/careers", type: "Global MNC", focus: "In-Vitro Diagnostics, Biotechnology & Personalized Healthcare" },
  "Merck / MSD": { website: "https://www.msd.com", careers: "https://jobs.msd.com", type: "Global MNC", focus: "Vaccines, Oncology (Keytruda), Infectious Diseases" },
  "GSK": { website: "https://www.gsk.com", careers: "https://www.gsk.com/en-gb/careers/", type: "Global MNC", focus: "Vaccines, HIV Therapeutics, Specialty Medicines" },
  "Sanofi": { website: "https://www.sanofi.com", careers: "https://www.sanofi.com/en/careers", type: "Global MNC", focus: "Immunology, Vaccines, Rare Diseases & Consumer Healthcare" },
  "Bristol Myers Squibb": { website: "https://www.bms.com", careers: "https://careers.bms.com", type: "Global MNC", focus: "Immuno-Oncology, Hematology, Cardiovascular" },
  "Amgen": { website: "https://www.amgen.com", careers: "https://careers.amgen.com", type: "Global MNC", focus: "Biologics, Biosimilars, Cardiovascular & Bone Health" },
  "Takeda": { website: "https://www.takeda.com", careers: "https://jobs.takeda.com", type: "Global MNC", focus: "Gastroenterology, Rare Diseases, Plasma-Derived Therapies" },
  "Bayer": { website: "https://www.bayer.com", careers: "https://www.bayer.com/en/careers", type: "Global MNC", focus: "Pharmaceuticals, Consumer Health & Crop Science" },
  "AbbVie": { website: "https://www.abbvie.com", careers: "https://careers.abbvie.com", type: "Global MNC", focus: "Immunology, Neuroscience, Aesthetics & Oncology" },
  "Boehringer Ingelheim": { website: "https://www.boehringer-ingelheim.com", careers: "https://jobs.boehringer-ingelheim.com", type: "Global MNC", focus: "Cardio-Metabolic, Respiratory, Animal Health" },
  "Novo Nordisk": { website: "https://www.novonordisk.com", careers: "https://www.novonordisk.com/careers.html", type: "Global MNC", focus: "Diabetes & Obesity Care, Rare Blood Disorders" },
  "Biogen": { website: "https://www.biogen.com", careers: "https://careers.biogen.com", type: "Global MNC", focus: "Neuroscience, Multiple Sclerosis, Alzheimer's" },
  "Gilead Sciences": { website: "https://www.gilead.com", careers: "https://www.gilead.com/careers", type: "Global MNC", focus: "Virology, HIV, Viral Hepatitis, Oncology" },
  "Viatris": { website: "https://www.viatris.com", careers: "https://www.viatris.com/en/careers", type: "Global MNC", focus: "Generics, Biosimilars, Branded Medicines" },
  "Organon": { website: "https://www.organon.com", careers: "https://jobs.organon.com", type: "Global MNC", focus: "Women's Health, Biosimilars, Established Brands" },
  "Vertex Pharmaceuticals": { website: "https://www.vrtx.com", careers: "https://www.vrtx.com/careers", type: "Global MNC", focus: "Cystic Fibrosis, Gene Editing, Sickle Cell Therapy" },
  "Regeneron": { website: "https://www.regeneron.com", careers: "https://careers.regeneron.com", type: "Global MNC", focus: "Monoclonal Antibodies, Ophthalmology, Immunology" },
  "Astellas Pharma": { website: "https://www.astellas.com", careers: "https://www.astellas.com/en/careers", type: "Global MNC", focus: "Urology, Oncology, Cell & Gene Therapy" },
  "Daiichi Sankyo": { website: "https://www.daiichisankyo.com", careers: "https://www.daiichisankyo.com/careers/", type: "Global MNC", focus: "Antibody-Drug Conjugates (ADC), Oncology" },
  "Eisai": { website: "https://www.eisai.com", careers: "https://www.eisai.com/careers/", type: "Global MNC", focus: "Neurology, Oncology, Dementia Research" },
  "Otsuka Pharmaceutical": { website: "https://www.otsuka.co.jp/en/", careers: "https://www.otsuka.co.jp/en/company/careers/", type: "Global MNC", focus: "CNS Disorders, Clinical Nutrition, Medical Devices" },
  "Merck KGaA": { website: "https://www.merckgroup.com", careers: "https://www.merckgroup.com/en/careers.html", type: "Global MNC", focus: "Healthcare, Life Science Solutions & Electronics" },
  "CSL": { website: "https://www.csl.com", careers: "https://www.csl.com/careers", type: "Global MNC", focus: "Plasma Biotherapies, Influenza Vaccines, Hematology" },
  "Baxter": { website: "https://www.baxter.com", careers: "https://jobs.baxter.com", type: "MedTech / MNC", focus: "Renal Care, Critical Care, Surgical Products" },
  "Stryker": { website: "https://www.stryker.com", careers: "https://careers.stryker.com", type: "MedTech / MNC", focus: "Orthopedics, Medical & Surgical Equipment" },
  "Medtronic": { website: "https://www.medtronic.com", careers: "https://www.medtronic.com/in-en/about/careers.html", type: "MedTech / MNC", focus: "Cardiovascular Devices, Surgical Robotics, Neuromodulation" },
  "Johnson & Johnson": { website: "https://www.jnj.com", careers: "https://jobs.jnj.com", type: "Global MNC", focus: "MedTech, Innovative Medicine, Surgical Solutions" },
  "Boston Scientific": { website: "https://www.bostonscientific.com", careers: "https://www.bostonscientific.com/en-US/careers.html", type: "MedTech / MNC", focus: "Interventional Medical Specialties & Implants" },
  "Abbott": { website: "https://www.abbott.com", careers: "https://www.abbott.com/careers.html", type: "MedTech & Nutrition", focus: "Diagnostics, Medical Devices, Nutritional Products" },
  "Alcon": { website: "https://www.alcon.com", careers: "https://www.alcon.com/careers", type: "MedTech / MNC", focus: "Eye Care, Ophthalmic Surgical & Vision Care" },
  "GE HealthCare": { website: "https://www.gehealthcare.com", careers: "https://www.gehealthcare.com/about/careers", type: "MedTech / MNC", focus: "Medical Imaging, Ultrasound, Patient Care Solutions" },
  "Philips Healthcare": { website: "https://www.philips.com", careers: "https://www.careers.philips.com", type: "MedTech / MNC", focus: "Health Informatics, Image-Guided Therapy, Monitoring" },
  "Siemens Healthineers": { website: "https://www.siemens-healthineers.com", careers: "https://www.siemens-healthineers.com/careers", type: "MedTech / MNC", focus: "Diagnostic Imaging, Laboratory Diagnostics, AI Healthcare" },
  "Thermo Fisher Scientific": { website: "https://www.thermofisher.com", careers: "https://jobs.thermofisher.com", type: "Life Sciences / MNC", focus: "Analytical Instruments, Lab Equipment, Clinical Research" },
  "Danaher": { website: "https://www.danaher.com", careers: "https://jobs.danaher.com", type: "Life Sciences / MNC", focus: "Biotechnology, Life Sciences & Diagnostics" },
  "Waters Corporation": { website: "https://www.waters.com", careers: "https://www.waters.com/nextgen/in/en/about-waters/careers.html", type: "Life Sciences / MNC", focus: "Liquid Chromatography, Mass Spectrometry, Software" },
  "Sun Pharma": { website: "https://www.sunpharma.com", careers: "https://www.sunpharma.com/careers", type: "Indian Pharma", focus: "Specialty Generics, Active Pharmaceutical Ingredients (API)" },
  "Dr. Reddy's Laboratories": { website: "https://www.drreddys.com", careers: "https://careers.drreddys.com", type: "Indian Pharma", focus: "Generics, Biosimilars, APIs, Customized Formulations" },
  "Aurobindo Pharma": { website: "https://www.aurobindo.com", careers: "https://www.aurobindo.com/careers/", type: "Indian Pharma", focus: "Oral Generics, Injectables, APIs" },
  "Cipla": { website: "https://www.cipla.com", careers: "https://www.cipla.com/careers", type: "Indian Pharma", focus: "Respiratory Care, Antiretrovirals, Generics" },
  "Lupin": { website: "https://www.lupin.com", careers: "https://www.lupin.com/careers/", type: "Indian Pharma", focus: "Pediatrics, Cardiovascular, Anti-TB & Respiratory" },
  "Zydus Lifesciences": { website: "https://zyduslife.com", careers: "https://zyduslife.com/careers", type: "Indian Pharma", focus: "Vaccines, Biologics, NCEs & Specialty Formulations" },
  "Torrent Pharma": { website: "https://www.torrentpharma.com", careers: "https://www.torrentpharma.com/index.php/site/info/careers", type: "Indian Pharma", focus: "Cardiovascular, CNS, Diabetology, Gastroenterology" },
  "Mankind Pharma": { website: "https://www.mankindpharma.com", careers: "https://www.mankindpharma.com/careers", type: "Indian Pharma", focus: "Consumer Healthcare, Formulations, OTC Products" },
  "Alkem Laboratories": { website: "https://www.alkemlabs.com", careers: "https://www.alkemlabs.com/careers.php", type: "Indian Pharma", focus: "Anti-infectives, Gastroenterology, Pain Management" },
  "Divi's Laboratories": { website: "https://www.divislabs.com", careers: "https://www.divislabs.com/careers/", type: "CDMO / API", focus: "Active Pharmaceutical Ingredients (APIs) & Custom Synthesis" },
  "Glenmark Pharmaceuticals": { website: "https://www.glenmarkpharma.com", careers: "https://jobs.glenmarkpharma.com", type: "Indian Pharma", focus: "Dermatology, Respiratory, Oncology & Novel Entities" },
  "Intas Pharmaceuticals": { website: "https://www.intaspharma.com", careers: "https://www.intaspharma.com/careers/", type: "Indian Pharma", focus: "Biosimilars, CNS, Cardiovascular & Oncology" },
  "Ipca Laboratories": { website: "https://www.ipca.com", careers: "https://www.ipca.com/careers/", type: "Indian Pharma", focus: "Formulations, APIs, Antimalarial Treatments" },
  "Laurus Labs": { website: "https://www.lauruslabs.com", careers: "https://www.lauruslabs.com/careers.php", type: "CDMO / API", focus: "ARV APIs, Custom Synthesis & Finished Dosage Forms" },
  "Natco Pharma": { website: "https://www.natcopharma.co.in", careers: "https://www.natcopharma.co.in/careers/", type: "Indian Pharma", focus: "Oncology Formulations, Complex Generics, Specialty APIs" },
  "Biocon": { website: "https://www.biocon.com", careers: "https://www.biocon.com/careers/", type: "Biotech / Indian", focus: "Biopharmaceuticals, Insulins, Statins & Enzymes" },
  "Biocon Biologics": { website: "https://www.bioconbiologics.com", careers: "https://www.bioconbiologics.com/careers/", type: "Biotech / Indian", focus: "Biosimilars, Monoclonal Antibodies, Diabetes Care" },
  "Alembic Pharmaceuticals": { website: "https://www.alembicpharmaceuticals.com", careers: "https://www.alembicpharmaceuticals.com/careers/", type: "Indian Pharma", focus: "Cardiology, Gynecology, Anti-infectives & Generics" },
  "Ajanta Pharma": { website: "https://www.ajantapharma.com", careers: "https://www.ajantapharma.com/careers.aspx", type: "Indian Pharma", focus: "Ophthalmology, Dermatology, Cardiology & Pain" },
  "Gland Pharma": { website: "https://glandpharma.com", careers: "https://glandpharma.com/careers.html", type: "CDMO / Injectables", focus: "Sterile Injectables, Oncology & Complex Delivery Systems" },
  "Hetero": { website: "https://www.hetero.com", careers: "https://www.hetero.com/careers", type: "Indian Pharma", focus: "Antiretrovirals, APIs & Generic Formulations" },
  "MSN Laboratories": { website: "https://www.msnlabs.com", careers: "https://www.msnlabs.com/careers.html", type: "CDMO / API", focus: "Active Ingredients, Intermediates & Formulations" },
  "Granules India": { website: "https://granulesindia.com", careers: "https://granulesindia.com/careers.php", type: "Indian Pharma", focus: "PFIs, APIs & Finished Dosage Formulations" },
  "Shilpa Medicare": { website: "https://www.vbshilpa.com", careers: "https://www.vbshilpa.com/careers.php", type: "Indian Pharma", focus: "Oncology & Non-Oncology APIs, Transdermal Patches" },
  "Bharat Biotech": { website: "https://www.bharatbiotech.com", careers: "https://www.bharatbiotech.com/careers.html", type: "Biotech / Vaccines", focus: "Vaccines (Covaxin, Rotavac), Biotherapeutics" },
  "Biological E": { website: "https://www.biologicale.com", careers: "https://www.biologicale.com/careers.html", type: "Biotech / Vaccines", focus: "Pediatric & Adult Vaccines, Biopharmaceuticals" },
  "Indian Immunologicals": { website: "https://www.indimmuno.com", careers: "https://www.indimmuno.com/careers/", type: "Biotech / Vaccines", focus: "Human & Veterinary Vaccines, Biologicals" },
  "Serum Institute of India": { website: "https://www.seruminstitute.com", careers: "https://www.seruminstitute.com/careers.php", type: "Biotech / Vaccines", focus: "World's Largest Vaccine Manufacturer by Doses" },
  "Syngene International": { website: "https://www.syngeneintl.com", careers: "https://www.syngeneintl.com/careers/", type: "CRO / CDMO", focus: "Integrated Research, Development & Manufacturing" },
  "Sai Life Sciences": { website: "https://www.sailife.com", careers: "https://www.sailife.com/careers/", type: "CRO / CDMO", focus: "Discovery, NCE Development & Commercial API Production" },
  "Aragen Life Sciences": { website: "https://www.aragen.com", careers: "https://www.aragen.com/careers", type: "CRO / CDMO", focus: "Small & Large Molecule R&D, Clinical Solutions" },
  "Neuland Laboratories": { website: "https://www.neulandlabs.com", careers: "https://www.neulandlabs.com/careers/", type: "CDMO / API", focus: "Peptides, Custom Manufacturing & Complex APIs" },
  "SMS Pharmaceuticals": { website: "https://www.smspharma.com", careers: "https://www.smspharma.com/careers.html", type: "CDMO / API", focus: "Active Pharmaceutical Ingredients & Intermediates" },
  "Vimta Labs": { website: "https://www.vimta.com", careers: "https://www.vimta.com/careers", type: "CRO / Testing", focus: "Contract Research, Bioanalytical Services & Diagnostics" },
  "Aurigene Pharmaceutical Services": { website: "https://www.aurigenerd.com", careers: "https://www.aurigenerd.com/careers", type: "CRO / CDMO", focus: "Accelerated Drug Discovery & Development Services" },
  "Piramal Pharma": { website: "https://www.piramalpharmasolutions.com", careers: "https://www.piramal.com/careers/", type: "CDMO / Indian", focus: "Inhalation Anesthetics, CDMO Solutions & OTC" },
  "Jubilant Pharmova": { website: "https://www.jubilantpharmova.com", careers: "https://www.jubilantpharmova.com/careers", type: "CDMO / Radiopharma", focus: "Radiopharmaceuticals, Allergy Immunotherapy & CDMO" },
  "Strides Pharma Science": { website: "https://www.strides.com", careers: "https://www.strides.com/careers.html", type: "Indian Pharma", focus: "Niche Softgel Capsules, Injectables & Oral Solid Generics" },
  "Wockhardt": { website: "https://www.wockhardt.com", careers: "https://www.wockhardt.com/careers.aspx", type: "Indian Pharma", focus: "Novel Antibiotics, Biotechnology & Vaccines" },
  "Emcure Pharmaceuticals": { website: "https://www.emcure.com", careers: "https://www.emcure.com/careers/", type: "Indian Pharma", focus: "Gynaecology, HIV, Cardiology, Injectables" },
  "Macleods Pharmaceuticals": { website: "https://www.macleodspharma.com", careers: "https://www.macleodspharma.com/careers.asp", type: "Indian Pharma", focus: "Anti-TB, Antimalarial, Anti-Infective Formulations" },
  "Aristo Pharmaceuticals": { website: "https://www.aristopharma.co.in", careers: "https://www.aristopharma.co.in/careers/", type: "Indian Pharma", focus: "Antibiotics, Pain Management, Gastroenterology" },
  "Eris Lifesciences": { website: "https://eris.co.in", careers: "https://eris.co.in/careers/", type: "Indian Pharma", focus: "Chronic & Sub-Chronic Therapy Segments" },
  "Gufic Biosciences": { website: "https://gufic.com", careers: "https://gufic.com/careers/", type: "Indian Pharma", focus: "Lyophilized Products, Herbal Medicine & Critical Care" },
  "FDC": { website: "https://www.fdcindia.com", careers: "https://www.fdcindia.com/careers.php", type: "Indian Pharma", focus: "Electrolytes (Electral), Ophthalmology & Oral Care" },
  "Marksans Pharma": { website: "https://www.marksanspharma.com", careers: "https://www.marksanspharma.com/careers.html", type: "Indian Pharma", focus: "OTC Formulations, Softgels & Pain Management" },
  "Akums Drugs & Pharmaceuticals": { website: "https://www.akums.in", careers: "https://www.akums.in/careers/", type: "CDMO / Formulations", focus: "Contract Manufacturing & Novel Drug Delivery" },
  "J B Chemicals & Pharmaceuticals": { website: "https://jbpharma.com", careers: "https://jbpharma.com/careers/", type: "Indian Pharma", focus: "Hypertension, Cardiac Care & Lozenge Formulations" },
  "Gennova Biopharmaceuticals": { website: "https://gennova.bio", careers: "https://gennova.bio/careers/", type: "Biotech / Vaccines", focus: "mRNA Vaccine Technology & Biosimilars" },
  "Serum Institute Vaccines": { website: "https://www.seruminstitute.com", careers: "https://www.seruminstitute.com/careers.php", type: "Biotech / Vaccines", focus: "Global Vaccine Manufacturing & Pediatric Immunization" },
  "Kaveri Seed / Life Sciences": { website: "https://www.kaveriseeds.in", careers: "https://www.kaveriseeds.in/careers/", type: "Agri-Biotech", focus: "Plant Biotechnology, Crop Science & Life Sciences" },
  "Sri Krishna Pharmaceuticals": { website: "https://srikrishnapharma.com", careers: "https://srikrishnapharma.com/careers/", type: "CDMO / API", focus: "Paracetamol, APIs & Direct Compression Granules" },
  "Aizant Drug Research Solutions": { website: "https://www.aizant.com", careers: "https://www.aizant.com/careers.html", type: "CRO / R&D", focus: "Drug Development, Clinical Research & Formulation" },
  "Virchow Laboratories": { website: "https://virchowlabs.com", careers: "https://virchowlabs.com/careers/", type: "CDMO / API", focus: "Sulfamethoxazole API & Biological Products" },
  "SMS Lifesciences India": { website: "https://www.smslife.in", careers: "https://www.smslife.in/careers.html", type: "CDMO / API", focus: "Active Pharmaceutical Ingredients & Intermediates" },
  "Hikal": { website: "https://www.hikal.com", careers: "https://www.hikal.com/careers/", type: "CDMO / API", focus: "Fine Chemicals, Crop Protection & Pharmaceutical APIs" },
  "Dishman Carbogen Amcis": { website: "https://www.dishmangroup.com", careers: "https://www.dishmangroup.com/careers.html", type: "CDMO / CRAMS", focus: "Highly Potent APIs (HPAPI) & Custom Development" },
  "Solara Active Pharma Sciences": { website: "https://solara.co.in", careers: "https://solara.co.in/careers/", type: "CDMO / API", focus: "Niche APIs, CRAMS & Global Regulatory Filings" },
  "Lasa Supergenerics": { website: "https://www.lasalabs.com", careers: "https://www.lasalabs.com/careers/", type: "API / Animal Health", focus: "Veterinary APIs & Synthetic Chemistry" },
  "Aarti Drugs": { website: "https://www.aartidrugs.co.in", careers: "https://www.aartidrugs.co.in/careers/", type: "API / Chemicals", focus: "Active Ingredients, Specialty Chemicals & Polymers" }
};

const csvContent = fs.readFileSync(path.join(__dirname, '..', 'List.csv'), 'utf8');
const lines = csvContent.split(/\r?\n/).filter(line => line.trim().length > 0);

const dataRows = lines.slice(1);

let mdLines = [
  "# Pharma & Life Sciences Companies in India",
  "",
  "A curated list of **100 top Pharmaceutical, Biotechnology, MedTech, and Contract Research & Manufacturing (CDMO/CRO)** companies operating in India, complete with official website links, career portals, primary locations, and key focus areas.",
  "",
  "> **How to edit on GitHub**: Click the pencil ✏️ icon at the top right of this file, add or edit a company line in the table below, and click **Propose changes** to submit a Pull Request!",
  "",
  "| ID | Company Name | Official Website | Careers Portal | India Locations | Type | Key Focus / Notes |",
  "|---|---|---|---|---|---|---|"
];

dataRows.forEach(rowStr => {
  const parts = [];
  let current = '';
  let inQuotes = false;
  for (let i = 0; i < rowStr.length; i++) {
    const char = rowStr[i];
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      parts.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }
  parts.push(current.trim());

  if (parts.length >= 2) {
    const id = parts[0];
    const rawName = parts[1].replace(/^"|"$/g, '');
    const rawLoc = parts[2] ? parts[2].replace(/^"|"$/g, '') : 'India';

    const info = enrichedData[rawName] || {
      website: `https://www.google.com/search?q=${encodeURIComponent(rawName)}`,
      careers: `https://www.google.com/search?q=${encodeURIComponent(rawName + ' careers')}`,
      type: "Pharma",
      focus: "Pharmaceuticals & Healthcare"
    };

    const websiteLink = `[Website](${info.website})`;
    const careersLink = `[Careers Portal](${info.careers})`;

    mdLines.push(`| ${id} | **${rawName}** | ${websiteLink} | ${careersLink} | ${rawLoc} | \`${info.type}\` | ${info.focus} |`);
  }
});

const targetDir = path.join(__dirname, '..', 'companies');
if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
}
const targetPath = path.join(targetDir, 'pharma.md');
fs.writeFileSync(targetPath, mdLines.join('\n'), 'utf8');

console.log(`Successfully generated ${targetPath} with ${dataRows.length} companies.`);
