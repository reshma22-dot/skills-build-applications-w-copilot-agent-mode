from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

class TeamModelTest(TestCase):
    def test_create_team(self):
        user = User.objects.create(username="teamuser", email="teamuser@example.com", password="password123")
        team = Team.objects.create(name="Test Team")
        team.members.add(user)
        self.assertEqual(team.name, "Test Team")
        self.assertIn(user, team.members.all())

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create(username="activityuser", email="activityuser@example.com", password="password123")
        activity = Activity.objects.create(user=user, activity_type="Running", duration=timedelta(minutes=30))
        self.assertEqual(activity.activity_type, "Running")
        self.assertEqual(activity.duration, timedelta(minutes=30))

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard_entry(self):
        user = User.objects.create(username="leaderuser", email="leaderuser@example.com", password="password123")
        leaderboard = Leaderboard.objects.create(user=user, score=100)
        self.assertEqual(leaderboard.score, 100)

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name="Test Workout", description="A test workout description.")
        self.assertEqual(workout.name, "Test Workout")
        self.assertEqual(workout.description, "A test workout description.")

class OctoFitTrackerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="testuser@example.com", password="password123")
        self.team = Team.objects.create(name="Test Team")
        self.team.members.add(self.user)
        self.activity = Activity.objects.create(user=self.user, activity_type="Running", duration="01:00:00")
        self.leaderboard = Leaderboard.objects.create(user=self.user, score=100)
        self.workout = Workout.objects.create(name="Test Workout", description="Test workout description")

    def test_user_creation(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_creation(self):
        response = self.client.get("/api/teams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_creation(self):
        response = self.client.get("/api/activities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leaderboard_creation(self):
        response = self.client.get("/api/leaderboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_workout_creation(self):
        response = self.client.get("/api/workouts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
