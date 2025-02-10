import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

github_org = "XCollab"  # Replace with your GitHub organization name
github_token = os.getenv("GITHUB_TOKEN")  # Store the GitHub token securely

def get_authenticated_user():
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("login")
    return None

def is_admin(user):
    url = f"https://api.github.com/orgs/{github_org}/memberships/{user}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        membership = response.json()
        return membership.get("role") == "admin"
    return False

def invite_user(username):
    url = f"https://api.github.com/orgs/{github_org}/invitations"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"invitee_id": get_user_id(username)}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        return f"✅ Successfully invited {username} to {github_org}! Please Check the Email"
    elif response.status_code == 422:
        return "⚠️ User is already a member or has a pending invite."
    elif response.status_code == 403:
        return ("❌ Error: Token does not have admin privileges to create an invitation. "
                "Please use an admin token with the 'admin:org' scope.")
    else:
        return f"❌ Error: {response.json()}"

def get_user_id(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("id")
    else:
        return None

st.title("🚀 Auto Invite to GitHub Community")
username = st.text_input("Enter GitHub Username:")

if st.button("Send Invite"):
    if github_token is None:
        st.error("GitHub token is missing! Set it in environment variables.")
    elif username.strip():
        result = invite_user(username.strip())
        st.write(result)
        
        # Show WhatsApp group link only if invitation was successful
        if result.startswith("✅"):
            st.success("🎉 You're invited! Join our WhatsApp group for project discussions:")
            st.markdown("### [Join WhatsApp Group](https://chat.whatsapp.com/JLuhWHAzeg7GuPRmhnGBKB)") 
    else:
        st.warning("Please enter a valid GitHub username.")
