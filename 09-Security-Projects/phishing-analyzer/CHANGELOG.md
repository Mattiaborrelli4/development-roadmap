# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-12

### Added
- Initial release of Phishing Email Analyzer
- SPF, DKIM, DMARC header analysis
- Link inspection for suspicious URLs
- Sender verification with spoofing detection
- Content analysis for phishing patterns
- Risk calculation algorithm
- Educational explanations for each finding
- CLI interface with multiple commands
- Italian language support
- Sample phishing email for testing
- Comprehensive test suite

### Features
- **Header Analysis**
  - SPF record checking
  - DKIM signature validation
  - DMARC policy verification
  - Authentication results parsing

- **Link Analysis**
  - Typosquatting detection
  - IP address URLs
  - Suspicious TLD detection
  - HTTPS verification
  - Shortened URL detection
  - Lookalike character detection

- **Sender Analysis**
  - Domain spoofing detection
  - Display name mismatch
  - Reply-To verification
  - Return-Path analysis
  - Free email domain detection

- **Content Analysis**
  - Urgency keyword detection
  - Pressure tactics identification
  - Credential request detection
  - Financial keyword scanning
  - Attachment analysis

### CLI Commands
- `analyze` - Analyze email files
- `analyze --stdin` - Read from stdin
- `check-links` - Check URLs for indicators
- `check-domain` - Verify DNS configuration
- `explain-spf` - Explain SPF
- `explain-dmarc` - Explain DMARC
- `explain-dkim` - Explain DKIM
- `learn` - Display educational guide

### Documentation
- Comprehensive README in Italian
- Educational content on phishing
- Best practices for email security
- How to report phishing
- Code comments throughout

## [Unreleased]

### Planned
- Multi-language support (English, Spanish)
- Web interface
- Database of known phishing campaigns
- Machine learning integration
- API endpoints
- Docker support
