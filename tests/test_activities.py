"""
Test suite for the activities endpoint.
Tests the GET /activities endpoint functionality.
"""

import pytest


class TestGetActivitiesEndpoint:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that the endpoint returns all available activities.

        Arrange: Activities are set up in the fixture
        Act: Make a GET request to /activities
        Assert: Verify all activities are returned with correct structure
        """
        # Arrange
        expected_activity_count = 9
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Team", "Soccer Club", "Drama Club",
            "Art Club", "Debate Club", "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        returned_activities = response.json()
        assert len(returned_activities) == expected_activity_count
        assert set(returned_activities.keys()) == set(expected_activities)

    def test_get_activities_includes_required_fields(self, client):
        """
        Test that each activity has all required fields.

        Arrange: Activities are set up in the fixture
        Act: Make a GET request to /activities
        Assert: Verify required fields are present in each activity
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        returned_activities = response.json()

        # Assert
        for activity_name, activity_data in returned_activities.items():
            for field in required_fields:
                assert field in activity_data, f"Field '{field}' missing from {activity_name}"

    def test_get_activities_participants_are_lists(self, client):
        """
        Test that participants field is always a list.

        Arrange: Activities are set up in the fixture
        Act: Make a GET request to /activities
        Assert: Verify participants field is a list for all activities
        """
        # Act
        response = client.get("/activities")
        returned_activities = response.json()

        # Assert
        for activity_name, activity_data in returned_activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants for {activity_name} is not a list"

    def test_get_activities_max_participants_are_positive_integers(self, client):
        """
        Test that max_participants are positive integers.

        Arrange: Activities are set up in the fixture
        Act: Make a GET request to /activities
        Assert: Verify max_participants are positive integers
        """
        # Act
        response = client.get("/activities")
        returned_activities = response.json()

        # Assert
        for activity_name, activity_data in returned_activities.items():
            max_participants = activity_data["max_participants"]
            assert isinstance(max_participants, int), \
                f"max_participants for {activity_name} is not an integer"
            assert max_participants > 0, \
                f"max_participants for {activity_name} is not positive"

    def test_get_activities_descriptions_are_non_empty_strings(self, client):
        """
        Test that descriptions are non-empty strings.

        Arrange: Activities are set up in the fixture
        Act: Make a GET request to /activities
        Assert: Verify descriptions are non-empty strings
        """
        # Act
        response = client.get("/activities")
        returned_activities = response.json()

        # Assert
        for activity_name, activity_data in returned_activities.items():
            description = activity_data["description"]
            assert isinstance(description, str), \
                f"Description for {activity_name} is not a string"
            assert len(description.strip()) > 0, \
                f"Description for {activity_name} is empty"

    def test_get_activities_schedules_are_non_empty_strings(self, client):
        """
        Test that schedules are non-empty strings.

        Arrange: Activities are set up in the fixture
        Act: Make a GET request to /activities
        Assert: Verify schedules are non-empty strings
        """
        # Act
        response = client.get("/activities")
        returned_activities = response.json()

        # Assert
        for activity_name, activity_data in returned_activities.items():
            schedule = activity_data["schedule"]
            assert isinstance(schedule, str), \
                f"Schedule for {activity_name} is not a string"
            assert len(schedule.strip()) > 0, \
                f"Schedule for {activity_name} is empty"

    def test_get_activities_returns_consistent_data(self, client):
        """
        Test that multiple calls return the same data.

        Arrange: Activities are set up in the fixture
        Act: Make multiple GET requests to /activities
        Assert: Verify responses are identical
        """
        # Act
        response1 = client.get("/activities")
        response2 = client.get("/activities")

        # Assert
        assert response1.status_code == response2.status_code == 200
        assert response1.json() == response2.json()