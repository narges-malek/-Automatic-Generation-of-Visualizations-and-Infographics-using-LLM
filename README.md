# Automatic Visualization Generator with LLMs

This platform leverages the power of LlamaIndex and Large Language Models (Llama 3.3 and Llama 3.2) to provide automatic data visualizations and insights from uploaded datasets. It simplifies data analysis and visualization through a user-friendly natural language interface.

## Features

- **File Support**: Handles data files in formats such as CSV, Excel, Word, or TXT.
- **Natural Language Interface**: Allows users to interact with their data through natural language queries.
- **Dynamic Visualizations**: Automatically generates visualizations and infographics tailored to the uploaded data.

## Technologies Used

- **Flask**: Manages web requests and responses, acting as the backend server framework.
- **LlamaIndex**: Integrates with LLMs for advanced data processing and analysis.
- **Python venv**: Utilizes virtual environments to manage package dependencies.
- **dotenv**: Manages environment variables for secure API usage.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/visualization-generator-llms.git
   cd visualization-generator-llms

2. Set up a virtual environment:
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   pip install -r requirements.txt

4. Set up environment variables:

Copy .env.example to .env
Update the .env file with your API keys and other configurations.

Usage;
Describe how to use the application, including examples of natural language queries and expected outputs.
