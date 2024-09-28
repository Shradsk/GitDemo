from flask import Flask, render_template, jsonify
import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

url = os.getenv('JIRA_URL')
auth = HTTPBasicAuth(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))

def fetch_jira_data():
    try:
        response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
        response.raise_for_status()
        issues = response.json().get("issues", [])

        issue_list = []
        for issue in issues:
            fields = issue["fields"]
            assignee = fields.get("assignee")
            assignee_name = assignee["displayName"] if assignee else "Unassigned"

            issue_list.append({
                "key": issue["key"],
                "summary": fields.get("summary", "No Summary"),
                "status": fields.get("status", {}).get("name", "No Status"),
                "assignee": assignee_name,
                "created": fields.get("created", "No Creation Date"),
                "priority": fields.get("priority", {}).get("name", "None")
            })

        return issue_list

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from JIRA: {e}")
        return []

@app.route('/api/jira-data')
def jira_data_view():
    data = fetch_jira_data()
    return jsonify(data)

@app.route('/chart')
def chart_view():
    return render_template('chart.html')

if __name__ == '__main__':
    app.run(debug=True)
