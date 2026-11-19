# FitTrack Workout Tracker

FitTrack is a Flask and SQLite application for viewing muscle groups, gym equipment, and workout sessions. It uses Flask-SQLAlchemy models, domain Blueprints, separate route modules, manager functions, controller classes, templates, and domain-specific exceptions.

## Phase 1: Project proposal and database design

The team proposed FitTrack as a way for students, gym-goers, and people who train independently to keep workout records and progress information organized. The proposal described the problem of workout notes, exercise details, and progress photos being scattered across different places. It outlined a Flask and SQLite application and planned a dashboard, exercise catalog, workout logger, and workout history.

The Phase 1 database design has five related tables: `muscle_group`, `equipment`, `exercise`, `workout_session`, and `workout_exercise`. Exercises connect to a muscle group and equipment. `workout_exercise` connects workout sessions and exercises and stores sets, reps, and weight. The project includes an ER diagram and sample data; the Phase 1 documentation reports 54 records across the five tables.

## Phase 2: Flask application and MVC structure

Phase 2 built the initial application using Flask, Flask-SQLAlchemy, and the SQLite database. It organized the app into domain packages and added models, managers, controller classes, Blueprints, separate route modules, templates, and domain-specific exceptions. The application displays muscle groups, equipment, and workout sessions on separate pages. Database read errors are rolled back and handled centrally with user-friendly error feedback. The project includes `requirements.txt`, the Phase 1 proposal, and Phase 2 documentation.

## Requirements

- Python 3.10 or newer
- Flask
- Flask-SQLAlchemy

## Run the application

1. Create and activate a virtual environment.
2. Install the packages listed in `requirements.txt` with `pip install -r requirements.txt`.
3. From this project folder, run `python app.py`.
4. Open the local address shown in the terminal. The home page links to the three list pages.

The application uses `instance/strength_training.db`. The included database contains sample records. The application will create any missing tables when it starts and will not remove existing data.

## Pages

- `/muscle-groups` — muscle group records
- `/equipment` — equipment records
- `/workouts` — workout session records

### Equipment filtering and sorting

The Equipment page form submits filter and sort choices as URL query parameters. For example:

```text
/equipment?category=Free%20weights&sort_by=name&sort_order=asc&limit=5
```

`category` is optional. `sort_by` can be `name`, `category`, or `target_muscle_focus`; `sort_order` can be `asc` or `desc`; and `limit` must be a positive whole number. Invalid sort choices or limits display a validation message.

### Muscle group search

Search muscle group names, target regions, and descriptions with one or more words. All search terms must match, although each term may match a different field. For example:

```text
/muscle-groups?search=upper%20body
```

## Project structure

```text
app/
  core/models.py          Exercise and WorkoutExercise models
  equipment/              equipment model, manager, controller, routes, Blueprint, template
  muscle_group/           muscle group model, manager, controller, routes, Blueprint, template
  workout_session/        workout session model, manager, controller, routes, Blueprint, template
  static/                 shared CSS
  templates/              home and shared error pages
database.py               SQLite connection setup
extensions.py             shared SQLAlchemy instance
app.py                    application entry point
instance/
  strength_training.db    SQLite database with sample records
requirements.txt          pinned Python dependencies
```

## Database tables

The five SQLAlchemy models map to `muscle_group`, `equipment`, `exercise`, `workout_session`, and `workout_exercise`. `MuscleGroup` and `Equipment` are in their respective domain packages, `WorkoutSession` is in the workout-session package, and the shared `Exercise` and `WorkoutExercise` models are in `app/core/models.py`. ORM relationships connect muscle groups to exercises, equipment to exercises, and workout sessions to their exercises. The `workout_exercise` association table stores sets, reps, and weight.

## Phase 3: Advanced queries and related data

Phase 3 builds on the existing FitTrack application by adding search, filtering, sorting, result limits, and related-data displays.

- **Equipment filtering, sorting, and limits:** On `/equipment`, users can filter equipment by category, sort by name, category, or target muscle focus in ascending or descending order, and set a maximum number of results. The controller validates that a result limit is a positive whole number.
- **Multi-term muscle group search:** On `/muscle-groups`, users can search muscle group names, target regions, and descriptions. Every entered term must match, while each term may match any of those three fields. The page includes search, clear, and no-results feedback.
- **Related exercises and equipment:** The Muscle Groups page displays exercises associated with each muscle group, including mechanic type, difficulty level, and equipment name and category. It accesses the SQLAlchemy relationships from MuscleGroup to Exercise and from Exercise to Equipment. Muscle groups without exercises display a message.
- **Workout sessions:** The `/workouts` page displays sessions by date, rating, and notes, with the newest sessions first.
- **Error handling:** Database query errors are rolled back and handled by the application's central error handler, which displays a user-friendly error page.

These updates extend the Phase 1 database design and Phase 2 Flask application structure. Search and relationship loading are implemented in `app/muscle_group/muscle_group_manager.py`; the Muscle Groups page displays related exercises and equipment through ORM relationship attributes. Styles for the Muscle Groups page are served from `app/static/muscle_group.css`. Domain-specific data exceptions are handled by the central application error handler in `app/__init__.py`.
