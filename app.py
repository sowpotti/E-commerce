import streamlit as st

# Sample product data
PRODUCTS = {
    "Mobiles": [
        {"id": 1, "name": "iPhone 16", "price": 59999},
        {"id": 2, "name": "Samsung Galaxy S25", "price": 79999},
    ],
    "Laptops": [
        {"id": 3, "name": "MacBook Air M4", "price": 110000},
        {"id": 4, "name": "Dell XPS 13", "price":99999},
    ],
    "Fashion": [
        {"id": 5, "name": "Levi's Jeans", "price": 2500},
        {"id": 6, "name": "Nike Sneakers", "price": 2000},
    ]
}


# Hardcoded user credentials
USERS = {
    "Lakshmi": "12345678",
    "Hari": "1818",
    "Sai": "7777"
}


# Used to store the shopping cart as a dictionary with product ID keys
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Stores the username of the logged-in user
if 'user' not in st.session_state:
    st.session_state.user = None


# APplication main header
st.title("🛒 E-Commerce Store")

# Sidebar login input fields for existing users
with st.sidebar:
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Validate login credentials
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.user = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password")

# Prevent access to shopping if user is not logged in
if not st.session_state.user:
    st.warning("Please log in to continue shopping.")
    st.stop()


st.sidebar.header("Categories")

# Allow user to pick a product category or view cart
category = st.sidebar.radio("Select a category:", list(PRODUCTS.keys()) + ["🛍️ View Cart"])

# Show products if a category is selected (not viewing cart)
if category != "🛍️ View Cart":
    st.header(f"Browse {category}")

    for product in PRODUCTS[category]:
        col1, col2 = st.columns([3, 1])

        # Product name and price
        with col1:
            st.subheader(product["name"])
            st.write(f"Price: Rs. {product['price']}")

        # Quantity input and add to cart button
        with col2:
            quantity = st.number_input(
                f"Qty - {product['id']}", min_value=1, step=1, key=f"qty_{product['id']}"
            )
            if st.button(f"Add {product['name']} to Cart", key=f"add_{product['id']}"):
                if product['id'] in st.session_state.cart:
                    st.session_state.cart[product['id']]['quantity'] += quantity
                else:
                    st.session_state.cart[product['id']] = {
                        'product': product,
                        'quantity': quantity
                    }
                st.success(f"Added {quantity} x {product['name']} to cart!")

# Cart page
else:
    st.header("Your Shopping Cart")

    # If no items, show empty message
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0

        # List all items with quantity and subtotal
        for idx, item in enumerate(st.session_state.cart.values()):
            name = item['product']['name']
            price = item['product']['price']
            qty = item['quantity']
            subtotal = price * qty
            st.write(f"{idx+1}. {name} - Rs. {price} x {qty} = Rs. {subtotal}")
            total += subtotal

        st.write("---")
        st.subheader(f"Total: Rs. {total}")

        # Simulated payment processing
        if st.button("Proceed to Payment"):
            st.success("✅ Payment successful! Order placed. Thank you.....!!!!!")
            st.session_state.cart.clear()