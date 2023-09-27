import requests
from bs4 import BeautifulSoup
import html

class GradescopeClient:
    def __init__(self, token=None):
        self.logged_in = False
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        
        if token:
            self.login(token)

    def is_logged_in(self):
        return self.logged_in

    def authenticated(self):
        response = self.session.get("https://www.gradescope.com/login")
        if response.status_code == 404:
            return False
        elif response.status_code == 401:
            return True
        else:
            raise Exception("HTTP Error")

    def login(self, token):
        self.session.get("https://www.gradescope.com")
        if self.authenticated():
            self.logged_in = True
        else:
            raise Exception("Invalid Login")

    def submit_files(self, course_id, assignment_id, files):
        if not self.logged_in:
            raise Exception("Invalid State")
        
        response = self.session.get(f"https://www.gradescope.com/courses/{course_id}")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]

        form_data = {
            "authenticity_token": csrf_token,
            "submission[method]": "upload",
        }
        
        for file_path in files:
            with open(file_path, "rb") as file:
                file_name = file_path.split("/")[-1]
                form_data[f"submission[files][]"] = (file_name, file)

        response = self.session.post(
            f"https://www.gradescope.com/courses/{course_id}/assignments/{assignment_id}/submissions",
            data=form_data,
        )

        submit_response = response.json()

        if "error" in submit_response:
            raise Exception(f"Submit Error: {submit_response['error']}")
        elif "success" in submit_response and submit_response["success"]:
            if "url" in submit_response:
                return f"https://www.gradescope.com{submit_response['url']}"
            else:
                return None
        else:
            raise Exception("Submit Error")
