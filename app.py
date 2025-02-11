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

# Updated user interface
st.set_page_config(page_title="XCollab Inviter", page_icon=":busts_in_silhouette:")

st.title('XCollab Inviter')
st.subheader("An open-source community built 𝗳𝗼𝗿 𝘀𝘁𝘂𝗱𝗲𝗻𝘁𝘀, 𝗯𝘆 𝘀𝘁𝘂𝗱𝗲𝗻𝘁𝘀.")
st.write("""Welcome to X Collaborators, a vibrant community of developers, learners, and enthusiasts passionate about building cutting-edge solutions in AI/ML, Python, JavaScript, and beyond! Our mission
            is to foster collaboration, innovation, and learning in the open-source ecosystem.""")
         

username = st.text_input("GitHub Username:")

if st.button("Send Invite"):
    if github_token is None:
        st.error("GitHub token is missing! Please set it in your environment variables.")
    elif username.strip():
        result = invite_user(username.strip())
        st.write(result)
        
        if result.startswith("✅"):
            st.success("🎉 Invitation sent successfully!")
            
            # Create a visually appealing container for next steps
            with st.container():
                st.markdown("""
                ### Next Steps 📋
                1. Check your email for the GitHub invitation
                2. Join our community chat for project discussions
                """)
            
            # Style the WhatsApp button with custom HTML/CSS
            st.markdown("""
            <div style='background-color:#25D366; padding:12px; border-radius:8px; text-align:center;'>
                <a href='https://chat.whatsapp.com/JLuhWHAzeg7GuPRmhnGBKB' 
                   style='color:white; text-decoration:none; font-weight:bold;'>
                💬 Join WhatsApp Group
                </a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a valid GitHub username.")
