# Budget Tracker

#### Video Demo: https://youtu.be/SUt3mS0fOHo

#### Description

This is my final project for CS50x — a simple personal expense tracker web application called **Budget Tracker**.
The idea came from the fact that I always wanted to keep better track of where my money goes every month, but most apps felt either too complicated or required subscriptions. So I decided to build something straightforward that does exactly what I need: log expenses quickly, see recent ones, check full history, and get summaries by category and by month.

The app lets you:
- Register and log in (with password hashing for security)
- Add expenses with amount, category, optional description and date
- See your 10 most recent expenses right on the home page + your total spending so far
- View the complete list of all expenses
- Get breakdowns: how much spent per category (Food, Transport, etc.) and monthly totals for the last year

I built it using **Python + Flask + SQLite**, which felt like the natural choice after doing the Finance problem set. Everything runs locally, no external APIs or cloud services — just pure backend + simple frontend with Bootstrap for decent looks without writing tons of CSS.

### Why this project?

Honestly, I wanted something useful that I might actually keep using after the course ends.
Also, it gave me a chance to practice almost everything from the second half of CS50:
- sessions and user authentication
- SQL queries (SELECT with ORDER BY, SUM + GROUP BY, strftime for dates)
- form handling and basic validation
- Jinja templating and Bootstrap layout
- flash messages for user feedback

### Files I created / modified

- **app.py**
  The heart of the application. All routes, database connection, logic for adding expenses, summaries, login/register/logout.
  I reused the login_required decorator and apology function from helpers.py (like in Finance), but wrote the expense-related routes myself.

- **helpers.py**
  Just copied the standard ones from problem set 8 (apology + login_required). Didn't change anything here.

- **templates/layout.html**
  Base template with navbar (Home, Add Expense, History, Summary, Log Out). Used Bootstrap 5 CDN for responsiveness.

- **templates/login.html** and **register.html**
  Simple forms, almost identical to Finance but with slightly cleaner Bootstrap classes.

- **templates/index.html**
  Home page — shows total spent, form to add new expense, and table of last 10 entries.
  I decided to put the add form here instead of a separate page because most of the time you're on the home screen anyway.

- **templates/history.html**
  Full list of expenses in a table, sorted newest first.

- **templates/summary.html**
  Two tables: one grouped by category (with totals), second grouped by month (last 12 months).
  This was the most satisfying part — seeing GROUP BY and SUM actually useful.

- **finance.db**
  SQLite database with two tables: users and expenses. Created automatically on first run (after I did touch finance.db to fix the cs50.SQL error).

### Some challenges I ran into

1. At first flask run crashed with "does not exist: finance.db".
   Turns out cs50.SQL doesn't auto-create the file like regular sqlite3 does. Fixed it by running `touch finance.db` in the terminal.

2. Got TemplateNotFound for add.html because I had return render_template("add.html") in the GET part of /add, but I never created that template.
   Solution: moved the form to index.html and changed /add GET to redirect("/") — much cleaner.

3. Spent way too long trying to make dates nice. Ended up defaulting to today's date if user doesn't pick one, and using strftime('%Y-%m') for monthly grouping.

4. Small styling issue — had a link to /static/styles.css but never created the file → 404 errors in console. Just removed the link since Bootstrap was enough.

### How to run it

1. Make sure you're in the project folder
2. `flask run` (or `flask run --host=0.0.0.0` in Codespace)
3. Open the link it gives you
4. Register → log in → start adding expenses

Tested on CS50 Codespace — works fine there.

### What I learned / would improve

This project really helped me get comfortable with full-stack flow in Flask.
I especially liked writing the summary queries — seeing real data aggregated was motivating.

If I had more time I would add:
- Edit/delete expenses
- Categories that user can create themselves
- Charts (maybe with Chart.js)
- Export to CSV

But for the final project scope this feels complete — it's functional, looks decent, solves a real small problem, and uses what we learned in the course.

Thanks to David Malan and the CS50 team — this was an awesome journey!

March 14, 2026
Lviv, Ukraine
