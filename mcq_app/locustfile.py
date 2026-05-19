import random
from locust import HttpUser, task, between

class StudentAssessmentUser(HttpUser):
    # Simulate a student waiting between 1 to 5 seconds between actions
    wait_time = between(1, 5)

    @task
    def submit_assessment(self):
        # 1. Simulate the student's unique ID
        student_id = f"STU_{random.randint(1000, 9999)}"
        
        # 2. Mock the form data matching your views.py structure
        # Assuming you have question IDs 1 through 20 in your database
        payload = {
            'user_id': student_id,
        }
        
        for q_id in range(1, 3):
            payload[f'question_{q_id}'] = random.choice(['choice_a', 'choice_b', 'choice_c', 'choice_d'])
        
        # 3. Send the POST request to your Django view URL
        # Replace '/mcq/' with the actual path to your mcq_list view
        headers = {'X-CSRFToken': 'mocked-token-if-csrf-exempt'} 
        self.client.post("/", data=payload, headers=headers)