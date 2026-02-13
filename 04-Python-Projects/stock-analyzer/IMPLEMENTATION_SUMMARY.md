# Stock Price Analyzer - Implementation Summary

## Project Overview

A complete Python-based stock price analyzer designed for university students learning data analysis and financial concepts.

## Files Created

### Core Implementation
- **`stock_analyzer.py`** (600+ lines)
  - Main application with all required functionality
  - Italian comments and docstrings throughout
  - ASCII-only UI for Windows compatibility

### Configuration & Documentation
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Complete project documentation
- **`QUICKSTART.md`** - Quick start guide in Italian
- **`demo_data.csv`** - Sample data for immediate testing
- **`test_setup.py`** - Installation verification script

### Directory Structure
```
stock-analyzer/
├── stock_analyzer.py       # Main program
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick start guide
├── demo_data.csv           # Sample stock data
├── test_setup.py           # Test script
├── charts/                 # Directory for saved charts
└── stock_data.csv          # Created after first save
```

## Implemented Features

### 1. Data Fetching
- **API Integration**: Alpha Vantage API (free tier)
- **Sample Data Mode**: Automatic realistic data generation
- **Error Handling**: Graceful fallback to sample data
- **CSV Import/Export**: Offline analysis capability

### 2. Technical Analysis
- **Moving Averages**: 20-day and 50-day SMA calculation
- **Statistics**: Min, max, mean, median, std deviation
- **Volatility Measurement**: Standard deviation percentage
- **Trend Analysis**: Linear regression for prediction

### 3. Visualization
- **Price Charts**: Matplotlib line charts
- **Multiple Indicators**: Price + MA20 + MA50 overlay
- **Chart Export**: Save as PNG with timestamp
- **Custom Styling**: Grid, legend, labels

### 4. User Interface
- **Main Menu**: 8 options for different functions
- **Italian Language**: All text in Italian
- **Input Validation**: Error checking and fallbacks
- **Help System**: Built-in explanation menu

## Key Functions Implemented

| Function | Purpose |
|----------|---------|
| `main()` | Main menu loop and program entry |
| `fetch_stock_data()` | API calls or sample data generation |
| `calculate_moving_averages()` | SMA calculation using pandas rolling |
| `plot_chart()` | Matplotlib chart creation and export |
| `calculate_statistics()` | Basic and advanced statistics |
| `predict_trend()` | Linear regression for trend analysis |
| `save_to_csv()` | Export data to CSV file |
| `load_from_csv()` | Import data from CSV file |
| `display_analysis()` | Formatted output of results |
| `generate_sample_data()` | Realistic sample data creation |

## Educational Features

### Code Comments
- **Docstrings**: Italian explanations for each function
- **Inline Comments**: Step-by-step explanations
- **Formula Documentation**: Mathematical formulas explained
- **Best Practices**: PEP 8 style, type hints

### Learning Concepts
- **Data Manipulation**: pandas DataFrame operations
- **Statistical Analysis**: Mean, median, std deviation, volatility
- **Financial Concepts**: Moving averages, trends, volatility
- **API Integration**: HTTP requests, JSON parsing
- **Visualization**: matplotlib plotting and customization
- **Machine Learning**: Linear regression basics
- **File I/O**: CSV reading and writing

## Usage Examples

### Quick Start (Sample Data)
```bash
python stock_analyzer.py
# Select: 1
# Symbol: AAPL
# Mode: 2 (sample data)
# View chart: s
# Save CSV: s
```

### With API Key
```bash
python stock_analyzer.py
# Select: 1
# Symbol: MSFT
# Mode: 1 (use API)
# API Key: [your key here]
```

### Load from CSV
```bash
python stock_analyzer.py
# Select: 2
# Filename: demo_data.csv
```

## Technical Specifications

### Dependencies
- **pandas >= 1.3.0**: Data manipulation
- **matplotlib >= 3.4.0**: Visualization
- **numpy >= 1.21.0**: Numerical calculations
- **requests >= 2.26.0**: API calls

### API Details
- **Provider**: Alpha Vantage
- **Free Tier**: 5 calls/minute, 500 calls/day
- **Registration**: Free at alphavantage.co
- **Endpoint**: TIME_SERIES_DAILY

### File Paths
- **CSV Storage**: `stock_data.csv` in project directory
- **Charts Storage**: `charts/` subdirectory
- **Demo Data**: `demo_data.csv` included

## Error Handling

### Network Errors
- Timeout handling with fallback to sample data
- API rate limit detection
- Connection error recovery

### File Operations
- Directory auto-creation
- File existence checks
- Permission error handling

### User Input
- Symbol validation
- Menu choice verification
- Empty input defaults

## Output Examples

### Analysis Summary
```
============================================================
ANALISI COMPLETA: AAPL
============================================================

[INFO GENERALI]
  Simbolo:        AAPL
  Giorni analizzati: 90

[STATISTICHE PREZZO]
  Prezzo Corrente: $172.50
  Massimo:        $184.20
  Minimo:         $150.25
  Media:          $171.23
  Variazione:     $33.95 (22.6%)

[VOLATILITA']
  Deviazione Std: $8.45
  Volatilita':    4.93%
  Livello:        Bassa

[TREND]
  Variazione giornaliera media: $0.3680
  Trend attuale: RIALZISTA FORTE
```

## Windows Compatibility

- **No Unicode/Emoji**: ASCII characters only
- **Path Handling**: Raw strings for Windows paths
- **Display**: Matplotlib configured for Windows
- **Encoding**: UTF-8 for file operations

## Testing

### Verification Script
Run `test_setup.py` to verify:
1. All dependencies installed
2. Directory structure created
3. Basic functionality working

### Sample Data Included
`demo_data.csv` provides 90 days of realistic stock data for testing without API.

## Extension Ideas

Students can extend this project with:
1. **Additional Indicators**: RSI, MACD, Bollinger Bands
2. **Multiple Stocks**: Portfolio comparison
3. **News Integration**: Sentiment analysis
4. **Advanced ML**: LSTM neural networks for prediction
5. **Web Interface**: Flask/Django web app
6. **Database**: SQLite for historical data storage
7. **Real-time Updates**: WebSocket integration

## Learning Outcomes

After completing this project, students will understand:
- Working with real-world financial data
- Statistical analysis and interpretation
- Data visualization techniques
- API integration and error handling
- File I/O operations
- Basic machine learning concepts
- Software development best practices

## Notes

- Educational project, not for real trading
- All calculations simplified for learning
- API key optional (sample data works great)
- Italian language for Italian students
- Cross-platform compatible (Windows tested)

---

**Project Location**: `C:\Users\matti\Desktop\Project Ideas Portfolio\04-Python-Projects\stock-analyzer\`

**Main Script**: `stock_analyzer.py`

**Quick Start**: See `QUICKSTART.md`

**Full Documentation**: See `README.md`
