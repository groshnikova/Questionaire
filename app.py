#!/usr/bin/env python3
"""
Interview Questions Practice App - Web Version
A Flask-based web application for practicing interview questions
"""

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

QUESTIONS_FILE = 'questions.json'
PROGRESS_FILE = 'progress.json'

def load_questions():
    """Load questions from JSON file"""
    if not os.path.exists(QUESTIONS_FILE):
        return []

    try:
        with open(QUESTIONS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('questions', [])
    except json.JSONDecodeError:
        return []

def save_questions(questions):
    """Save questions to JSON file"""
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump({'questions': questions}, f, indent=2)

def load_progress():
    """Load progress from separate progress file"""
    if not os.path.exists(PROGRESS_FILE):
        return {}

    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_progress(progress):
    """Save progress to separate progress file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def merge_questions_with_progress(questions):
    """Merge questions with progress data"""
    progress = load_progress()
    for q in questions:
        q_id = str(q.get('id'))
        q['answered'] = progress.get(q_id, False)
    return questions

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions"""
    questions = load_questions()
    questions = merge_questions_with_progress(questions)

    # Get filter parameters
    category = request.args.get('category')
    unanswered_only = request.args.get('unanswered') == 'true'

    # Apply filters
    if category and category != 'all':
        questions = [q for q in questions if q.get('category') == category]

    if unanswered_only:
        questions = [q for q in questions if not q.get('answered', False)]

    return jsonify(questions)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get unique categories"""
    questions = load_questions()
    categories = sorted(list(set(q.get('category', 'Uncategorized') for q in questions)))
    return jsonify(categories)

@app.route('/api/questions/<int:question_id>/toggle', methods=['POST'])
def toggle_answered(question_id):
    """Toggle answered status for a question"""
    progress = load_progress()
    q_id = str(question_id)

    # Toggle the answered status in progress file
    progress[q_id] = not progress.get(q_id, False)
    save_progress(progress)

    return jsonify({'success': True, 'answered': progress[q_id]})

@app.route('/api/questions', methods=['POST'])
def add_question():
    """Add a new question"""
    data = request.json
    questions = load_questions()

    # Generate new ID
    new_id = max([q.get('id', 0) for q in questions], default=0) + 1

    new_question = {
        'id': new_id,
        'category': data.get('category', 'Uncategorized'),
        'question': data.get('question', ''),
        'hint': data.get('hint', '')
    }

    questions.append(new_question)
    save_questions(questions)

    return jsonify({'success': True, 'question': new_question})

@app.route('/api/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """Update an existing question"""
    data = request.json
    questions = load_questions()

    for q in questions:
        if q.get('id') == question_id:
            q['category'] = data.get('category', q.get('category'))
            q['question'] = data.get('question', q.get('question'))
            q['hint'] = data.get('hint', q.get('hint', ''))
            save_questions(questions)
            return jsonify({'success': True, 'question': q})

    return jsonify({'success': False, 'error': 'Question not found'}), 404

@app.route('/api/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Delete a question"""
    questions = load_questions()
    questions = [q for q in questions if q.get('id') != question_id]
    save_questions(questions)

    # Also remove from progress
    progress = load_progress()
    if str(question_id) in progress:
        del progress[str(question_id)]
        save_progress(progress)

    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    questions = load_questions()
    questions = merge_questions_with_progress(questions)

    total = len(questions)
    answered = sum(1 for q in questions if q.get('answered', False))

    # Stats by category
    categories = {}
    for q in questions:
        cat = q.get('category', 'Uncategorized')
        if cat not in categories:
            categories[cat] = {'total': 0, 'answered': 0}
        categories[cat]['total'] += 1
        if q.get('answered', False):
            categories[cat]['answered'] += 1

    return jsonify({
        'total': total,
        'answered': answered,
        'unanswered': total - answered,
        'percentage': round((answered / total * 100) if total > 0 else 0, 1),
        'categories': categories
    })

@app.route('/api/reset', methods=['POST'])
def reset_progress():
    """Reset all answered flags"""
    # Clear the progress file
    save_progress({})
    return jsonify({'success': True})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Interview Questions Practice App")
    print("="*60)
    print("\nStarting server at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
