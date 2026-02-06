# Patient Care Dashboard

A full-stack care management system that helps Care Admins manage patients, their care teams, and track health screening scores over time.

## Features

- **Patient Management**: View, create, edit, and delete patients with comprehensive demographic information
- **Search & Filter**: Search patients by name, email, or phone, and filter by status (active, inactive, discharged)
- **Care Team Assignments**: Assign and unassign care team members (Health Coaches, BHCMs, Psychiatrists) to patients
- **Health Screening Tracking**: Visualize health screening trends over time with interactive charts
- **Pagination**: Efficient navigation through large patient lists

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs`

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **Charts**: Recharts for health screening visualization
- **HTTP Client**: Axios

## Project Structure

```
Cerula/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application and routes
│   │   ├── database.py      # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   └── schemas.py       # Pydantic schemas
│   ├── requirements.txt
│   └── seed_data.py         # Database seeding script
├── frontend/
│   ├── src/
│   │   ├── api/             # API client functions
│   │   ├── components/       # React components
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── types.ts          # TypeScript type definitions
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+ (with pip)
- Node.js 18+ (with npm)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Seed the database with sample data:
   ```bash
   python seed_data.py
   ```

   This will create:
   - 7 care team members (Health Coaches, BHCMs, Psychiatrists)
   - 10 patients with various statuses
   - Care team assignments
   - 6 months of health screening data for each patient

5. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **View Patients**: The home page displays a list of all patients with search and filter capabilities
2. **View Patient Details**: Click on any patient row to view detailed information
3. **Edit Patient**: Click "Edit Patient" on the patient detail page to modify patient information
4. **Create Patient**: Click "Add Patient" on the patient list page
5. **Manage Care Team**: On the patient detail page, assign or unassign care team members
6. **View Health Screenings**: Health screening trends are displayed as a line chart on the patient detail page

## API Endpoints

### Patients
- `GET /api/patients` - List patients (with pagination, search, filter)
- `GET /api/patients/count` - Get total patient count
- `GET /api/patients/{id}` - Get patient details
- `POST /api/patients` - Create a new patient
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

### Care Team Members
- `GET /api/care-team-members` - List care team members (optional role filter)
- `GET /api/care-team-members/{id}` - Get care team member details

### Care Team Assignments
- `GET /api/patients/{patient_id}/care-team-assignments` - Get assignments for a patient
- `POST /api/patients/{patient_id}/care-team-assignments` - Assign a member to a patient
- `DELETE /api/patients/{patient_id}/care-team-assignments/{assignment_id}` - Unassign a member

### Health Screenings
- `GET /api/patients/{patient_id}/health-screenings` - Get health screening history
- `GET /api/health-screenings/{id}` - Get a specific screening

## Design Decisions

### Database Schema

**Patients Table**
- Stores patient demographic information and enrollment details
- Status enum: active, inactive, discharged
- Email is unique and indexed for fast lookups

**Care Team Members Table**
- Stores care team member information
- Role enum: Health Coach, Behavioral Health Care Manager, Psychiatrist
- Email is unique and indexed

**Care Team Assignments Table**
- Many-to-many relationship between patients and care team members
- Includes assigned_date for tracking when assignments were made
- Prevents duplicate assignments

**Health Screenings Table**
- Stores monthly health screening scores (0-10 scale)
- Linked to patients via foreign key
- Screening date allows tracking over time

### API Design

- RESTful API design with clear resource naming
- Pagination implemented using `skip` and `limit` query parameters
- Search functionality across multiple fields (name, email, phone)
- Status filtering for patients
- Comprehensive error handling with appropriate HTTP status codes
- Input validation using Pydantic schemas

### Frontend Architecture

- Component-based architecture with separation of concerns
- TypeScript for type safety
- API client abstraction for easy maintenance
- Responsive design for mobile and desktop
- Error handling and loading states throughout

### Health Screening Visualization

- Line chart showing score trends over time
- Color-coded scores (red for high ≥7, yellow for medium 4-7, green for low <4)
- Average score and trend indicators
- Table view for detailed screening history
- Sorted chronologically to show progression

### User Experience

- Intuitive navigation with breadcrumbs
- Confirmation dialogs for destructive actions
- Real-time search and filtering
- Clear visual indicators for patient status
- Responsive tables and forms
- Loading and error states

## Assumptions & Limitations

### Assumptions
- Health screenings are pre-stored (no UI for creating new screenings)
- One screening per patient per month
- Care team members can be assigned to multiple patients
- Patients can have multiple care team members
- Email addresses are unique identifiers

### Limitations
- SQLite database (suitable for development, consider PostgreSQL for production)
- No authentication/authorization (assumes single admin user)
- No audit logging
- No soft deletes (patients are permanently deleted)
- Health screenings are read-only (no edit/delete functionality)

## Future Enhancements

- User authentication and role-based access control
- Audit logging for patient and assignment changes
- Export functionality (CSV, PDF)
- Advanced filtering and sorting options
- Bulk operations (assign multiple members, bulk status updates)
- Email notifications for care team assignments
- Dashboard with aggregated statistics
- Patient notes/comments functionality
- Integration with external health systems

## Testing

To test the application:

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Use the seeded data to explore functionality:
   - Search for "John" or "Jane"
   - Filter by "Active" status
   - Click on a patient to view details
   - Assign a care team member
   - View health screening trends
   - Create a new patient
   - Edit patient information

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

**Frontend won't start:**
- Ensure Node.js 18+ is installed
- Check that all dependencies are installed: `npm install`
- Verify port 3000 is not in use

**Database errors:**
- Delete `patient_care.db` and run `seed_data.py` again
- Ensure SQLite is available (usually included with Python)

**CORS errors:**
- Ensure backend is running on port 8000
- Check that CORS middleware is configured correctly in `main.py`

## License

This project is created for assessment purposes.
