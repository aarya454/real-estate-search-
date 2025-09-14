#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd






# In[2]:


df = pd.read_csv(r'Mumbai_dataset.csv')




# In[3]:


#df.head()


# In[4]:


#df.head()


# In[5]:


#df.shape


# In[6]:


#df.groupby('type')['type'].agg('count')


# In[7]:


#df.groupby('age')['age'].agg('count')


# In[8]:


#df.groupby('region')['region'].agg('count')


# In[9]:


#df.isnull().sum()


# In[10]:


df1 = df.dropna()
df1.isnull().sum()


# In[11]:


#df1.shape


# In[12]:


#df1['bhk'].unique()


# In[13]:


#df1.head()


# In[14]:


df1['price_per_sqft_area'] = df1['price']*1000000/df1['area']
#df1.head()


# In[15]:


#len(df1.locality.unique())


# In[16]:


df1.region = df1.region.apply(lambda x: x.strip())

region_stats = df1.groupby('region')['region'].agg('count').sort_values(ascending=False)
#region_stats


# In[17]:


region_stats_less_then_10 = region_stats[region_stats<=10]
#region_stats_less_then_10


# In[18]:


df1.region = df1.region.apply(lambda x: 'other' if x in region_stats_less_then_10 else x)
len(df1.region.unique())


# In[19]:


#df1.head(10)


# In[20]:


#df1[df1.area/df1.bhk<300].head()


# In[21]:


#df1.price_per_sqft_area.describe()


# In[22]:


#df1.head()


# In[23]:


# bhk
# type
# locality
# area
# price
# region
# status
# age
# price_per_sqft_area
df2 = df1[['bhk','type','locality','area','price','price_unit','region','status','age','price_per_sqft_area']]


# In[24]:


#df2.head()


# In[25]:


#df2.isnull().sum()


# In[26]:


df2.dropna (inplace=True)


# In[27]:


#df2.duplicated().sum()


# In[28]:


#df2.iloc[0].region


# In[29]:


df2['region'] = df2['region'].str.lower().str.strip()


# In[30]:


def recommend_by_region(location_name):
    location_name = location_name.lower().strip()
    filtered = df2[df2['region'].str.contains(location_name)]
    if filtered.empty:
        return f"No properties found in '{location_name}'"
    else:
        return filtered.reset_index(drop=True)


# In[31]:


#df2.head()


# In[37]:

# In[ ]:




import pandas as pd

import streamlit as st
import pandas as pd

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("Mumbai_dataset.csv")
    df['region'] = df['region'].astype(str).str.lower().str.strip()
    df['locality'] = df['locality'].astype(str).str.strip()
    return df

df = load_data()

# Prepare filter options
regions = sorted(df["region"].dropna().astype(str).unique())
localities = sorted(df["locality"].dropna().astype(str).unique())
min_price = int(df["price"].min())
max_price = int(df["price"].max())


# ---------- Custom CSS for Navbar ----------
st.markdown(
    """
    <style>
        .search-bar {
            display: flex;
            justify-content: space-between;
            background: #0a3d62;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            color: white;
        }
        .search-bar label {
            color: white !important;
            font-weight: bold;
        }
        .search-bar .stSelectbox, .search-bar .stSlider {
            background: white;
            border-radius: 6px;
            padding: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)




# HERO SEARCH BAR
# ------------------------------
st.markdown(
    """
    <style>
    .hero-box {
        background: #0a3d62;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        justify-content: center;
    }
    .hero-box label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 🔎 Property Finder Search")

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    region = st.selectbox("Region", ["All"] + sorted(df["region"].unique()))
with col2:
    locality = st.selectbox("Locality", ["All"] + sorted(df["locality"].unique()))
with col3:
    bhk_options = ["All"] + sorted({int(float(b)) for b in df["bhk"].dropna().unique()})
    bhk = st.selectbox("BHK", bhk_options)
with col4:
    budget = st.selectbox("Budget", ["All", "₹50L - ₹1Cr", "₹1Cr - ₹2Cr", "₹2Cr+"])
with col5:
    post_property = st.button("➕ Post Property")


search = st.button("🔍 Search")

if search:
    st.success("Search button clicked! (filters will apply below)")






# ---------- Post Property Form ----------
if post_property:
    st.subheader("Post Your Property")
    with st.form("post_form", clear_on_submit=True):
        region = st.text_input("Region (e.g., Andheri, Bandra)")
        locality = st.text_input("Locality (e.g., Powai, Lokhandwala)")
        bhk = st.selectbox("BHK", ["1", "2", "3", "4", "5+"])
        price = st.number_input("Price (in Lakhs)", min_value=1)
        image = st.file_uploader("Upload Property Image", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("Submit Property")

        if submitted:
            st.success("✅ Your property has been posted successfully!")
            st.info(f"Region: {region}, Locality: {locality}, BHK: {bhk}, Price: ₹{price} Lakhs")
            if image:
                st.image(image, caption="Uploaded Property Image", use_container_width=True)






# ---------- Apply Filters ----------
filtered = df.copy()

if region != "All":
    filtered = filtered[filtered["region"] == region]

if locality != "All":
    filtered = filtered[filtered["locality"] == locality]

if budget != "All":
    if budget == "₹50L - ₹1Cr":
        filtered = filtered[(filtered["price"] >= 5000000) & (filtered["price"] <= 10000000)]
    elif budget == "₹1Cr - ₹2Cr":
        filtered = filtered[(filtered["price"] >= 10000000) & (filtered["price"] <= 20000000)]
    elif budget == "₹2Cr+":
        filtered = filtered[filtered["price"] > 20000000]


# List of 10 property images
property_images = [
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flat%201.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flat%202.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flat%203.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flAT%204.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/FLAT%205.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/FLAT6.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/FLAT7.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flat8.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flat9.jpg",
    r"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/flat10.jpg"
]




# ---------- Show Properties ----------

import streamlit as st
import streamlit.components.v1 as components

# Function to convert image to base64


# ✅ Use raw strings (r"...") for Windows paths
img_urls = [
"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/tower1.jpg",
"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/tower2.jpg",
"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/tower3.jpg",
"https://raw.githubusercontent.com/aarya454/real-estate-search-/36668be2a9e2bb7fa61f21c5a086cd9758cc55f7/tower4.jpg",
]

# ✅ Notice the f here ↓
carousel_html = f"""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick-theme.min.css"/>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.9.0/slick.min.js"></script>

<style>
.carousel-container {{
    width: 100%;
    margin: auto;
}}
.slick-slide img {{
    width: 100%;
    border-radius: 12px;
}}
</style>

<div class="carousel-container">
  <div class="carousel">
    <div><img src="{img_urls[0]}" alt="Luxury Tower 1"></div>
    <div><img src="{img_urls[1]}" alt="Skyline Tower"></div>
    <div><img src="{img_urls[2]}" alt="Modern Residences"></div>
    <div><img src="{img_urls[3]}" alt="Classic Apartments"></div>
  </div>
</div>


<script>
$(document).ready(function(){{
  $('.carousel').slick({{
    dots: true,
    infinite: true,
    autoplay: true,
    autoplaySpeed: 2000,
    arrows: true
  }});
}});
</script>
"""

st.subheader("🏙️ Featured Towers")
components.html(carousel_html, height=450)




st.subheader("🏡 Available Properties")

if filtered.empty:
    st.warning("No properties found with the given filters.")
else:
    for i, (_, row) in enumerate(filtered.iterrows()):
        with st.container():
            col1, col2 = st.columns([1, 2])

            # Left column = Property Image
            # Left column = Property Image from dataset
        # Left column = Property Image
        with col1:
            st.image(property_images[i % len(property_images)], use_container_width=True)

            # Right column = Property Details
            with col2:
                st.markdown(f"### {row['locality']} - {row['bhk']} BHK")
                st.markdown(f"**Region:** {row['region'].title()}")
                st.markdown(f"**Price:** ₹ {row['price']} {row['price_unit']}")
                st.markdown(f"**Area:** {row['area']} sq.ft")
                st.markdown(f"**Status:** {row['status']}")
                st.markdown(f"**Age:** {row['age']}")

        st.markdown("---")






    
# %%
