# AI Student Performance Prediction System

An intelligent system that predicts student academic performance and provides personalized learning recommendations using machine learning algorithms.

## Features

- **Performance Prediction**: Predict student performance levels based on various academic and engagement metrics
- **Personalized Learning**: Generate customized learning recommendations for each student
- **Batch Processing**: Process multiple student records at once
- **RESTful API**: Easy-to-use API endpoints for integration
- **Data Preprocessing**: Automatic data cleaning and feature engineering
- **Comprehensive Analytics**: Performance analysis and insights

## Project Structure

```
AI-Student-Performance/
├── api/
│   ├── __init__.py          # Flask app initialization
│   ├── config.py            # Configuration settings
│   └── routes.py            # API endpoints
├── src/
│   ├── prediction_engine.py # ML prediction models
│   ├── personalized_learning.py # Learning recommendations
│   ├── data_preprocessing.py # Data preprocessing
│   ├── utils.py             # Utility functions
│   └── models/              # Trained ML models
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS)
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Alexanderdoppalapudi/AI-Student-Performance.git
   cd AI-Student-Performance
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## API Endpoints

### Prediction Endpoints

- **POST `/api/predict`** - Make a single prediction
  ```json
  {
    "student_id": "STU001",
    "assignment_score": 85,
    "attendance": 90,
    "engagement_level": 4,
    "study_hours": 5,
    "subject": "Math"
  }
  ```

- **POST `/api/batch-predict`** - Predict for multiple students
  ```json
  {
    "students": [
      {"student_id": "STU001", ...},
      {"student_id": "STU002", ...}
    ]
  }
  ```

### Learning Recommendations

- **POST `/api/learning-recommendations`** - Get personalized recommendations
- **GET `/api/performance-levels`** - Get performance level definitions

### Utility Endpoints

- **POST `/api/preprocess`** - Preprocess student data
- **GET `/api/health`** - Health check

## Usage Examples

### Python Request

```python
import requests
import json

url = 'http://localhost:5000/api/predict'
data = {
    'student_id': 'STU001',
    'assignment_score': 85,
    'attendance': 90,
    'engagement_level': 4,
    'study_hours': 5,
    'subject': 'Math',
    'performance_level': 'Good'
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

### cURL Request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "assignment_score": 85,
    "attendance": 90,
    "engagement_level": 4,
    "study_hours": 5,
    "subject": "Math"
  }'
```

## Performance Levels

| Level | GPA Range | Description |
|-------|-----------|-------------|
| Excellent | 3.7 - 4.0 | Outstanding performance |
| Very Good | 3.3 - 3.6 | Excellent work |
| Good | 3.0 - 3.2 | Above average |
| Satisfactory | 2.7 - 2.9 | Meets requirements |
| Needs Improvement | 2.0 - 2.6 | Below expectations |
| At Risk | 0.0 - 1.9 | Critical attention needed |

## Machine Learning Models

The system uses multiple machine learning models:

- **XGBoost**: Primary prediction model
- **LightGBM**: Secondary model for comparison
- **Scikit-learn**: For data preprocessing and feature engineering
- **TensorFlow/Keras**: For deep learning capabilities

## Personalized Learning Recommendations

The system provides:

- **Study Schedule**: Customized study time recommendations
- **Learning Resources**: Subject-specific learning materials
- **Focus Areas**: Areas needing improvement
- **Study Techniques**: Evidence-based study methods
- **Peer Support**: Collaboration and tutoring options
- **Motivation**: Personalized encouragement messages

## Configuration

Edit `.env` file to configure:

```env
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///student_performance.db
LOG_LEVEL=INFO
```

## Testing

Run tests with pytest:

```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

## Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Alexander Doppalapudi**
- GitHub: [@Alexanderdoppalapudi](https://github.com/Alexanderdoppalapudi)
- Email: alexanderdoppalapudi029@gmail.com

## Support

For support, email alexanderdoppalapudi029@gmail.com or open an issue in the repository.

## Acknowledgments

- Scikit-learn for ML utilities
- XGBoost and LightGBM for gradient boosting
- Flask for web framework
- TensorFlow/Keras for deep learning
