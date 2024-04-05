import streamlit as st
import base64
import random
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Define the SQLite database
DATABASE_URL = "sqlite:///stockupeats.db"
Base = declarative_base()

# Define the Orders model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, unique=True, index=True)
    items = Column(String)
    total_price = Column(Float)

# Create the database and tables
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_order(order_number, items, total_price):
    db = SessionLocal()
    try:
        items_json = json.dumps(items)  # Convert items dictionary to JSON string
        order = Order(order_number=order_number, items=items_json, total_price=total_price)
        db.add(order)
        db.commit()
    finally:
        db.close()

def get_order(order_number):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_number == order_number).first()
        if order:
            items_dict = json.loads(order.items)
            order.items = items_dict
        return order
    finally:
        db.close()

# Custom CSS for styling
main_page_style = """
<style>
body {
    background-color: #e6f3ff;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.stButton>button:hover {
    background-color: #45a049;
}

.stTextInput>div>div>input {
    border-radius: 4px;
}
</style>
"""

st.set_page_config(layout="wide")

# Apply custom CSS
st.markdown(main_page_style, unsafe_allow_html=True)

# Registered usernames and passwords (for demonstration purposes)
registered_users = {"user1": "password1", "user2": "password2", "user3": "password3", "cashier": "cashierpassword"}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Page title and header
st.title("StockUpEats")
st.header("Welcome to StockUpEats - Your Favorite Food Ordering App!")

# Login form
login_form_placeholder = st.empty()
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    if username in registered_users:
        if password == registered_users[username]:
            st.session_state.logged_in = True
            st.session_state.user_type = 'cashier' if username == 'cashier' else 'customer'
            st.success(f"Welcome back, {username}!")
            st.write("Redirecting to the main interface...")
            # Add a redirect or load the main interface here
            login_form_placeholder.empty()
        else:
            st.error("Incorrect password. Please try again.")
    else:
        st.error("User not found. Please check your username.")

# Check if user is logged in before displaying content
if st.session_state.logged_in:
    if st.session_state.user_type == 'customer':
        # Existing code for customer interface
        # Example menu items structured by categories
        menu_items = {
            "Snacks": {
                "Vada Pav": {"price": 25.00, "image": "data:image/png;base64," + base64.b64encode(open("static/vadapav.png", "rb").read()).decode()},
                "Pizza": {"price": 150.00, "image": "data:image/png;base64," + base64.b64encode(open("static/pizza.png", "rb").read()).decode()},
                "Burger": {"price": 55.00, "image": "data:image/png;base64," + base64.b64encode(open("static/burger.png", "rb").read()).decode()},
            },
            "Desserts": {
                "Ice Cream": {"price": 40.00, "image": "data:image/png;base64," + base64.b64encode(open("static/icecream.png", "rb").read()).decode()},
                "Cake": {"price": 55.00, "image": "data:image/png;base64," + base64.b64encode(open("static/cake.png", "rb").read()).decode()},
            },
            # Add more categories and items as needed
        }

        if 'order' not in st.session_state:
            st.session_state.order = {}

        # Function to add items to the order
        def add_to_order(category, item_name):
            item_key = f"{category} - {item_name}"
            if item_key in st.session_state.order:
                st.session_state.order[item_key]['quantity'] += 1
            else:
                st.session_state.order[item_key] = {"name": item_name, "category": category, "quantity": 1, "price": menu_items[category][item_name]['price']}

        # Title of the app
        st.title('StockUpEats')

        # Option menu for choosing between sections
        selected_option = st.sidebar.selectbox("Choose an option:", ["Menu", "Meet Our Team", "Give Feedback", "Cart"])

        if selected_option == "Meet Our Team":
            # Meet Our Team section
            st.header("Meet Our Team")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.image("static/arindam.png", width=150)
                st.write("Arindam Pandey")

            with col2:
                st.image("static/sankalp.png", width=150)
                st.write("Sankalp Hargode")

            with col3:
                st.image("static/vinayak.png", width=150)
                st.write("Vinayak Punj")

            with col4:
                st.image("static/sagar.png", width=150)
                st.write("Sagar Tarachandani")

        elif selected_option == "Give Feedback":
            # Give Feedback section
            st.header("Give Feedback")
            feedback = st.text_area("Please provide your feedback here:", "")
            if st.button("Submit Feedback"):
                # Process feedback here (e.g., save to database)
                st.success("Thank you for your feedback!")

        elif selected_option == "Cart":
            st.header("Your Cart")
            total_price = 0
            for item, details in st.session_state.cart.items():
                total_price += details['quantity'] * details['price']
                st.write(f"{item}: {details['quantity']}")
            st.write(f"Total Price: ₹{total_price:.2f}")

            if st.button("Proceed to Checkout"):
                # Add code to proceed to checkout
                payment_option = st.radio("Choose a payment option:", ["Pay at Counter", "Pay Online"])
                if payment_option == "Pay at Counter":
                    st.success("Redirecting you to pay at the counter.")
                    order_number = random.randint(100, 999)
                    save_order(order_number, st.session_state.order, total_price)
                    st.success(f"Order placed! Your order number is {order_number}.")
                elif payment_option == "Pay Online":
                    st.success("Redirecting you to pay online.")
                    order_number = random.randint(100, 999)
                    save_order(order_number, st.session_state.order, total_price)
                    st.success(f"Order placed! Your order number is {order_number}.")

        else:
            # Menu section
            st.header("Menu")
            search_query = st.text_input("Search", "").lower()

            # Display menu items based on search query
            for category, items in menu_items.items():
                with st.expander(category, expanded=True):
                    for item_name, details in items.items():
                        if search_query in item_name.lower():
                            st.image(details['image'], width=150, caption=item_name)
                            st.write(f"Price: ₹{details['price']:.2f}")
                            # Use item_name and category as part of the key to ensure uniqueness
                            button_key = f"add_{category}_{item_name}".replace(" ", "_").lower()
                            if st.button(f"Add to Order", key=button_key):
                                add_to_order(category, item_name)
                                if item_name in st.session_state.cart:
                                    st.session_state.cart[item_name]['quantity'] += 1
                                else:
                                    st.session_state.cart[item_name] = {"name": item_name, "quantity": 1, "price": details['price']}
                            st.text("")
    elif st.session_state.user_type == 'cashier':
        # Cashier interface
        st.header("Cashier Dashboard")
        order_number = st.number_input("Enter Order Number", value=0, step=1, min_value=0)
        if st.button("Fetch Order"):
            if order_number != 0:
                order = get_order(order_number)
                if order:
                    st.subheader(f"Order Details for Order Number: {order.order_number}")
                    st.write("Items:", )
                    st.table(order.items)
                    st.write(f"Total Price: ₹{order.total_price:.2f}")
                    #st.write(f"Order Number: {order.order_number}, Items: {order.items}, Total Price: {order.total_price}")
                    # Add code for payment here
                else:
                    st.warning("Order not found.")
            else:
                st.warning("Please enter a valid order number.")
else:
    st.info("Please login to access StockUpEats.")
