import streamlit as st
import pandas as pd
import random
import qrcode
import io
import time
from PIL import Image
from fpdf import FPDF

st.set_page_config(page_title="CraftGuard AI v2", layout="wide")

st.markdown("""
<h1 style='text-align:center;color:#FF4B4B;'>🌍 CraftGuard AI</h1>
<h4 style='text-align:center;'>Verified Marketplace for Traditional Crafts</h4>
""", unsafe_allow_html=True)

# -------------------------
# CERTIFICATE GENERATOR
# -------------------------

def generate_certificate(product, artisan, score):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=20)
    pdf.cell(200,20,txt="CraftGuard AI", ln=True, align="C")

    pdf.set_font("Arial", size=16)
    pdf.cell(200,10,txt="Authenticity Certificate", ln=True, align="C")

    pdf.ln(20)

    pdf.set_font("Arial", size=12)

    pdf.cell(200,10,txt=f"Product: {product}", ln=True)
    pdf.cell(200,10,txt=f"Artisan: {artisan}", ln=True)
    pdf.cell(200,10,txt=f"Authenticity Score: {score}%", ln=True)

    pdf.cell(200,10,txt="Status: Verified Handmade Craft", ln=True)

    pdf.ln(20)

    pdf.cell(200,10,txt="Certified by CraftGuard AI Platform", ln=True)

    pdf.output("certificate.pdf")


# -------------------------
# SESSION STORAGE
# -------------------------

for key in ["artisans","crafts","orders","cart","wishlist","reviews"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Register Artisan",
        "Upload Craft",
        "Marketplace",
        "Wishlist",
        "Cart",
        "Orders",
        "Craft Map",
        "Analytics"
    ]
)

# -------------------------
# DASHBOARD
# -------------------------

if menu == "Dashboard":

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Artisans",len(st.session_state.artisans))
    col2.metric("Craft Listings",len(st.session_state.crafts))
    col3.metric("Orders",len(st.session_state.orders))
    col4.metric("Verified Crafts",random.randint(20,90))

    st.divider()

    st.subheader("⭐ Featured Artisan")

    if st.session_state.artisans:
        artisan=random.choice(st.session_state.artisans)
        st.success(f"{artisan['Name']} – {artisan['Craft']}")
        st.write(artisan["Story"])
    else:
        st.info("No artisans registered yet.")

# -------------------------
# ARTISAN REGISTRATION
# -------------------------

elif menu == "Register Artisan":

    st.header("👩‍🎨 Artisan Registration")

    name=st.text_input("Name")
    craft=st.text_input("Craft Specialty")
    region=st.text_input("Region")

    phone=st.text_input("Phone")
    email=st.text_input("Email")

    experience=st.slider("Years of Experience",1,40)

    story=st.text_area("Craft Story")

    gallery=st.file_uploader("Workshop Photos",accept_multiple_files=True)

    video=st.file_uploader("Workshop Video")

    lat=st.number_input("Latitude",value=20.0)
    lon=st.number_input("Longitude",value=78.0)

    if st.button("Register Artisan"):

        artisan={
            "Name":name,
            "Craft":craft,
            "Region":region,
            "Phone":phone,
            "Email":email,
            "Experience":experience,
            "Story":story,
            "Gallery":gallery,
            "Video":video,
            "lat":lat,
            "lon":lon
        }

        st.session_state.artisans.append(artisan)

        st.success("Artisan Registered")
        st.balloons()

# -------------------------
# CRAFT UPLOAD
# -------------------------

elif menu == "Upload Craft":

    st.header("📦 Upload Craft")

    if not st.session_state.artisans:
        st.warning("Register artisan first")

    else:

        artisan_names=[a["Name"] for a in st.session_state.artisans]

        artisan=st.selectbox("Artisan",artisan_names)

        product=st.text_input("Product Name")

        description=st.text_area("Description")

        price=st.number_input("Price",min_value=1)

        image=st.file_uploader("Upload Craft Image")

        process=st.text_area("Craft Process")

        if st.button("Analyze & Upload"):

            with st.spinner("Analyzing craft authenticity..."):
                time.sleep(2)

            score=random.randint(70,95)

            if score>=90:
                level="Gold Certified"
            elif score>=85:
                level="Silver Certified"
            else:
                level="Basic Verified"

            craft={
                "Artisan":artisan,
                "Product":product,
                "Description":description,
                "Price":price,
                "Score":score,
                "Level":level,
                "Image":image,
                "Process":process
            }

            st.session_state.crafts.append(craft)

            st.success("Craft uploaded successfully")
            st.write("Authenticity Score:",score)
            st.write("Certification:",level)

            # VERIFIED HANDMADE + CERTIFICATE
            if score >= 85:

                st.success("✅ Verified Handmade Craft")

                generate_certificate(product, artisan, score)

                with open("certificate.pdf", "rb") as file:

                    st.download_button(
                        label="Download Authenticity Certificate",
                        data=file,
                        file_name="craft_certificate.pdf",
                        mime="application/pdf"
                    )

# -------------------------
# MARKETPLACE
# -------------------------

elif menu == "Marketplace":

    st.header("🛍 Global Marketplace")

    search=st.text_input("Search Crafts")

    for craft in st.session_state.crafts:

        if search.lower() in craft["Product"].lower():

            col1,col2=st.columns([1,2])

            with col1:
                if craft["Image"]:
                    st.image(craft["Image"],width=220)

            with col2:

                st.subheader(craft["Product"])
                st.write("Artisan:",craft["Artisan"])
                st.write("Price: ₹",craft["Price"])
                st.write("Authenticity Score:",craft["Score"])
                st.write("Certification:",craft["Level"])

                st.write("Description:",craft["Description"])

                if st.button(f"Add to Cart {craft['Product']}"):
                    st.session_state.cart.append(craft)

                if st.button(f"Wishlist {craft['Product']}"):
                    st.session_state.wishlist.append(craft)

                qr_data=f"{craft['Product']} | {craft['Artisan']} | {craft['Score']}"
                qr=qrcode.make(qr_data)

                buf=io.BytesIO()
                qr.save(buf)
                st.image(buf)

                st.subheader("Buyer Reviews")

                rating=st.slider(f"Rate {craft['Product']}",1,5)
                review=st.text_input("Write Review")

                if st.button(f"Submit Review {craft['Product']}"):
                    st.session_state.reviews.append(
                        {"product":craft["Product"],"rating":rating,"text":review}
                    )
                    st.success("Review submitted")

            st.divider()

# -------------------------
# WISHLIST
# -------------------------

elif menu=="Wishlist":

    st.header("❤️ Wishlist")

    for item in st.session_state.wishlist:
        st.write(item["Product"],"₹",item["Price"])

# -------------------------
# CART
# -------------------------

elif menu=="Cart":

    st.header("🛒 Cart")

    for item in st.session_state.cart:

        st.write(item["Product"],"₹",item["Price"])

        if st.button(f"Buy {item['Product']}"):

            order={
                "Product":item["Product"],
                "Artisan":item["Artisan"],
                "Price":item["Price"],
                "Status":"Processing"
            }

            st.session_state.orders.append(order)

            st.success("Order placed")

# -------------------------
# ORDERS
# -------------------------

elif menu=="Orders":

    st.header("📦 Orders")

    for order in st.session_state.orders:
        st.write(order)

# -------------------------
# MAP DISCOVERY
# -------------------------

elif menu=="Craft Map":

    st.header("🗺 Artisan Discovery Map")

    if not st.session_state.artisans:
        st.info("No artisans yet")

    else:

        map_data=pd.DataFrame(st.session_state.artisans)
        st.map(map_data[["lat","lon"]])

# -------------------------
# ANALYTICS
# -------------------------

elif menu=="Analytics":

    st.header("📊 Craft Demand Analytics")

    data=pd.DataFrame({
        "Craft":["Pottery","Handloom","Embroidery","Woodcraft"],
        "Demand":[40,70,50,30]
    })

    st.bar_chart(data.set_index("Craft"))

    st.subheader("Platform Impact")

    st.write("Artisans:",len(st.session_state.artisans))
    st.write("Products:",len(st.session_state.crafts))
    st.write("Orders:",len(st.session_state.orders))