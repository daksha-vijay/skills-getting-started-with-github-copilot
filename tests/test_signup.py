"""
Test suite for user signup functionality.
Tests the POST /activities/{activity_name}/signup endpoint.
"""

import pytest
from src.app import activities


class TestSignupForActivityEndpoint:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successfully_adds_student_to_activity(self, client):
        """
        Test that a student can successfully sign up for an activity.

        Arrange: An empty activity (Basketball Team) is selected
        Act: Make a POST request with a student email
        Assert: Verify the student is added and response is correct
        """
        # Arrange
        activity_name = "Basketball Team"
        student_email = "alex@mergington.edu"
        expected_status_code = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert student_email in activities[activity_name]["participants"]
        assert "Signed up" in response.json()["message"]

    def test_signup_fails_when_activity_not_found(self, client):
        """
        Test that signup fails with appropriate error when activity doesn't exist.

        Arrange: A non-existent activity name
        Act: Make a POST request to signup for that activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        non_existent_activity = "Invisible Club"
        student_email = "alex@mergington.edu"
        expected_status_code = 404
        expected_detail = "Activity not found"

        # Act
        response = client.post(
            f"/activities/{non_existent_activity}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert response.json()["detail"] == expected_detail

    def test_signup_fails_when_student_already_enrolled(self, client):
        """
        Test that signup fails when student is already enrolled in activity.

        Arrange: A student already enrolled in Chess Club
        Act: Attempt to sign up the same student again
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        already_enrolled_student = "michael@mergington.edu"  # Already in Chess Club
        expected_status_code = 400
        expected_detail = "Student already signed up for this activity"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": already_enrolled_student}
        )

        # Assert
        assert response.status_code == expected_status_code
        assert response.json()["detail"] == expected_detail

    def test_signup_allows_multiple_students_same_activity(self, client):
        """
        Test that multiple different students can sign up for the same activity.

        Arrange: An empty activity and multiple student emails
        Act: Sign up multiple students for the activity
        Assert: Verify all students are added
        """
        # Arrange
        activity_name = "Soccer Club"
        student_emails = ["player1@mergington.edu", "player2@mergington.edu", "player3@mergington.edu"]

        # Act
        for email in student_emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        for email in student_emails:
            assert email in activities[activity_name]["participants"]

    def test_signup_allows_same_student_multiple_activities(self, client):
        """
        Test that the same student can sign up for multiple activities.

        Arrange: Multiple activities and one student email
        Act: Sign up the student for multiple activities
        Assert: Verify student is in all activities
        """
        # Arrange
        activity_names = ["Art Club", "Debate Club", "Science Club"]
        student_email = "versatile@mergington.edu"

        # Act
        for activity_name in activity_names:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": student_email}
            )
            assert response.status_code == 200

        # Assert
        for activity_name in activity_names:
            assert student_email in activities[activity_name]["participants"]

    def test_signup_preserves_existing_participants(self, client):
        """
        Test that signing up a new student preserves existing participants.

        Arrange: An activity with existing participants
        Act: Sign up a new student
        Assert: Verify existing participants are still there
        """
        # Arrange
        activity_name = "Programming Class"
        new_student_email = "newstudent@mergington.edu"
        existing_participants = activities[activity_name]["participants"].copy()

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student_email}
        )

        # Assert
        assert response.status_code == 200
        current_participants = activities[activity_name]["participants"]
        for existing_email in existing_participants:
            assert existing_email in current_participants
        assert new_student_email in current_participants
        assert len(current_participants) == len(existing_participants) + 1

    def test_signup_response_includes_activity_and_email(self, client):
        """
        Test that signup response message includes activity name and email.

        Arrange: An activity and student email
        Act: Sign up the student
        Assert: Verify response message contains both activity and email
        """
        # Arrange
        activity_name = "Drama Club"
        student_email = "actor@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert activity_name in message
        assert student_email in message
        assert "Signed up" in message