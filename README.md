# Automated Data Classification & Governance System

## Overview

This project is a prototype system that demonstrates automated data classification and governance policy enforcement. It classifies structured data into sensitivity levels and applies governance rules such as retention policies and security controls.

The system simulates real-world enterprise data governance workflows using mock datasets.

## Features

* Upload and process CSV datasets
* Automatic data classification:

  * Public
  * Internal
  * Confidential
  * Highly Sensitive
* Governance rule application:

  * Retention policies
  * Security handling recommendations
* Sensitive data masking and redaction
* Interactive web interface using Streamlit
* Export options:

  * CSV report
  * Text report
  * PDF report with tables and charts


## System Workflow

1. Upload dataset
2. Run classification and governance processing
3. View results in dashboard
4. Download reports


## Technologies Used

* Python
* Pandas
* Streamlit
* ReportLab (PDF generation)
* Matplotlib (data visualization)

## Project Structure

data_governance_system/
│
├── app.py
├── modules/
│   ├── parser.py
│   ├── classifier.py
│   ├── governance.py
│   └── report_generator.py
├── utils/
│   ├── masking.py
│   └── pdf_report.py
├── data/
│   └── sample_dataset.csv
└── README.md

## How to Run

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run the application

streamlit run app.py

## Security Considerations

* The system uses mock datasets only
* Data is processed in-memory (session-based)
* No permanent storage of uploaded data
* Sensitive fields are masked or redacted in outputs

## Scope & Limitations

* Designed for small to medium datasets (up to ~10,000 records)
* Uses rule-based classification (no machine learning yet)
* Limited to CSV input format


## Future Improvements

* Integrate machine learning for improved classification
* Add role-based access control
* Expand dataset support (JSON, databases)
* Enhance report visualization and analytics

## Author

Naika Jean

## License

This project is for educational purposes.
