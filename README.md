# PoliLens

Developed by **Ayaan Iqbal, Raiyan Aaijaz and Mihir Kachroo**

PoliLens is a stock analysis tool that tracks **politicians' stock transactions** and correlates them with **legislation** and **news reports**. The system leverages **AI-powered NLP models** to identify potential patterns and insights that may indicate politically motivated stock movements.

## Table of Contents
- [Key Features and Tools](#key-features-and-tools)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Preview](#preview)
- [License](#license)

## Key Features and Tools
PoliLens combines **data scraping, AI-powered analysis, and a web dashboard** to provide meaningful insights.

| Feature | Description | Technology/Tools |
|---------|-------------|------------------|
| **Stock Transaction Tracking** | Scrapes and stores politicians' stock transactions from public sources. | Python, BeautifulSoup, Requests |
| **Legislation & News Correlation** | Extracts and analyzes legislative bills and financial news for impact on stock movements. | NLP, Hugging Face Transformers |
| **AI-Powered Insights** | Uses machine learning models to detect patterns between stock trades and legislative actions. | TensorFlow, Scikit-learn |
| **Web Dashboard** | Displays key trends and findings interactively. | React, Node.js, Bootstrap, MongoDB (Currently in development) |

## System Architecture
PoliLens consists of **three core modules** working together:

1. **Data Scraper (Backend - Python)**
   - Scrapes stock trades from websites such as CapitolTrades and SmartInsider.
   - Collects legislative and financial news data.
   - Stores data in a structured format for further analysis.

2. **AI & NLP Analysis**
   - Pre-trained NLP models analyze stock transactions concerning legislative activity.
   - Generates insights on potential conflicts of interest or trading patterns.

3. **Web Dashboard (MERN Stack)**
   - Displays AI-generated insights on a user-friendly interface.
   - Allows users to explore connections between political activity and stock movements.  
   *(Currently in development)*

## Installation
**Prerequisites:**
- Python 3.11 or higher
- MongoDB for database storage

### 1. Clone the Repository:
```bash
   git clone https://github.com/your-repo/polilens.git
   cd polilens
```

## Usage

## Preview

## License
This project is licensed under the MIT License. See the LICENSE file for details.
