# 🚀 Jobseeker Company Directory & Career Portals

[![GitHub License](https://img.shields.io/github/license/achuet/career-portals?color=blue)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/achuet/career-portals?style=social)](https://github.com/achuet/career-portals)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen)](https://achuet.github.io/career-portals/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/achuet/career-portals/pulls)

An open-source, community-curated directory designed to help **jobseekers** quickly find **official career portals, websites, office locations, and sub-industry focus** for companies across India.

Instead of navigating scattered job boards or outdated lists, jobseekers can browse formatted Markdown tables natively inside GitHub or use the interactive **GitHub Pages Web App** with real-time search, city filtering, bookmarking, and 1-click links to direct career portals and LinkedIn job searches.

---

## 📁 Category Directories (Markdown Tables)

Each industry category is maintained as an easily editable **Markdown (`.md`)** table file. Click any link below to view or edit:

| Category | File | Description | Company Count |
|---|---|---|---|
| 🧪 **Pharma & Life Sciences** | [`companies/pharma.md`](companies/pharma.md) | Top 100 Pharma, Biotech, MedTech, CDMO & CRO companies in India | **100** |
| 💻 **IT & Software** | [`companies/tech.md`](companies/tech.md) | Product MNCs, SaaS, and IT Services companies | **10+** |
| 🏦 **Banking & Fintech** | [`companies/finance.md`](companies/finance.md) | Banks, Investment GCCs, and Neobanks | **7+** |

---

## 🌟 Key Features

### For Jobseekers
- 🎯 **Direct Career Links**: 1-click access to verified official career pages (no middleman redirect ads).
- 📍 **Location Filtering**: Filter by major tech/pharma hubs (Hyderabad, Bengaluru, Mumbai, Pune, Chennai, Gurugram, etc.).
- 🔍 **Real-Time Instant Search**: Search by company name, city, or specialty tag.
- ⚡ **Dual View Modes**: Switch between rich visual Cards Grid and compact Table List view.
- ⭐️ **Local Favorites**: Bookmark target companies in your browser for follow-ups.
- 📤 **Export Data**: Download custom company lists as JSON, CSV, or Markdown.

### For Open-Source Contributors
- 📝 **Markdown-First Format**: No complex database or backend setup required.
- ✏️ **Edit Directly on GitHub**: Add or update companies directly from your browser by editing `.md` files in GitHub web interface.

---

## 🤝 How to Add a New Company (Contribution Guide)

Anyone can contribute! Follow these 3 simple steps to add a company:

### Method 1: Edit directly on GitHub Web (No git required!)
1. Open the target category Markdown file (e.g. [`companies/pharma.md`](companies/pharma.md) or [`companies/tech.md`](companies/tech.md)).
2. Click the **Pencil icon ✏️** at the top right of the file to edit.
3. Scroll to the bottom of the table and add a new row following this format:
   ```markdown
   | 101 | **Your Company Name** | [Website](https://www.example.com) | [Careers Portal](https://www.example.com/careers) | Hyderabad, Bengaluru | `Global MNC` | Oncology & Biologics |
   ```
4. Click **Propose changes**, enter a short title (e.g., "Add BioTech Solutions"), and click **Create pull request**!

### Method 2: Use the Web App Generator
1. Open the [Live Web App](https://WC-Companies.github.io/WC_Companies_List/).
2. Click **Submit Company** button in the top navigation bar.
3. Fill in the form — it will auto-generate the exact Markdown row for you to copy and paste!

---

## 🛠️ Local Development & Web Setup

Since the application is built using standard static web technologies (HTML5, CSS3, Vanilla JS), you can run it locally with any web server:

```bash
# Clone the repository
git clone https://github.com/achuet/career-portals.git
cd career-portals

# Option 1: Serve using Python 3
python -m http.server 8000

# Option 2: Serve using Node npx
npx serve .
```

Open `http://localhost:8000` in your web browser to test!

---

## 🌐 Deploying to GitHub Pages

To host this directory on your own GitHub Pages:

1. Go to your repository **Settings** on GitHub.
2. Click **Pages** in the left sidebar menu.
3. Under **Build and deployment**:
   - **Source**: Select `Deploy from a branch`
   - **Branch**: Select `main` branch / `root (/)` folder.
4. Click **Save**. Your site will automatically go live at `https://achuet.github.io/career-portals/`!

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.

---

<p center>Made with ❤️ to help all jobseekers land their dream roles.</p>
