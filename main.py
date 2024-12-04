import json
import requests
import streamlit as st
import pandas as pd


# Fetch JSON data from URL
def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


# Add custom users
def add_custom_users(users):
    custom_users = [
        {
            "id": 11,
            "name": "Your Name",
            "username": "yourusername",
            "email": "yourname@example.com",
            "address": {"city": "YourCity", "geo": {"lat": "48.8566", "lng": "2.3522"}},
        },
        {
            "id": 12,
            "name": "John Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "address": {
                "city": "Newville",
                "geo": {"lat": "34.0522", "lng": "-118.2437"},
            },
        },
        {
            "id": 13,
            "name": "Jane Smith",
            "username": "janesmith",
            "email": "janesmith@example.com",
            "address": {"city": "Oldtown", "geo": {"lat": "51.5074", "lng": "-0.1278"}},
        },
    ]
    users.extend(custom_users)
    return users


# Streamlit app
def main():
    st.title("User Search and Map Viewer")

    # Load and prepare data
    users = fetch_users()
    users = add_custom_users(users)

    # Convert users to a DataFrame
    data = pd.DataFrame(
        [
            {
                "Name": user["name"],
                "City": user["address"]["city"],
                "Lat": user["address"]["geo"]["lat"],
                "Lng": user["address"]["geo"]["lng"],
            }
            for user in users
        ]
    )

    # Search functionality
    search_option = st.selectbox("Search by", ["City", "Name"])
    search_query = st.text_input(f"Enter {search_option}:")

    if search_query:
        # Filter data based on search query
        results = data[data[search_option].str.contains(search_query)]

        if not results.empty:
            # Create a selectbox to choose a user
            selected_user = st.selectbox("Select a user:", results["Name"].tolist())

            if selected_user:
                # Display user details
                user_data = results[results["Name"] == selected_user].iloc[0]
                st.write(f"**Selected User:** {user_data['Name']}")
                st.write(f"**City:** {user_data['City']}")

                # Display map
                st.map(
                    pd.DataFrame(
                        {
                            "lat": [float(user_data["Lat"])],
                            "lon": [float(user_data["Lng"])],
                        }
                    )
                )
        else:
            st.write("No results found.")


main()
