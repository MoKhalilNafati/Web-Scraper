# 🎓 DAAD Programs Scraper

This project is a **Python web scraper** that extracts detailed information about degree programs listed on the [DAAD website](https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/).  
It collects program metadata and saves the results into a structured CSV file.

---

## 🚀 Features

The scraper extracts the following fields:

- **Program**  
- **University / Hochschule**  
- **Location**  
- **Period of Study**  
- **Area of Study**  
- **Focus**  
- **Deadlines** (for international students from non-EU countries)  
- **Admission Semester**  
- **Annotation**  
- **Admission Modus**  
- **Admission Requirements**  
- **Lecture Period**  
- **Student Advisory Service** (E-Mail + Website)  
- **Detail Page Link**  

## 📦 Requirements

Make sure you have Python 3.8+ installed and install the dependencies:
```bash
pip install requests
pip install beautifulsoup4
pip install lxml
```

## 📝 Usage

Open the script in your editor and adjust the ##BASE_URL## for your preferred programs filter.
The results will be saved in programs.csv file.
Replace your with open(...) line: Find this line in your main function
```
with open("C:/Users/Khalil/Documents/VS/Web Scraping v2/programs.csv", "w", newline="") as f:
```
