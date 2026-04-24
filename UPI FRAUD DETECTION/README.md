# UPI Fraud Detection

A machine learning web application built with Flask and TensorFlow/Keras to detect fraudulent UPI transactions based on transaction details.

## Project Structure
- **app.py**: Main Flask application file containing routing and prediction logic.
- **src/**: Directory containing Jupyter notebooks used to build and evaluate the model, along with data files.
- **model/**: Pre-trained TensorFlow `.h5` model files.
- **dataset/**: Contains the historical UPI Fraud details datasets used in modeling.
- **templates/**: HTML pages for the interactive web frontend system.
- **static/**: Static assets like CSS styles, JavaScript behavior files, and images.

## Features
- **Interactive Web Interface**: Complete dashboard for analyzing and previewing datasets.
- **Fraud Check Utility**: Form where transaction details (date, account details, category, amount, etc.) can be passed to verify for fraudulence in real-time.
- **Statistics View**: Real-time analytical chart views visualizing transaction behaviors.

## Setup Instructions

1. **Clone the repository** installed locally (or via Github) and open the parent directory.
2. **Install all required dependencies** using the provided `requirements.txt`:
   ```shell
   pip install -r requirements.txt
   ```
3. **Run the Flask Web Application**:
   ```shell
   python app.py
   ```
4. **Access the platform**: Open your browser and navigate to `http://127.0.0.1:5000`.
