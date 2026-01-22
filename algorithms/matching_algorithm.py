"""
Student Similarity Matching Algorithm

This module implements the core matching algorithm that calculates
compatibility scores between students based on multiple factors.
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, time


class StudentMatcher:
    """
    Calculates similarity scores between students for study partner matching.

    Uses weighted multi-factor analysis including:
    - Learning pace compatibility
    - Schedule overlap
    - Interest similarity
    - Goal alignment
    - Learning style matching
    - Past collaboration success
    """

    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize matcher with feature weights.

        Args:
            weights: Dictionary of feature weights. If None, uses default weights.
        """
        self.weights = weights or {
            'learning_pace': 0.20,
            'schedule_overlap': 0.25,
            'interest_similarity': 0.20,
            'goal_alignment': 0.15,
            'learning_style': 0.10,
            'past_success': 0.10
        }

        # Normalize weights to sum to 1.0
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}

    def calculate_similarity(self, student1: Dict, student2: Dict) -> float:
        """
        Calculate overall similarity score between two students.

        Args:
            student1: First student profile dictionary
            student2: Second student profile dictionary

        Returns:
            Similarity score from 0-100
        """
        # Calculate individual feature similarities
        pace_sim = self._calculate_pace_similarity(
            student1.get('learning_pace'),
            student2.get('learning_pace')
        )

        schedule_sim = self._calculate_schedule_overlap(
            student1.get('study_schedule', {}),
            student2.get('study_schedule', {})
        )

        interest_sim = self._calculate_interest_similarity(
            student1.get('subjects_of_interest', []),
            student2.get('subjects_of_interest', [])
        )

        goal_sim = self._calculate_goal_alignment(
            student1.get('study_goals', []),
            student2.get('study_goals', [])
        )

        style_sim = self._calculate_learning_style_similarity(
            student1.get('learning_style', []),
            student2.get('learning_style', [])
        )

        # Calculate weighted score
        total_score = (
            self.weights['learning_pace'] * pace_sim +
            self.weights['schedule_overlap'] * schedule_sim +
            self.weights['interest_similarity'] * interest_sim +
            self.weights['goal_alignment'] * goal_sim +
            self.weights['learning_style'] * style_sim
        )

        # Apply penalties
        total_score = self._apply_penalties(total_score, student1, student2, schedule_sim)

        # Incorporate past collaboration feedback if available
        past_success = self._get_past_collaboration_score(
            student1.get('id'),
            student2.get('id')
        )

        if past_success is not None:
            total_score = 0.7 * total_score + 0.3 * past_success

        # Normalize to 0-100 scale
        return min(100, max(0, total_score * 100))

    def _calculate_pace_similarity(self, pace1: str, pace2: str) -> float:
        """
        Calculate learning pace compatibility.

        Args:
            pace1: Learning pace of student 1 (fast/moderate/slow)
            pace2: Learning pace of student 2 (fast/moderate/slow)

        Returns:
            Similarity score from 0-1
        """
        pace_map = {'slow': 1, 'moderate': 2, 'fast': 3}

        if not pace1 or not pace2:
            return 0.5  # Neutral if missing

        p1 = pace_map.get(pace1.lower(), 2)
        p2 = pace_map.get(pace2.lower(), 2)

        # Perfect match = 1.0, adjacent = 0.7, opposite = 0.3
        diff = abs(p1 - p2)
        if diff == 0:
            return 1.0
        elif diff == 1:
            return 0.7
        else:
            return 0.3

    def _calculate_schedule_overlap(self, schedule1: Dict, schedule2: Dict) -> float:
        """
        Calculate percentage of overlapping study time availability.

        Args:
            schedule1: Study schedule of student 1
            schedule2: Study schedule of student 2

        Returns:
            Overlap percentage from 0-1
        """
        if not schedule1 or not schedule2:
            return 0.5  # Neutral if missing

        total_overlap_minutes = 0
        total_possible_minutes = 0

        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

        for day in days:
            slots1 = schedule1.get(day, [])
            slots2 = schedule2.get(day, [])

            if not slots1 or not slots2:
                continue

            # Convert to minute ranges
            ranges1 = [self._time_range_to_minutes(slot) for slot in slots1]
            ranges2 = [self._time_range_to_minutes(slot) for slot in slots2]

            # Calculate overlap
            for r1_start, r1_end in ranges1:
                for r2_start, r2_end in ranges2:
                    overlap_start = max(r1_start, r2_start)
                    overlap_end = min(r1_end, r2_end)

                    if overlap_start < overlap_end:
                        total_overlap_minutes += (overlap_end - overlap_start)

                total_possible_minutes += (r1_end - r1_start)

        if total_possible_minutes == 0:
            return 0.5

        overlap_ratio = total_overlap_minutes / total_possible_minutes
        return min(1.0, overlap_ratio)

    def _time_range_to_minutes(self, slot: Dict) -> Tuple[int, int]:
        """Convert time slot to minutes from midnight."""
        start = slot.get('start', '00:00')
        end = slot.get('end', '00:00')

        start_minutes = self._time_str_to_minutes(start)
        end_minutes = self._time_str_to_minutes(end)

        return start_minutes, end_minutes

    def _time_str_to_minutes(self, time_str: str) -> int:
        """Convert time string (HH:MM) to minutes from midnight."""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except:
            return 0

    def _calculate_interest_similarity(self, interests1: List[str], interests2: List[str]) -> float:
        """
        Calculate cosine similarity of subject interests.

        Args:
            interests1: List of subjects for student 1
            interests2: List of subjects for student 2

        Returns:
            Similarity score from 0-1
        """
        if not interests1 or not interests2:
            return 0.3  # Low score if missing

        # Convert to sets for easier comparison
        set1 = set([i.lower() for i in interests1])
        set2 = set([i.lower() for i in interests2])

        # Jaccard similarity
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    def _calculate_goal_alignment(self, goals1: List[Dict], goals2: List[Dict]) -> float:
        """
        Calculate alignment of study goals.

        Args:
            goals1: Study goals of student 1
            goals2: Study goals of student 2

        Returns:
            Alignment score from 0-1
        """
        if not goals1 or not goals2:
            return 0.4  # Neutral-low if missing

        # Extract subjects from goals
        subjects1 = set([g.get('subject', '').lower() for g in goals1])
        subjects2 = set([g.get('subject', '').lower() for g in goals2])

        # Calculate overlap
        intersection = len(subjects1 & subjects2)
        union = len(subjects1 | subjects2)

        if union == 0:
            return 0.0

        base_score = intersection / union

        # Bonus for matching target grades/priorities
        matching_priorities = 0
        total_comparisons = 0

        for g1 in goals1:
            for g2 in goals2:
                if g1.get('subject', '').lower() == g2.get('subject', '').lower():
                    total_comparisons += 1
                    if g1.get('priority') == g2.get('priority'):
                        matching_priorities += 1

        if total_comparisons > 0:
            priority_bonus = (matching_priorities / total_comparisons) * 0.2
            base_score = min(1.0, base_score + priority_bonus)

        return base_score

    def _calculate_learning_style_similarity(self, styles1: List[str], styles2: List[str]) -> float:
        """
        Calculate learning style compatibility (Jaccard similarity).

        Args:
            styles1: Learning styles of student 1
            styles2: Learning styles of student 2

        Returns:
            Similarity score from 0-1
        """
        if not styles1 or not styles2:
            return 0.5  # Neutral if missing

        set1 = set([s.lower() for s in styles1])
        set2 = set([s.lower() for s in styles2])

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.5

        return intersection / union

    def _apply_penalties(self, score: float, student1: Dict, student2: Dict, schedule_overlap: float) -> float:
        """
        Apply penalties for incompatibilities.

        Args:
            score: Current similarity score
            student1: First student profile
            student2: Second student profile
            schedule_overlap: Schedule overlap score

        Returns:
            Adjusted score
        """
        # Severe schedule conflict penalty
        if schedule_overlap < 0.3:
            score *= 0.5

        # Opposite learning paces penalty
        pace1 = student1.get('learning_pace', '').lower()
        pace2 = student2.get('learning_pace', '').lower()
        if (pace1 == 'fast' and pace2 == 'slow') or (pace1 == 'slow' and pace2 == 'fast'):
            score *= 0.7

        # Different institutions penalty (if applicable)
        if student1.get('institution') != student2.get('institution'):
            score *= 0.9

        return score

    def _get_past_collaboration_score(self, user_id1: str, user_id2: str) -> float:
        """
        Retrieve past collaboration success score from database.

        Args:
            user_id1: First user ID
            user_id2: Second user ID

        Returns:
            Past success score from 0-1, or None if no past collaboration
        """
        # TODO: Implement database lookup
        # This would query the study_sessions collection for past collaborations
        # and calculate average effectiveness ratings
        return None

    def find_top_matches(self, target_student: Dict, candidate_students: List[Dict], top_n: int = 10) -> List[Tuple[Dict, float]]:
        """
        Find top N matching students for a target student.

        Args:
            target_student: Target student profile
            candidate_students: List of candidate student profiles
            top_n: Number of top matches to return

        Returns:
            List of (student, score) tuples, sorted by score descending
        """
        matches = []

        for candidate in candidate_students:
            # Skip self-match
            if candidate.get('id') == target_student.get('id'):
                continue

            score = self.calculate_similarity(target_student, candidate)
            matches.append((candidate, score))

        # Sort by score descending and return top N
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]


# Example usage
if __name__ == "__main__":
    # Sample student profiles
    student_a = {
        'id': 'user_1',
        'learning_pace': 'moderate',
        'study_schedule': {
            'monday': [{'start': '14:00', 'end': '17:00'}],
            'wednesday': [{'start': '14:00', 'end': '17:00'}],
        },
        'subjects_of_interest': ['Machine Learning', 'Algorithms', 'Python'],
        'study_goals': [
            {'subject': 'Machine Learning', 'target_grade': 'A', 'priority': 'high'}
        ],
        'learning_style': ['visual', 'kinesthetic'],
        'institution': 'MIT'
    }

    student_b = {
        'id': 'user_2',
        'learning_pace': 'moderate',
        'study_schedule': {
            'monday': [{'start': '15:00', 'end': '18:00'}],
            'wednesday': [{'start': '13:00', 'end': '16:00'}],
        },
        'subjects_of_interest': ['Machine Learning', 'Data Science', 'Statistics'],
        'study_goals': [
            {'subject': 'Machine Learning', 'target_grade': 'A', 'priority': 'high'}
        ],
        'learning_style': ['visual', 'auditory'],
        'institution': 'MIT'
    }

    matcher = StudentMatcher()
    similarity = matcher.calculate_similarity(student_a, student_b)

    print(f"Similarity Score: {similarity:.2f}/100")
    print(f"Match Quality: {'Excellent' if similarity >= 80 else 'Good' if similarity >= 60 else 'Fair' if similarity >= 40 else 'Poor'}")
