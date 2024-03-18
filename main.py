import streamlit as st

# Example menu items structured by categories
menu_items = {
    "Snacks": {
        "Pizza": {"price": 10.99, "image": "https://via.placeholder.com/150?text=Pizza"},
        "Burger": {"price": 5.99, "image": "https://via.placeholder.com/150?text=Burger"},
    },
    "Desserts": {
        "Ice Cream": {"price": 3.99, "image": "https://via.placeholder.com/150?text=Ice%20Cream"},
        "Cake": {"price": 4.99, "image": "https://via.placeholder.com/150?text=Cake"},
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

st.title('StockUpEats')

menu_column, order_column = st.columns([3, 1])

with menu_column:
    st.header("Menu")
    search_query = st.text_input("Search", "").lower()

    # Display menu items based on search query
    for category, items in menu_items.items():
        with st.expander(category, expanded=True):
            for item_name, details in items.items():
                if search_query in item_name.lower():
                    st.image(details['image'], width=100, caption=item_name)
                    st.write(f"Price: ₹{details['price']:.2f}")
                    # Use item_name and category as part of the key to ensure uniqueness
                    button_key = f"add_{category}_{item_name}".replace(" ", "_").lower()
                    if st.button(f"Add to Order", key=button_key):
                        add_to_order(category, item_name)
                    st.text("")

with order_column:
    st.header("Your Order")
    if st.session_state.order:
        total_price = 0
        for item_key, item_details in st.session_state.order.items():
            st.write(f"{item_details['name']} x {item_details['quantity']} = ₹{item_details['price'] * item_details['quantity']:.2f}")
            total_price += item_details['price'] * item_details['quantity']
        st.write(f"<span style='font-size: large; font-weight: bold;'>Total Price: ₹{total_price:.2f}</span>", unsafe_allow_html=True)
        if st.button("Place Order"):
            # Prompt the user to select payment method
            payment_method = st.selectbox("Select Payment Method", ("Counter", "Online"))
            if payment_method == "Counter":
                st.success("Your order has been placed! Please proceed to the counter for payment.")
            else:
                st.success("Your order has been placed! Please complete the payment online.")
            if st.button("Confirm"):
                st.success("Order confirmed!")
    else:
        st.write("Your order is empty.")
