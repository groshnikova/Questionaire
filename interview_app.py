#!/usr/bin/env python3
"""
Interview Questions Practice App
A simple CLI tool to practice interview questions
"""

import json
import os
import sys
from typing import List, Dict

class InterviewApp:
    def __init__(self, questions_file='questions.json'):
        self.questions_file = questions_file
        self.questions = []
        self.load_questions()

    def load_questions(self):
        """Load questions from JSON file"""
        if not os.path.exists(self.questions_file):
            print(f"Error: {self.questions_file} not found!")
            sys.exit(1)

        try:
            with open(self.questions_file, 'r') as f:
                data = json.load(f)
                self.questions = data.get('questions', [])
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.questions_file}")
            sys.exit(1)

    def save_questions(self):
        """Save questions back to JSON file"""
        with open(self.questions_file, 'w') as f:
            json.dump({'questions': self.questions}, f, indent=2)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("Interview Questions Practice App")
        print("="*50)
        print("\n1. Practice all questions")
        print("2. Practice by category")
        print("3. Practice unanswered questions")
        print("4. View all questions")
        print("5. Reset progress")
        print("6. Statistics")
        print("7. Exit")
        print("\nChoice: ", end="")

    def get_categories(self) -> List[str]:
        """Get unique categories from questions"""
        categories = set(q.get('category', 'Uncategorized') for q in self.questions)
        return sorted(list(categories))

    def filter_questions(self, category=None, unanswered_only=False) -> List[Dict]:
        """Filter questions based on criteria"""
        filtered = self.questions

        if category:
            filtered = [q for q in filtered if q.get('category') == category]

        if unanswered_only:
            filtered = [q for q in filtered if not q.get('answered', False)]

        return filtered

    def practice_questions(self, questions_to_practice):
        """Practice a set of questions"""
        if not questions_to_practice:
            print("\nNo questions available to practice!")
            input("\nPress Enter to continue...")
            return

        total = len(questions_to_practice)
        for idx, question in enumerate(questions_to_practice, 1):
            self.clear_screen()
            print(f"\nQuestion {idx} of {total}")
            print("="*50)
            print(f"\nCategory: {question.get('category', 'N/A')}")
            print(f"\nQuestion: {question.get('question', 'N/A')}")

            if question.get('notes'):
                print(f"\nNotes: {question.get('notes')}")

            print("\n" + "-"*50)
            print("\nOptions:")
            print("  [Enter] - Next question")
            print("  [m]     - Mark as answered")
            print("  [s]     - Skip")
            print("  [q]     - Quit to main menu")

            choice = input("\nYour choice: ").lower().strip()

            if choice == 'q':
                break
            elif choice == 'm':
                # Find the original question and mark it
                for q in self.questions:
                    if q.get('id') == question.get('id'):
                        q['answered'] = True
                        break
                self.save_questions()
                print("\nMarked as answered!")
                input("Press Enter to continue...")
            elif choice == 's':
                continue
            else:
                continue

        print("\nPractice session completed!")
        input("\nPress Enter to continue...")

    def view_all_questions(self):
        """Display all questions"""
        self.clear_screen()
        print("\nAll Questions")
        print("="*50)

        for q in self.questions:
            status = "✓" if q.get('answered', False) else "○"
            print(f"\n[{status}] ID: {q.get('id')} | Category: {q.get('category', 'N/A')}")
            print(f"    Q: {q.get('question', 'N/A')}")

        input("\nPress Enter to continue...")

    def reset_progress(self):
        """Reset all answered flags"""
        confirm = input("\nAre you sure you want to reset all progress? (yes/no): ")
        if confirm.lower() == 'yes':
            for q in self.questions:
                q['answered'] = False
            self.save_questions()
            print("\nProgress reset successfully!")
        else:
            print("\nReset cancelled.")
        input("\nPress Enter to continue...")

    def show_statistics(self):
        """Show practice statistics"""
        self.clear_screen()
        total = len(self.questions)
        answered = sum(1 for q in self.questions if q.get('answered', False))
        unanswered = total - answered

        print("\nStatistics")
        print("="*50)
        print(f"\nTotal Questions: {total}")
        print(f"Answered: {answered}")
        print(f"Unanswered: {unanswered}")

        if total > 0:
            percentage = (answered / total) * 100
            print(f"Progress: {percentage:.1f}%")

        print("\nBy Category:")
        categories = self.get_categories()
        for cat in categories:
            cat_questions = [q for q in self.questions if q.get('category') == cat]
            cat_answered = sum(1 for q in cat_questions if q.get('answered', False))
            print(f"  {cat}: {cat_answered}/{len(cat_questions)}")

        input("\nPress Enter to continue...")

    def select_category(self):
        """Let user select a category"""
        categories = self.get_categories()

        if not categories:
            print("\nNo categories found!")
            input("\nPress Enter to continue...")
            return None

        print("\nSelect a category:")
        print("-"*50)
        for idx, cat in enumerate(categories, 1):
            count = len([q for q in self.questions if q.get('category') == cat])
            print(f"{idx}. {cat} ({count} questions)")

        try:
            choice = int(input("\nEnter category number: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1]
        except ValueError:
            pass

        print("\nInvalid choice!")
        input("\nPress Enter to continue...")
        return None

    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.display_menu()

            choice = input().strip()

            if choice == '1':
                self.practice_questions(self.questions)
            elif choice == '2':
                category = self.select_category()
                if category:
                    questions = self.filter_questions(category=category)
                    self.practice_questions(questions)
            elif choice == '3':
                questions = self.filter_questions(unanswered_only=True)
                self.practice_questions(questions)
            elif choice == '4':
                self.view_all_questions()
            elif choice == '5':
                self.reset_progress()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice!")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = InterviewApp()
    app.run()
