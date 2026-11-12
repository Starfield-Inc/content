# Tech stack

- Backend: Python 3.12 with FastAPI.
- Database: SQLite for the hackathon. We chose it because nobody wants to run a server during a weekend event.
- Frontend: plain JavaScript with Leaflet for the map. We skipped React to save setup time.
- Model: a small gradient boosting model for surge height, trained with scikit-learn.
- Text messages: a free sandbox number from the SMS provider. It can only text numbers the team has verified.
