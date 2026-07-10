"""Personalized learning recommendation engine"""

import logging
from .utils import get_performance_level

logger = logging.getLogger(__name__)

class PersonalizedLearning:
    """Generates personalized learning recommendations"""
    
    def __init__(self):
        self.learning_resources = {
            'Math': ['Khan Academy', 'PatrickJMT', 'Paul\'s Online Math Notes', 'Brilliant.org'],
            'Science': ['Crash Course', 'TED-Ed', 'Amoeba Sisters', 'Professor Dave Explains'],
            'English': ['Grammarly', 'Hemingway App', 'TED Talks', 'Literature Online'],
            'History': ['Crash Course History', 'TED Talks', 'Documentaries', 'Historical Societies'],
            'Programming': ['Codecademy', 'Coursera', 'DataCamp', 'freeCodeCamp']
        }
    
    def get_recommendations(self, student_data):
        """Generate personalized learning recommendations"""
        recommendations = {
            'study_schedule': self._generate_study_schedule(student_data),
            'learning_resources': self._recommend_resources(student_data),
            'focus_areas': self._identify_focus_areas(student_data),
            'study_techniques': self._recommend_study_techniques(student_data),
            'peer_support': self._recommend_peer_support(student_data),
            'motivation': self._generate_motivation(student_data)
        }
        
        logger.info(f"Recommendations generated for student")
        return recommendations
    
    def _generate_study_schedule(self, student_data):
        """Generate personalized study schedule"""
        study_hours = student_data.get('study_hours', 0)
        engagement = student_data.get('engagement_level', 3)
        
        if study_hours < 3:
            return {
                'recommendation': 'Increase study time',
                'suggested_hours_per_week': 15,
                'daily_goal': '2-3 hours',
                'best_time': 'Early morning or evening'
            }
        elif study_hours < 5:
            return {
                'recommendation': 'Moderate study schedule',
                'suggested_hours_per_week': 20,
                'daily_goal': '3-4 hours',
                'best_time': 'Mix of morning and evening sessions'
            }
        else:
            return {
                'recommendation': 'Optimize study quality over quantity',
                'suggested_hours_per_week': 15,
                'daily_goal': '2-3 focused hours',
                'best_time': 'Peak alertness hours'
            }
    
    def _recommend_resources(self, student_data):
        """Recommend learning resources"""
        subject = student_data.get('subject', 'Math')
        performance = student_data.get('performance_level', 'Good')
        
        resources = []
        if subject in self.learning_resources:
            resources = self.learning_resources[subject]
        
        if performance == 'At Risk':
            resources.insert(0, 'Personalized Tutor')
            resources.append('YouTube Tutorials')
        elif performance == 'Excellent':
            resources.append('Advanced Courses')
            resources.append('Online Competitions')
        
        return resources
    
    def _identify_focus_areas(self, student_data):
        """Identify areas that need focus"""
        assignment_score = student_data.get('assignment_score', 75)
        attendance = student_data.get('attendance', 80)
        engagement = student_data.get('engagement_level', 3)
        
        focus_areas = []
        
        if assignment_score < 70:
            focus_areas.append('Improve assignment completion and quality')
        
        if attendance < 85:
            focus_areas.append('Increase class attendance')
        
        if engagement < 3:
            focus_areas.append('Increase classroom participation and engagement')
        
        if not focus_areas:
            focus_areas.append('Maintain current performance and explore advanced topics')
        
        return focus_areas
    
    def _recommend_study_techniques(self, student_data):
        """Recommend effective study techniques"""
        engagement = student_data.get('engagement_level', 3)
        study_hours = student_data.get('study_hours', 0)
        
        techniques = []
        
        if engagement < 2:
            techniques.extend([
                'Pomodoro Technique (25 min study + 5 min break)',
                'Active recall and spaced repetition',
                'Study groups for accountability'
            ])
        elif engagement < 4:
            techniques.extend([
                'Feynman Technique (explain concepts in simple terms)',
                'Mind mapping for complex topics',
                'Practice problems and self-testing'
            ])
        else:
            techniques.extend([
                'Teach others to deepen understanding',
                'Connect new concepts to existing knowledge',
                'Research and explore beyond curriculum'
            ])
        
        return techniques
    
    def _recommend_peer_support(self, student_data):
        """Recommend peer support options"""
        return {
            'study_groups': 'Join or form study groups with classmates',
            'peer_tutoring': 'Find peer tutors for challenging subjects',
            'discussion_forums': 'Participate in online forums and discussions',
            'group_projects': 'Collaborate on group projects'
        }
    
    def _generate_motivation(self, student_data):
        """Generate personalized motivation message"""
        performance = student_data.get('performance_level', 'Good')
        
        messages = {
            'Excellent': 'You\'re doing amazing! Keep pushing your boundaries and help others too!',
            'Very Good': 'Great work! You\'re on the right track. Keep the momentum going!',
            'Good': 'You\'re doing well! Small improvements can lead to great results.',
            'Satisfactory': 'You have potential! Focus on your weaknesses and seek help when needed.',
            'Needs Improvement': 'It\'s time to turn things around. Get help and stay committed!',
            'At Risk': 'You need urgent support. Reach out to advisors and tutors today!'
        }
        
        return messages.get(performance, 'Keep working hard and believe in yourself!')
