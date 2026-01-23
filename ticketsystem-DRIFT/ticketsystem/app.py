from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = "tickets.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    first_run = not os.path.exists(DATABASE)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            solved INTEGER DEFAULT 0,
            solution TEXT
        )
    """)

    if first_run:
        tickets = [
            (
                "Statisk internett",
                "sett opp statisk IP for internettforbindelse",
                "Lett",
            ),
            (
                "Feilsøk WiFi",
                "bruk verktøy for å finne og fikse WiFi-problemer",
                "Middels",
            ),
            (
                "Installer programvare",
                "installer nødvendig programvare på nye maskiner, discord, steam og annet man trenger til gaming",
                "Lett",
            ),
            (
                "Sikkerhetskopiering",
                "sett opp automatiske sikkerhetskopier for dokumenter mappen",
                "Vanskelig",
            ),
            (
                "Oppdater drivere",
                "sjekk og oppdater alle maskinvaredrivere til nyeste versjon",
                "Middels",
            ),
            (
                "Sikkerhet",
                "Gjør PCen min ekstra trygg mot virus og hackere.",
                "Vanskelig.",
            ),
            ("Personalisering", "Jeg vil bytte bakgrunnsbilde.", "Enkel."),
            (
                "HTTP-Server",
                "Jeg skal kjøre en Python HTTP-server fra maskinen.",
                "Vanskelig.",
            ),
        ]

        cursor.executemany(
            "INSERT INTO tickets (title, description, difficulty) VALUES (?, ?, ?)",
            tickets,
        )

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()

    unsolved_tickets = conn.execute("SELECT * FROM tickets WHERE solved = 0").fetchall()

    solved_tickets = conn.execute("SELECT * FROM tickets WHERE solved = 1").fetchall()

    conn.close()

    return render_template(
        "index.html", unsolved_tickets=unsolved_tickets, solved_tickets=solved_tickets
    )


@app.route("/ticket/<int:ticket_id>")
def ticket(ticket_id):
    conn = get_db_connection()
    ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    conn.close()

    if ticket is None:
        return "Ticket not found", 404

    return render_template("ticket.html", ticket=ticket)


@app.route("/solve/<int:ticket_id>", methods=["POST"])
def solve(ticket_id):
    solution = request.form["solution"]

    conn = get_db_connection()
    conn.execute(
        "UPDATE tickets SET solved = 1, solution = ? WHERE id = ?",
        (solution, ticket_id),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
