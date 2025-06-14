from datetime import datetime
import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class Journal:
    def __init__(self, filename="entries.json"):
        self.filename = filename
        self.entries = []
        self.console = Console()
        self.load_entries()

    def load_entries(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.entries = json.load(f)
        else:
            self.entries = []

    def save_entries(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def mood_message(self, mood_rating):
        messages = {
            1: "[bold red]Cheer up! Tomorrow is a new day.[/bold red]",
            2: "[yellow]Hang in there![/yellow]",
            3: "[cyan]Not bad! Keep going![/cyan]",
            4: "[green]Great job![/green]",
            5: "[bold green]You're on fire today![/bold green]"
        }
        return messages.get(mood_rating, "")

    def add_entry(self):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": input("Entry Title: "),
            "events": input("Main Events: "),
            "feelings": input("How did you feel today? "),
            "notes": input("Additional Notes: "),
            "forget": input("Things I Wish to Forget: ")
        }
        while True:
            try:
                mood = int(input("Rate your mood (1-5): "))
                if 1 <= mood <= 5:
                    entry["mood"] = mood
                    break
                else:
                    self.console.print("[red]Please enter a number between 1 and 5.[/red]")
            except ValueError:
                self.console.print("[red]Invalid input. Please enter a number.[/red]")
        self.entries.append(entry)
        self.save_entries()
        self.console.print(Panel(self.mood_message(entry["mood"]), title="Mood Message", expand=False))
        self.console.print("[green]Journal entry added and saved.[/green]\n")

    def view_entries(self):
        if not self.entries:
            self.console.print("[red]No journal entries found.[/red]\n")
            return
        table = Table(title="Journal Entries", show_lines=True)
        table.add_column("No.", style="cyan", width=4)
        table.add_column("Date", style="magenta")
        table.add_column("Title", style="yellow")
        table.add_column("Events", style="white")
        table.add_column("Feelings", style="white")
        table.add_column("Mood", style="bold green")
        table.add_column("Forget", style="red")
        table.add_column("Notes", style="white")
        for idx, entry in enumerate(self.entries, 1):
            table.add_row(
                str(idx),
                entry.get("date", ""),
                entry.get("title", ""),
                entry.get("events", ""),
                entry.get("feelings", ""),
                str(entry.get("mood", "")),
                entry.get("forget", ""),
                entry.get("notes", "")
            )
        self.console.print(table)

    def search_by_mood(self):
        try:
            mood = int(input("Enter the mood rating to search for (1-5): "))
            if not (1 <= mood <= 5):
                self.console.print("[red]Please enter a number between 1 and 5.[/red]")
                return
        except ValueError:
            self.console.print("[red]Invalid input. Please enter a number.[/red]")
            return

        filtered = [entry for entry in self.entries if entry.get("mood") == mood]
        if not filtered:
            self.console.print(f"[yellow]No entries found with mood rating {mood}.[/yellow]\n")
            return

        table = Table(title=f"Journal Entries with Mood {mood}", show_lines=True)
        table.add_column("No.", style="cyan", width=4)
        table.add_column("Date", style="magenta")
        table.add_column("Title", style="yellow")
        table.add_column("Events", style="white")
        table.add_column("Feelings", style="white")
        table.add_column("Mood", style="bold green")
        table.add_column("Forget", style="red")
        table.add_column("Notes", style="white")
        for idx, entry in enumerate(filtered, 1):
            table.add_row(
                str(idx),
                entry.get("date", ""),
                entry.get("title", ""),
                entry.get("events", ""),
                entry.get("feelings", ""),
                str(entry.get("mood", "")),
                entry.get("forget", ""),
                entry.get("notes", "")
            )
        self.console.print(table)

def main_menu():
    journal = Journal()
    while True:
        print("Personal Journal Menu:")
        print("1. Create a new journal entry")
        print("2. View all journal entries")
        print("3. Search entries by mood")
        print("4. Exit")
        choice = input("Select an option (1-4): ")
        if choice == "1":
            journal.add_entry()
        elif choice == "2":
            journal.view_entries()
        elif choice == "3":
            journal.search_by_mood()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

if __name__ == "__main__":
    main_menu()