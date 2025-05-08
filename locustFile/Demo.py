from locust import HttpUser, task, between

class DummyJSONUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://dummyjson.com"

    def on_start(self):
        login_response = self.client.post(
            "/auth/login",
            json={"username": "emilys", "password": "emilyspass"},
            name="POST login"
        )

        print("login response:", login_response.text)

        if login_response.status_code == 200:
            try:
                #يقرأ التوكن ويحول الرد الى json
                login_data = login_response.json()
                print("login JSON:", login_data)

                #يحفظ التوكن في المتغير
                self.token = login_data.get("accessToken")  # التعديل هنا
                print("Token received:", self.token)

                print("Logged in as:", login_data.get("firstName"), login_data.get("lastName"))

            except Exception as e:
                print("Error parsing login response:", str(e))
                self.token = None
        else:
            print("Login Failed with status:", login_response.status_code)
            print("Response Text:", login_response.text)
            self.token = None

    @task
    def get_profile(self):
        #اذا كان الself فيلو متغير اسمو tkoen وله فيمه كمل التاسك
        if hasattr(self, "token") and self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/auth/me", headers=headers, name="GET user profile")

    @task
    def update_user(self):
        if hasattr(self, "token") and self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.put(
                "/users/1",
                headers=headers,
                json={"firstName": "SamaUpdated"},
                name="PUT update user"
            )

    @task
    def delete_product(self):
        self.client.delete("/products/1", name="DELETE product")

    @task
    def create_product(self):
        self.client.post(
            "/products/add",
            json={
                "title": "Sama's Phone",
                "description": "performance testing",
                "price": 199
            },
            name="POST new product"
        )
