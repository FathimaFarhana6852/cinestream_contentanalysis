# 🎬 CineStream Content Analytics Dashboard

## 📌 Project Overview

The CineStream Content Analytics Dashboard is an interactive data visualization dashboard developed using **Python** and **Streamlit**.

The dashboard helps analyze CineStream content by providing interactive filters, KPIs, charts, and business insights. Users can explore the dataset by filtering Genre, Language, Content Type, Age Rating, IMDb Score, Runtime, and Added Date.

---

## 🎯 Objectives

- Analyze CineStream content performance.
- Provide interactive filtering options.
- Display important KPIs.
- Visualize trends using different charts.
- Answer key business questions through data analysis.

---

## 📂 Dataset

The project uses the **CineStream Catalog Dataset**.

### Dataset Columns

- Title
- Genre
- Language
- Type
- AgeRating
- IMDbScore
- RuntimeMinutes
- AddedDate
- ViewsMillions
- WatchHoursMillions
- ProductionCostCr
- RevenueCr
- ROI_Pct
- Performance_Band

---

## 📊 Dashboard Features

### Module 1
- Data Cleaning
- Missing Value Handling
- Derived Columns

### Module 2
- KPI Cards
- Data Preview
- JSON Display

### Module 3
- Interactive Filters
- Download CSV
- Color Picker

### Module 4
- Sidebar Layout
- Tabs
- Containers
- Expander

### Module 5
- Monthly Line Chart
- Type Bar Chart
- Top Genres Chart
- Language Treemap
- Revenue vs Production Cost Scatter Plot
- ROI by Genre Chart
- IMDb Distribution Histogram
- IMDb vs Views Scatter Plot

### Module 6
- Cached Data Loading
- Filter Form
- Smart Status Messages
- Empty Data Handling

### Module 7
- GitHub Deployment
- Streamlit Cloud Deployment
- Final Report

---

## 📈 Dashboard KPIs

- Total Titles
- Total Views (Millions)
- Total Watch Hours (Millions)
- Average IMDb Score

---

## 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly

---

## 📷 Dashboard Screenshot

<img width="1892" height="897" alt="image" src="https://github.com/user-attachments/assets/82a9a577-b51e-4ec7-b833-127fecc76b72" />

---

## 📁 Project Structure

```
CineStream
│
├── data
│   └── CineStream_Catalog.csv
│
├── notebooks
│   └── m1_explore.ipynb
│
├── output
│   ├── cleaned_cinestream.csv
│   └── m7_report.pdf
│
├── cinestream_app.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

Clone the repository

```bash
git clone https://github.com/yourusername/cinestream_contentanalysis.git
```

Go to the project folder

```bash
cd cinestream_contentanalysis
```

Install required libraries

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run cinestream_app.py
```

---
## 🌐 Live Demo

**Streamlit Cloud**

[https://your-app.streamlit.app](https://cinestreamcontentanalysis-fathimafarhana.streamlit.app/)

---

## 📂 GitHub Repository

[https://github.com/yourusername/cinestream_contentanalysis](https://github.com/FathimaFarhana6852/cinestream_contentanalysis)

---

## 👩‍💻 Developed By

**Fathima Farhana**

Data Analytics Project using Python & Streamlit.
