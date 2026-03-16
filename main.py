import streamlit as st
import pandas as pd

st.title("🛒 Flipkart Shopping App")

# ---------------- PRODUCT LIST ----------------
if "products" not in st.session_state:
    st.session_state.products = [
        ["Laptop", 50000, 10],
        ["Mobile", 20000, 15],
        ["Headphones", 2000, 30],
        ["Keyboard", 1500, 20],
        ["Mouse", 800, 25]
    ]

# ---------------- CART ----------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------- DISPLAY PRODUCTS ----------------
st.subheader("📦 Available Products")

product_data = []

for i, p in enumerate(st.session_state.products):
    product_data.append([i+1, p[0], p[1], p[2]])

product_df = pd.DataFrame(
    product_data,
    columns=["ID", "Product Name", "Price (₹)", "Stock"]
)

st.dataframe(product_df, width="stretch")

# ---------------- ADD TO CART ----------------
st.sidebar.header("🛍 Add Product to Cart")

product_id = st.sidebar.number_input(
    "Enter Product ID",
    min_value=1,
    max_value=len(st.session_state.products),
    step=1
)

qty = st.sidebar.number_input(
    "Enter Quantity",
    min_value=1,
    step=1
)

if st.sidebar.button("Add to Cart"):

    selected_product = st.session_state.products[product_id - 1]

    if qty > selected_product[2]:
        st.sidebar.error("❌ Out of Stock")
    else:

        name = selected_product[0]
        price = selected_product[1]
        total = price * qty

        st.session_state.cart.append([product_id - 1, name, price, qty, total])

        # 🔽 Update stock
        st.session_state.products[product_id - 1][2] -= qty

        st.sidebar.success("✅ Item Added to Cart")

# ---------------- INVOICE ----------------
st.subheader("🧾 Invoice")

if st.session_state.cart:

    subtotal = 0

    header = st.columns(6)
    header[0].write("S.No")
    header[1].write("Product")
    header[2].write("Price")
    header[3].write("Qty")
    header[4].write("Total")
    header[5].write("Action")

    for i, item in enumerate(st.session_state.cart):

        col = st.columns(6)

        col[0].write(i+1)
        col[1].write(item[1])
        col[2].write(item[2])
        col[3].write(item[3])
        col[4].write(item[4])

        subtotal += item[4]

        if col[5].button("❌ Remove", key=i):

            # 🔼 Restore stock
            product_index = item[0]
            st.session_state.products[product_index][2] += item[3]

            st.session_state.cart.pop(i)

            st.rerun()

    st.divider()

    # ---------------- BILL CALCULATION ----------------
    discount = 0
    if subtotal > 50000:
        discount = subtotal * 0.10

    gst = (subtotal - discount) * 0.18
    final_amount = subtotal - discount + gst

    st.markdown(f"**Subtotal:** ₹ {subtotal:.2f}")
    st.markdown(f"**Discount (10% if subtotal > 50000):** -₹ {discount:.2f}")
    st.markdown(f"**GST (18%):** ₹ {gst:.2f}")

    st.markdown(f"## 💰 Final Payable Amount: ₹ {final_amount:.2f}")

    if st.button("🗑 Clear Cart"):

        # Restore all stock
        for item in st.session_state.cart:
            product_index = item[0]
            st.session_state.products[product_index][2] += item[3]

        st.session_state.cart = []

        st.success("Cart Cleared Successfully")
        st.rerun()

else:
    st.info("🛒 Cart is empty")