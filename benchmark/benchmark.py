'''
pip install locust --break-system-packages
'''
from locust import HttpUser, task, between

class FaceIDUser(HttpUser):

    # @task
    # def login(self):
    #     with open("mock/st_check.png", "rb") as image_file:
    #         self.client.post("/login", params={"user_id": 'st'}, headers={"accept": "application/json"}, files={"file": ("st_check.png", image_file, "image/png")})
    @task
    def login(self):
        self.client.post("/login-test")

if __name__ == "__main__":
    import os
    os.system("locust -f benchmark.py --host=http://localhost:8000 --users=1000 --spawn-rate=1000")
