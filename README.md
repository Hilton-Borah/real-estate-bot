# Real Estate Chatbot

An interactive chatbot application for real estate analysis and insights. This project consists of a React frontend and Django backend, providing real-time property analysis and market trends.

## Features

- 🏠 Real-time property market analysis
- 📊 Interactive data visualizations
- 💬 Natural language query processing
- 📈 Price trend comparisons
- 🗺️ Area-wise market insights
- 📱 Responsive design for all devices

## Project Structure

```
real_estate_chatbot/
├── real-estate-frontend/     # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── assets/         # Static assets
│   │   └── index.css       # Global styles
│   ├── public/             # Public assets
│   └── package.json        # Frontend dependencies
│
└── backend/                # Django backend application
    ├── chatbot/           # Chatbot logic
    ├── real_estate_chatbot/# Django project settings
    ├── manage.py          # Django management script
    └── requirements.txt   # Backend dependencies
```

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd real-estate-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the backend server:
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000`

## Technologies Used

### Frontend
- React 18
- Vite
- TailwindCSS
- Heroicons
- Chart.js for visualizations

### Backend
- Django
- Django REST Framework
- SQLite database
- Python data analysis libraries

## Usage Examples

1. Property Analysis:
   ```
   "Analyze property trends in Wakad"
   ```

2. Area Comparison:
   ```
   "Compare prices in Aundh and Baner"
   ```

3. Rental Trends:
   ```
   "Show rental trends in Kothrud"
   ```

## API Endpoints

- `POST /api/analyze/`
  - Analyzes real estate queries
  - Request body: `{ "query": "your query here" }`
  - Returns: `{ "summary": "analysis", "chart_data": {...}, "table_data": {...} }`

## Styling and UI

The application uses TailwindCSS for styling with a responsive design:
- Full viewport width layout (1520px)
- Professional gradient headers
- Responsive message bubbles
- Interactive loading animations
- Clean card-based interface

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the development team.

## Acknowledgments

- Built with React and Django
- Styled with TailwindCSS
- Icons from Heroicons
- Charts powered by Chart.js 