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

4. Set up the database schema and seed data:
   ```bash
   python seed_data.py
   ```

   This script will:
   - Automatically create all database tables (if they don't exist)
   - Seed the database with sample data:
     - 7 care team members (Health Coaches, BHCMs, Psychiatrists)
     - 10 patients with various statuses (active, inactive, discharged)
     - Care team assignments linking members to patients
     - 6 months of health screening data for each patient (60 screenings total)
   
   **Note**: The seed script is idempotent - it's safe to run multiple times. It only adds data that doesn't already exist, so you won't get duplicates.

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

## API Documentation

The API is built with FastAPI and provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs` (or your deployed URL + `/docs`)
- **ReDoc**: `http://localhost:8000/redoc` (alternative documentation format)
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` (machine-readable schema)

### API Endpoints

#### Patients

**List Patients**
- `GET /api/patients` - List patients with pagination, search, and filtering
  - Query Parameters:
    - `skip` (int, default: 0) - Number of records to skip
    - `limit` (int, default: 20, max: 100) - Number of records to return
    - `search` (string, optional) - Search by name, email, or phone
    - `status` (string, optional) - Filter by status: `active`, `inactive`, or `discharged`
  - Response: Array of patient objects
  - Example: `GET /api/patients?search=john&status=active&limit=10`

**Get Patient Count**
- `GET /api/patients/count` - Get total count of patients matching filters
  - Query Parameters: Same as list patients (`search`, `status`)
  - Response: `{"count": 10}`

**Get Patient Details**
- `GET /api/patients/{id}` - Get detailed patient information including care team and screenings
  - Path Parameter: `id` (int) - Patient ID
  - Response: Patient object with nested care_team_assignments and health_screenings

**Create Patient**
- `POST /api/patients` - Create a new patient
  - Request Body: Patient object (JSON)
    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "date_of_birth": "1990-01-01",
      "enrollment_date": "2024-01-01",
      "status": "active",
      "phone": "555-1234",
      "address": "123 Main St",
      "care_program": "Behavioral Health Program"
    }
    ```
  - Response: Created patient object (201 Created)

**Update Patient**
- `PUT /api/patients/{id}` - Update patient information
  - Path Parameter: `id` (int) - Patient ID
  - Request Body: Partial patient object (all fields optional)
  - Response: Updated patient object

**Delete Patient**
- `DELETE /api/patients/{id}` - Delete a patient
  - Path Parameter: `id` (int) - Patient ID
  - Response: 204 No Content

#### Care Team Members

**List Care Team Members**
- `GET /api/care-team-members` - List all care team members
  - Query Parameters:
    - `role` (string, optional) - Filter by role: `Health Coach`, `Behavioral Health Care Manager`, or `Psychiatrist`
  - Response: Array of care team member objects
  - Example: `GET /api/care-team-members?role=Health Coach`

**Get Care Team Member**
- `GET /api/care-team-members/{id}` - Get care team member details
  - Path Parameter: `id` (int) - Member ID
  - Response: Care team member object

#### Care Team Assignments

**Get Patient Assignments**
- `GET /api/patients/{patient_id}/care-team-assignments` - Get all care team assignments for a patient
  - Path Parameter: `patient_id` (int) - Patient ID
  - Response: Array of assignment objects with nested care_team_member

**Assign Care Team Member**
- `POST /api/patients/{patient_id}/care-team-assignments` - Assign a care team member to a patient
  - Path Parameter: `patient_id` (int) - Patient ID
  - Request Body:
    ```json
    {
      "care_team_member_id": 1,
      "assigned_date": "2024-01-01"  // optional, defaults to today
    }
    ```
  - Response: Created assignment object (201 Created)

**Unassign Care Team Member**
- `DELETE /api/patients/{patient_id}/care-team-assignments/{assignment_id}` - Remove an assignment
  - Path Parameters:
    - `patient_id` (int) - Patient ID
    - `assignment_id` (int) - Assignment ID
  - Response: 204 No Content

#### Health Screenings

**Get Patient Health Screenings**
- `GET /api/patients/{patient_id}/health-screenings` - Get health screening history for a patient
  - Path Parameter: `patient_id` (int) - Patient ID
  - Response: Array of health screening objects, ordered by date (newest first)
  - Each screening includes: `id`, `patient_id`, `screening_date`, `score` (0-10)

**Get Health Screening**
- `GET /api/health-screenings/{id}` - Get a specific health screening
  - Path Parameter: `id` (int) - Screening ID
  - Response: Health screening object

### API Response Format

All endpoints return JSON. Error responses follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP Status Codes:
- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input/validation error
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Authentication

Currently, the API does not require authentication. In production, you would add API keys or OAuth tokens.

## Design Decisions

### Database Schema

The database schema is automatically created when you run the application or seed script using SQLAlchemy's `Base.metadata.create_all()`. No manual migrations are required for initial setup.

**Database Setup Process:**
1. Tables are created automatically on first run via `Base.metadata.create_all(bind=engine)`
2. Seed data is populated via `seed_data.py` script
3. For production (PostgreSQL), the same process applies - tables are created automatically

**Schema Details:**

**Patients Table**
- Primary Key: `id` (auto-incrementing integer)
- Fields: `first_name`, `last_name`, `date_of_birth`, `email` (unique, indexed), `phone`, `address`, `enrollment_date`, `status` (enum), `care_program`
- Status enum: `active`, `inactive`, `discharged`
- Relationships: One-to-many with CareTeamAssignment, One-to-many with HealthScreening

**Care Team Members Table**
- Primary Key: `id` (auto-incrementing integer)
- Fields: `first_name`, `last_name`, `email` (unique, indexed), `phone`, `role` (enum)
- Role enum: `Health Coach`, `Behavioral Health Care Manager`, `Psychiatrist`
- Relationships: One-to-many with CareTeamAssignment

**Care Team Assignments Table**
- Primary Key: `id` (auto-incrementing integer)
- Foreign Keys: `patient_id` → Patients.id, `care_team_member_id` → CareTeamMembers.id
- Fields: `assigned_date` (defaults to current date)
- Unique Constraint: Prevents duplicate assignments (same patient + member combination)
- Represents: Many-to-many relationship between patients and care team members

**Health Screenings Table**
- Primary Key: `id` (auto-incrementing integer)
- Foreign Key: `patient_id` → Patients.id
- Fields: `screening_date`, `score` (float, 0-10 scale)
- Purpose: Tracks monthly behavioral health screening scores over time

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
