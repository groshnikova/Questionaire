# Interview Questions Practice App

A simple, interactive CLI application to help you practice interview questions. Track your progress, organize questions by category, and prepare for your next interview.

## Features

- Practice interview questions interactively
- Organize questions by categories
- Track which questions you've answered
- View statistics on your progress
- Easy-to-edit JSON format for adding questions

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd Questionaire
```

2. Make the app executable (optional):
```bash
chmod +x interview_app.py
```

## Usage

### Running the App

```bash
python3 interview_app.py
```

Or if you made it executable:
```bash
./interview_app.py
```

### Menu Options

1. **Practice all questions** - Go through all questions in your list
2. **Practice by category** - Filter questions by a specific category
3. **Practice unanswered questions** - Only show questions you haven't marked as answered
4. **View all questions** - See a list of all questions with their status
5. **Reset progress** - Clear all "answered" flags to start fresh
6. **Statistics** - View your progress and breakdown by category
7. **Exit** - Close the application

### During Practice

While practicing questions, you have these options:
- **[Enter]** - Move to the next question
- **[m]** - Mark the current question as answered
- **[s]** - Skip the current question
- **[q]** - Quit back to the main menu

## Adding Your Own Questions

Edit the `questions.json` file to add your interview questions. Each question should follow this format:

```json
{
  "id": 1,
  "category": "Behavioral",
  "question": "Tell me about a time you faced a conflict at work.",
  "notes": "Use the STAR method",
  "answered": false
}
```

### Fields:

- **id**: Unique identifier (number)
- **category**: Category name (string) - organize your questions
- **question**: The actual question text (string)
- **notes**: Optional hints or reminders (string)
- **answered**: Progress tracking (boolean) - automatically updated by the app

### Example questions.json:

```json
{
  "questions": [
    {
      "id": 1,
      "category": "Technical",
      "question": "Explain the difference between REST and GraphQL.",
      "notes": "Focus on advantages and use cases",
      "answered": false
    },
    {
      "id": 2,
      "category": "Behavioral",
      "question": "Describe a time you had to learn a new technology quickly.",
      "notes": "Mention the outcome and what you learned",
      "answered": false
    },
    {
      "id": 3,
      "category": "System Design",
      "question": "How would you design a URL shortening service?",
      "notes": "Consider scalability, database choice, and API design",
      "answered": false
    }
  ]
}
```

## Tips

1. **Organize by Interview Type**: Create categories like "Technical", "Behavioral", "System Design", "Company-Specific", etc.
2. **Add Notes**: Use the notes field for reminders about frameworks (like STAR method) or key points to mention
3. **Regular Practice**: Use "Practice unanswered questions" to focus on questions you haven't covered recently
4. **Track Progress**: Check your statistics regularly to ensure balanced coverage across all categories

## File Structure

```
Questionaire/
├── interview_app.py    # Main application
├── questions.json      # Your interview questions
└── README.md          # This file
```

## Customization

The app is designed to be simple and easy to modify. Here are some ideas:

- Add a "difficulty" field to questions
- Include sample answers in the JSON
- Add timing functionality to simulate real interview conditions
- Export practice session logs

## License

Free to use and modify as needed.

## Contributing

Feel free to enhance this app for your needs. Some ideas for improvements:
- Web interface
- Flashcard mode
- Speech-to-text for practicing answers out loud
- Export/import functionality
- Multiple question sets
