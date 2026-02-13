# Stock Price Analyzer - Feature Overview

## Main Features Checklist

### Data Acquisition
- [x] Fetch from Alpha Vantage API
- [x] Sample data generation (no API key needed)
- [x] CSV export functionality
- [x] CSV import functionality
- [x] Error handling with fallback

### Analysis Functions
- [x] Moving Averages (20-day)
- [x] Moving Averages (50-day)
- [x] Min/Max price calculation
- [x] Average price calculation
- [x] Median price calculation
- [x] Standard deviation (volatility)
- [x] Linear regression prediction
- [x] Trend identification

### Visualization
- [x] Price line chart
- [x] Moving averages overlay
- [x] Multiple indicators display
- [x] Grid and legend
- [x] Chart export to PNG
- [x] Timestamp in filename

### User Interface
- [x] Main menu system
- [x] Italian language
- [x] ASCII-only (Windows compatible)
- [x] Input validation
- [x] Help section
- [x] Clear error messages

### Educational Features
- [x] Italian docstrings
- [x] Code comments
- [x] Formula explanations
- [x] Interpretation of results
- [x] Investment warnings

## Menu Structure

```
Stock Price Analyzer v1.0
==========================

1. Analyze Stock
   ├─ Input symbol (AAPL, MSFT, etc.)
   ├─ Choose API or Sample Data
   ├─ View chart (yes/no)
   ├─ Save to CSV (yes/no)
   └─ Display full analysis

2. Load from CSV
   ├─ Select CSV file
   ├─ View chart (yes/no)
   └─ Display full analysis

3. View Chart Only
   ├─ Select CSV file
   └─ Display chart

4. List CSV Files
   └─ Show all available files

5. Help
   └─ Display explanations

0. Exit
```

## Analysis Output Example

```
============================================================
ANALISI COMPLETA: AAPL
============================================================

[INFO GENERALI]
  Simbolo:           AAPL
  Periodo:           2024-01-01 to 2024-04-30
  Giorni analizzati: 90

[STATISTICHE PREZZO]
  Prezzo Corrente:   $183.70
  Massimo:           $184.20
  Minimo:            $150.25
  Media:             $171.23
  Mediana:           $175.55
  Variazione:        $33.95 (22.6%)

[VOLATILITA']
  Deviazione Std:    $8.45
  Volatilita':       4.93%
  Livello:           Bassa

[TREND]
  Variazione giornaliera media: $0.3680
  Variazione prevista 30gg:     $11.04
  Trend attuale:      RIALZISTA FORTE
  Suggerimento:       OPPORTUNITA' DI ACQUISTO

============================================================
NOTA: Questa analisi e' solo a scopo educativo.
Non costituisce consiglio di investimento.
============================================================
```

## Key Functions Reference

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `main()` | None | None | Program entry point |
| `fetch_stock_data()` | symbol, use_sample, api_key | DataFrame | Get stock data |
| `calculate_moving_averages()` | prices, days | Series | Calculate SMA |
| `plot_chart()` | dates, prices, ma20, ma50, symbol | str | Create chart |
| `calculate_statistics()` | prices | Dict | Compute stats |
| `predict_trend()` | dates, prices | Tuple | Linear regression |
| `save_to_csv()` | data, filename | str | Export data |
| `load_from_csv()` | filename | DataFrame | Import data |
| `display_analysis()` | data, stats, slope, symbol | None | Show results |

## File Operations

### Reading
```python
data = load_from_csv('demo_data.csv')
# Returns: DataFrame with columns: date, close, volume
```

### Writing
```python
save_to_csv(data, 'my_stock.csv')
# Saves: DataFrame to CSV file
```

### Sample Data Format
```csv
date,close,volume
2024-01-01,150.25,5234000
2024-01-02,152.80,6123000
...
```

## Calculations Explained

### Simple Moving Average (SMA)
```
SMA = (P1 + P2 + ... + Pn) / n
```
Where P = price, n = number of days

### Standard Deviation (Volatility)
```
std = sqrt(sum((x - mean)^2) / n)
```
Measures price variation from average

### Linear Regression
```
y = mx + q
```
Where:
- m = slope (trend direction)
- q = intercept (starting point)
- x = time (days)
- y = price

## Color Scheme

Charts use:
- **Blue**: Closing price
- **Orange**: 20-day moving average
- **Green**: 50-day moving average

## Trend Interpretation

| Slope | Interpretation | Suggestion |
|-------|---------------|-------------|
| > 0.1 | Strong Bullish | Buy Opportunity |
| 0.01 - 0.1 | Weak Bullish | Monitor |
| -0.01 - 0.01 | Neutral/Sideways | Wait |
| -0.01 - -0.1 | Weak Bearish | Monitor |
| < -0.1 | Strong Bearish | Caution - Sell |

## Volatility Levels

| Std Dev % | Level | Meaning |
|-----------|-------|---------|
| < 5% | Low | Stable price |
| 5-10% | Medium | Normal fluctuation |
| > 10% | High | Large swings |

## API Integration

### Alpha Vantage Details
- **Endpoint**: `https://www.alphavantage.co/query`
- **Function**: `TIME_SERIES_DAILY`
- **Output Size**: `compact` (100 days)
- **Rate Limit**: 5 calls/minute (free tier)

### Response Format
```json
{
  "Time Series (Daily)": {
    "2024-01-01": {
      "4. close": "150.25",
      "5. volume": "5234000"
    }
  }
}
```

## Educational Concepts Covered

### Python Skills
- DataFrames (pandas)
- List comprehensions
- Type hints
- Error handling
- File I/O
- API requests
- String formatting

### Math/Statistics
- Averages
- Standard deviation
- Linear regression
- Trend analysis
- Percentage calculations

### Finance
- Stock prices
- Moving averages
- Volatility
- Trading volume
- Technical analysis

## Quick Reference

### Installation
```bash
pip install -r requirements.txt
```

### Run Program
```bash
python stock_analyzer.py
```

### Test Installation
```bash
python test_setup.py
```

### Common Commands
- Analyze with sample data: Select option 1, then choose sample mode
- Load demo data: Select option 2, enter `demo_data.csv`
- View chart only: Select option 3, enter CSV filename
- List files: Select option 4

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | Run `pip install -r requirements.txt` |
| API error | Use sample data mode instead |
| No chart displayed | Check matplotlib installation |
| File not found | Use option 4 to list available files |
| Permission error | Check write permissions in directory |

---

**Ready to use!** Just run `python stock_analyzer.py` and follow the menu prompts.
