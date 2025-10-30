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

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions"""
    questions = load_questions()

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
    questions = load_questions()

    for q in questions:
        if q.get('id') == question_id:
            q['answered'] = not q.get('answered', False)
            save_questions(questions)
            return jsonify({'success': True, 'answered': q['answered']})

    return jsonify({'success': False, 'error': 'Question not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    questions = load_questions()
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
    questions = load_questions()

    for q in questions:
        q['answered'] = False

    save_questions(questions)
    return jsonify({'success': True})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Interview Questions Practice App")
    print("="*60)
    print("\nStarting server at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
