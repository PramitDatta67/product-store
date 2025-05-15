import streamlit as st
from utils.store import load_products, save_order
import os
import json

# Set up Streamlit configuration
st.set_page_config(page_title="Productivity Store", page_icon="🛒", layout="wide")

# Sidebar for navigation
st.sidebar.image("https://img.icons8.com/fluency/96/shop.png", width=100)
st.sidebar.title("🛍️ Navigation")
st.sidebar.button("Home", on_click=lambda: st.session_state.update(page="Home"))
st.sidebar.button("Shop Products", on_click=lambda: st.session_state.update(page="Shop"))
st.sidebar.button("Checkout", on_click=lambda: st.session_state.update(page="Checkout"))
st.sidebar.button("Admin Upload", on_click=lambda: st.session_state.update(page="Admin_Upload"))

# Load default page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# HOME PAGE
if st.session_state.page == "Home":
    st.image("https://images.unsplash.com/photo-1581090700227-1e8e97b17cc3", use_column_width=True)
    st.title("Welcome to the Productivity Store")
    st.markdown("Boost your work with handpicked productivity tools for professionals and leaders.")

# SHOP PRODUCTS
elif st.session_state.page == "Shop":
    st.title("Shop All Products")
    products = load_products()

    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            st.image(f"assets/images/{product['image']}", width=200)
            st.subheader(product['title'])
            st.write(f"₹{product['price']}")
            if st.button(f"Add {product['title']} to Cart", key=product['id']):
                if "cart" not in st.session_state:
                    st.session_state.cart = []
                st.session_state.cart.append(product)
                st.success(f"{product['title']} added to your cart!")

# CHECKOUT
elif st.session_state.page == "Checkout":
    st.title("Checkout")
    if "cart" in st.session_state and st.session_state.cart:
        total_price = sum([item['price'] for item in st.session_state.cart])
        st.write(f"Total: ₹{total_price}")
        
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        address = st.text_area("Shipping Address")

        if st.button("Confirm Order"):
            order = {
                "name": name,
                "email": email,
                "address": address,
                "items": st.session_state.cart,
                "total": total_price
            }
            save_order(order)
            st.success("Order confirmed! Thank you for your purchase.")
            st.session_state.cart = []  # Clear cart after checkout
    else:
        st.warning("Your cart is empty. Please add items to cart before checking out.")

# ADMIN UPLOAD
elif st.session_state.page == "Admin_Upload":
    st.title("Admin Upload Products")
    product_title = st.text_input("Product Title")
    product_price = st.number_input("Product Price", min_value=0)
    product_category = st.selectbox("Category", ["Desk", "Gadget", "Tool"])
    product_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if st.button("Add Product"):
        if product_title and product_price and product_category and product_image:
            products = load_products()
            new_product = {
                "id": len(products) + 1,
                "title": product_title,
                "price": product_price,
                "category": product_category,
                "image": product_image.name,
                "payment_link": "https://buy.stripe.com/test_example"
            }

            # Save the uploaded image
            os.makedirs("assets/images", exist_ok=True)
            with open(f"assets/images/{product_image.name}", "wb") as f:
                f.write(product_image.getbuffer())

            # Save product to JSON
            with open("data/products.json", "a") as f:
                json.dump(new_product, f)
                f.write("\n")

            st.success(f"{product_title} added to the store!")
        else:
            st.error("Please fill in all the fields.")
