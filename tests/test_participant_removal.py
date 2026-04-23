"""
Test suite for participant removal functionality.
Tests the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest
from src.app import activities


class TestRemoveParticipantEndpoint:
    """Test suite for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_successfully_removes_student(self, client):
        """
        Test that a student can be successfully removed from an activity.

        Arrange: A student enrolled in Programming Class is selected
        Act: Make a DELETE request with the student email
        Assert: Verify the student is removed and response is correct
        """
        # Arrange
        activity_name = "Programming Class"
        student_email = "emma@mergington.edu"  # Already in Programming Class
        initial_count = len(activities[activity_name]["participants"])
        expected_status_code = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{student_email}"
        )

        # Assert
        assert response.status_code == expected_status_code
        assert student_email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1
        assert "Removed" in response.json()["message"]

    def test_remove_participant_fails_when_activity_not_found(self, client):
        """
        Test that removal fails with appropriate error when activity doesn't exist.

        Arrange: A non-existent activity name
        Act: Make a DELETE request to remove from that activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        non_existent_activity = "Invisible Club"
        student_email = "alex@mergington.edu"
        expected_status_code = 404
        expected_detail = "Activity not found"

        # Act
        response = client.delete(
            f"/activities/{non_existent_activity}/participants/{student_email}"
        )

        # Assert
        assert response.status_code == expected_status_code
        assert response.json()["detail"] == expected_detail

    def test_remove_participant_fails_when_student_not_enrolled(self, client):
        """
        Test that removal fails when student is not enrolled in the activity.

        Arrange: An empty activity and a student email
        Act: Attempt to remove the student from the activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Basketball Team"  # Empty activity
        student_email = "notenrolled@mergington.edu"
        expected_status_code = 404
        expected_detail = "Student not signed up for this activity"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{student_email}"
        )

        # Assert
        assert response.status_code == expected_status_code
        assert response.json()["detail"] == expected_detail

    def test_remove_participant_preserves_other_participants(self, client):
        """
        Test that removing one participant preserves others in the activity.

        Arrange: An activity with multiple participants
        Act: Remove one participant
        Assert: Verify other participants remain
        """
        # Arrange
        activity_name = "Gym Class"
        student_to_remove = "john@mergington.edu"
        student_to_keep = "olivia@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{student_to_remove}"
        )

        # Assert
        assert response.status_code == 200
        assert student_to_remove not in activities[activity_name]["participants"]
        assert student_to_keep in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_remove_participant_response_includes_activity_and_email(self, client):
        """
        Test that removal response message includes activity name and email.

        Arrange: An activity and enrolled student
        Act: Remove the student
        Assert: Verify response message contains both activity and email
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{student_email}"
        )

        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert activity_name in message
        assert student_email in message
        assert "Removed" in message

    def test_remove_participant_allows_resignup(self, client):
        """
        Test that a removed participant can sign up again.

        Arrange: Remove a student from an activity
        Act: Sign up the same student again
        Assert: Verify signup succeeds
        """
        # Arrange
        activity_name = "Programming Class"
        student_email = "sophia@mergington.edu"

        # Act: Remove student
        response = client.delete(
            f"/activities/{activity_name}/participants/{student_email}"
        )
        assert response.status_code == 200

        # Act: Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        assert student_email in activities[activity_name]["participants"]

    def test_remove_multiple_participants_sequentially(self, client):
        """
        Test removing multiple participants one by one.

        Arrange: An activity with multiple participants
        Act: Remove participants sequentially
        Assert: Verify all are removed
        """
        # Arrange
        activity_name = "Gym Class"
        students_to_remove = ["john@mergington.edu", "olivia@mergington.edu"]

        # Act
        for email in students_to_remove:
            response = client.delete(
                f"/activities/{activity_name}/participants/{email}"
            )
            assert response.status_code == 200

        # Assert
        for email in students_to_remove:
            assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == 0