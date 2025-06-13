# Data Contract Portal

A comprehensive web application for creating, managing, and auto-generating data contracts from various sources including databases, APIs, and files.

## Features

- **Manual Contract Creation**: Build data contracts field by field with custom types and validation rules
- **Auto-Generation**: Automatically generate contracts from multiple sources
- **Search & Filter**: Quickly find contracts using the built-in search functionality
- **Export Capabilities**: Download contracts as JSON files
- **Copy to Clipboard**: Share contracts easily with one-click copying
- **Responsive Design**: Fully responsive interface that works on all devices

## Table of Contents

- [Getting Started](#getting-started)
- [Auto-Generation Features](#auto-generation-features)
- [Manual Contract Creation](#manual-contract-creation)
- [Contract Management](#contract-management)
- [Data Types](#data-types)
- [Examples](#examples)
- [Browser Compatibility](#browser-compatibility)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional installations required - runs entirely in the browser

### Installation

1. **GitHub Pages Deployment**:
   ```bash
   # Clone or download the repository
   git clone <your-repository-url>
   
   # Save the HTML file as index.html in your repository
   # Enable GitHub Pages in repository settings
   ```

2. **Local Development**:
   ```bash
   # Simply open index.html in your web browser
   # Or serve it using a local server:
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

3. **Direct Usage**:
   - Download the `index.html` file
   - Open it directly in your web browser
   - No server setup required

## Auto-Generation Features

The Data Contract Portal's auto-generation feature is designed to streamline the contract creation process by analyzing existing data sources and automatically inferring schema structures.

### Database Schema Import

**Purpose**: Convert SQL database schemas into standardized data contracts.

**How it works**:
1. **Schema Parsing**: The system parses SQL DDL statements to extract table structure
2. **Type Mapping**: SQL data types are automatically mapped to contract data types
3. **Constraint Detection**: NOT NULL constraints are converted to required field indicators
4. **Field Analysis**: Each column becomes a contract field with appropriate metadata

**Supported SQL Types**:
```sql
VARCHAR/TEXT     → string
INT/INTEGER      → integer
BOOLEAN          → boolean
TIMESTAMP        → timestamp
FLOAT/DECIMAL    → float
```

**Example Usage**:
```sql
-- Input Schema
CREATE TABLE customers (
    id
