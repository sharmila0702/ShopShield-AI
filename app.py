import streamlit as st
import pandas as pd
import requests
import re
from urllib.parse import quote

# ============================================================
# SHOPSHIELD AI
# ============================================================

st.set_page_config(
    page_title="ShopShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ============================================================
# BLUE PROFESSIONAL THEME
# ============================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #061A2E, #0B2D4D, #0D47A1);
    color: white;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: white !important;
}

p, label {
    color: #EAF6FF !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #1565C0, #2196F3);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
}

[data-testid="stMetric"] {
    background: rgba(33,150,243,0.15);
    padding: 15px;
    border-radius: 15px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061A2E, #0B2D4D);
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #102F4A !important;
    color: white !important;
}

div[data-baseweb="select"] > div {
    background-color: #102F4A !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "entered" not in st.session_state:
    st.session_state.entered = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# ============================================================
# LANDING PAGE
# ============================================================

if not st.session_state.entered:

    st.title("🛡️ ShopShield AI")
    st.subheader("Your Agentic Shopping Guardian")

    st.write(
        "Don't just find a product. Find the product that's actually "
        "worth buying."
    )

    st.info(
        "ShopShield analyzes your requirement, compares brands and models, "
        "checks your budget, identifies risks and gives a BUY, CONSIDER "
        "or AVOID decision."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🤖 Agentic Analysis")
        st.write("Requirement → Product → Decision")

    with c2:
        st.markdown("### 💰 Smart Budget")
        st.write("Checks affordability.")

    with c3:
        st.markdown("### 🛡️ Purchase Protection")
        st.write("Detects purchase risks.")

    st.markdown("---")

    name = st.text_input("Enter your name")

    if st.button("🚀 Start Smart Shopping", use_container_width=True):

        if name.strip():
            st.session_state.user_name = name
            st.session_state.entered = True
            st.rerun()
        else:
            st.warning("Please enter your name.")

    st.stop()


# ============================================================
# MODEL-SPECIFIC IMAGE FUNCTION
# ============================================================

@st.cache_data(show_spinner=False)
def get_product_image(brand, model, category):

    search_text = f"{brand} {model} {category} product"

    encoded = quote(search_text)

    # Bing image thumbnail/search endpoint.
    # Query contains the exact brand + model, so each product
    # gets a different image instead of one category image.
    image_url = (
        f"https://tse1.mm.bing.net/th?q={encoded}"
        f"&w=800&h=600&c=7&rs=1&p=0"
    )

    try:
        response = requests.get(
            image_url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code == 200:
            return image_url

    except Exception:
        pass

    return "https://placehold.co/800x600/0B2D4D/FFFFFF?text=Product+Image"


# ============================================================
# PRODUCT DATABASE
# ============================================================

products = [

# LAPTOP
["Laptop","Lenovo","IdeaPad Slim 5",59990,4.4,86,88,512],
["Laptop","HP","Pavilion 14",57990,4.3,84,85,512],
["Laptop","Dell","Inspiron 14",62990,4.4,87,86,512],
["Laptop","ASUS","Vivobook 15",54990,4.5,88,84,512],
["Laptop","Acer","Aspire 5",52990,4.3,82,83,512],
["Laptop","Apple","MacBook Air",99990,4.7,94,92,512],
["Laptop","MSI","Modern 14",61990,4.3,90,82,512],
["Laptop","Samsung","Galaxy Book",69990,4.4,88,89,512],

# SMARTPHONE
["Smartphone","Samsung","Galaxy A56",29999,4.4,86,88,256],
["Smartphone","OPPO","Reno Series",28999,4.5,88,90,256],
["Smartphone","OnePlus","Nord Series",27999,4.4,92,86,256],
["Smartphone","Vivo","V Series",26999,4.3,85,91,256],
["Smartphone","Xiaomi","Xiaomi Series",24999,4.3,90,87,256],
["Smartphone","Redmi","Note Series",21999,4.2,86,85,256],
["Smartphone","Realme","GT Series",23999,4.3,91,84,256],
["Smartphone","Motorola","Edge Series",25999,4.2,88,87,256],
["Smartphone","Apple","iPhone Series",69990,4.7,96,90,256],
["Smartphone","Google","Pixel Series",59999,4.5,91,89,128],

# HEADPHONES
["Headphones","Sony","WH Series",29990,4.7,94,92,0],
["Headphones","JBL","Tune Series",7999,4.5,86,88,0],
["Headphones","boAt","Rockerz Series",2499,4.2,78,84,0],
["Headphones","Sennheiser","Momentum Series",24990,4.7,96,90,0],
["Headphones","Bose","QuietComfort Series",27990,4.6,94,91,0],
["Headphones","OnePlus","Buds Series",4999,4.3,84,86,0],
["Headphones","Noise","Air Series",2999,4.2,79,85,0],

# SMARTWATCH
["Smartwatch","Apple","Watch Series",44990,4.7,95,90,0],
["Smartwatch","Samsung","Galaxy Watch",29990,4.5,91,92,0],
["Smartwatch","Garmin","Forerunner Series",32990,4.6,94,95,0],
["Smartwatch","Noise","ColorFit Series",2999,4.2,78,88,0],
["Smartwatch","boAt","Wave Series",2499,4.1,75,86,0],
["Smartwatch","Fire-Boltt","Phoenix Series",1999,4.0,74,84,0],
["Smartwatch","Amazfit","GTS Series",9999,4.4,87,92,0],
["Smartwatch","OnePlus","Watch Series",14999,4.3,89,90,0],

# TABLET
["Tablet","Apple","iPad Air",59990,4.7,95,92,256],
["Tablet","Samsung","Galaxy Tab Series",34990,4.5,89,91,256],
["Tablet","Lenovo","Tab Series",24990,4.3,83,88,128],
["Tablet","OnePlus","Pad Series",29990,4.4,91,89,128],
["Tablet","Xiaomi","Pad Series",26990,4.3,88,90,128],
["Tablet","Redmi","Pad Series",19990,4.2,82,87,128],
["Tablet","Realme","Pad Series",17990,4.1,80,85,128],

# CAMERA
["Camera","Canon","EOS Series",64990,4.6,92,85,128],
["Camera","Sony","Alpha Series",79990,4.7,97,88,128],
["Camera","Nikon","Z Series",74990,4.6,94,87,128],
["Camera","Fujifilm","X Series",69990,4.7,93,89,128],
["Camera","Panasonic","Lumix Series",59990,4.4,88,86,128],
["Camera","GoPro","Hero Series",39990,4.5,90,92,128],

# MONITOR
["Monitor","Dell","UltraSharp Series",24990,4.6,91,80,0],
["Monitor","LG","UltraFine Series",22990,4.5,90,82,0],
["Monitor","Samsung","ViewFinity Series",26990,4.5,92,84,0],
["Monitor","ASUS","ProArt Series",29990,4.6,94,80,0],
["Monitor","Acer","Nitro Series",18990,4.4,91,78,0],
["Monitor","BenQ","GW Series",19990,4.5,88,81,0],
["Monitor","MSI","Optix Series",21990,4.4,93,79,0],
["Monitor","Lenovo","ThinkVision Series",20990,4.4,87,80,0],

# KEYBOARD
["Keyboard","Logitech","K Series",2999,4.5,84,0,0],
["Keyboard","HP","Wireless Keyboard",1999,4.3,78,0,0],
["Keyboard","Dell","KB Series",2499,4.3,80,0,0],
["Keyboard","ASUS","TUF Gaming",3999,4.4,89,0,0],
["Keyboard","Razer","BlackWidow",8999,4.6,95,0,0],
["Keyboard","Corsair","K Series",7999,4.6,94,0,0],
["Keyboard","Keychron","K Series",6999,4.6,92,0,0],
["Keyboard","Redragon","K Series",3499,4.4,88,0,0],

# MOUSE
["Mouse","Logitech","MX Master",7999,4.7,94,0,0],
["Mouse","HP","Wireless Mouse",1499,4.2,76,0,0],
["Mouse","Dell","MS Series",1999,4.3,79,0,0],
["Mouse","ASUS","TUF Gaming Mouse",2999,4.4,88,0,0],
["Mouse","Razer","DeathAdder",4999,4.6,94,0,0],
["Mouse","Corsair","Harpoon",3499,4.5,90,0,0],
["Mouse","Redragon","Gaming Mouse",1999,4.3,85,0,0],
["Mouse","Microsoft","Bluetooth Mouse",1799,4.3,80,0,0],

# TV
["TV","Samsung","Crystal Series",44990,4.5,91,90,0],
["TV","LG","UHD Series",42990,4.6,92,91,0],
["TV","Sony","Bravia Series",54990,4.7,96,91,0],
["TV","TCL","QLED Series",34990,4.4,88,89,0],
["TV","Xiaomi","Smart TV Series",29990,4.3,84,88,0],
["TV","Hisense","U Series",36990,4.4,89,90,0],
["TV","OnePlus","TV Series",31990,4.2,86,87,0],
["TV","Panasonic","4K Series",39990,4.3,87,89,0],

# SPEAKER
["Speaker","JBL","Flip Series",9999,4.6,91,90,0],
["Speaker","Sony","SRS Series",12999,4.6,93,91,0],
["Speaker","Bose","Smart Speaker",29990,4.7,96,89,0],
["Speaker","boAt","Stone Series",2999,4.2,78,88,0],
["Speaker","Marshall","Emberton",16990,4.7,95,90,0],
["Speaker","Anker","Soundcore Series",5999,4.4,86,92,0],

# MICROPHONE
["Microphone","FIFINE","USB Microphone",4999,4.4,84,0,0],
["Microphone","HyperX","QuadCast",12999,4.7,94,0,0],
["Microphone","Razer","Seiren Series",9999,4.5,90,0,0],
["Microphone","Logitech","Blue Series",8999,4.5,88,0,0],
["Microphone","Shure","MV Series",14999,4.7,96,0,0],
["Microphone","Audio-Technica","AT Series",11999,4.6,93,0,0],

# PRINTER
["Printer","HP","DeskJet Series",7999,4.3,80,0,0],
["Printer","Canon","PIXMA Series",8999,4.5,86,0,0],
["Printer","Epson","EcoTank Series",14999,4.6,91,0,0],
["Printer","Brother","Laser Series",13999,4.5,89,0,0],
["Printer","Samsung","Laser Series",12999,4.3,85,0,0],

# SSD
["SSD","Samsung","990 EVO",8999,4.7,96,0,1000],
["SSD","WD","Blue Series",7499,4.6,92,0,1000],
["SSD","Crucial","MX500",6999,4.5,88,0,1000],
["SSD","Kingston","NV2",6499,4.4,86,0,1000],
["SSD","SanDisk","SSD Plus",5999,4.3,82,0,1000],
["SSD","Seagate","FireCuda Series",9999,4.6,94,0,1000],

# POWER BANK
["Power Bank","Anker","PowerCore Series",2999,4.6,91,95,0],
["Power Bank","Ambrane","Powerbank Series",1499,4.3,82,90,0],
["Power Bank","boAt","Energy Series",1299,4.2,79,88,0],
["Power Bank","Xiaomi","Power Bank Series",1999,4.5,87,92,0],
["Power Bank","Samsung","Battery Pack",2999,4.5,89,93,0],
["Power Bank","Portronics","Power Plate",1399,4.2,80,89,0],

# ROUTER
["Router","TP-Link","Archer Series",2999,4.5,88,0,0],
["Router","ASUS","RT Series",6999,4.6,94,0,0],
["Router","Netgear","Nighthawk",8999,4.6,96,0,0],
["Router","D-Link","Wi-Fi Series",2499,4.3,82,0,0],
["Router","Tenda","AC Series",1999,4.2,80,0,0],
["Router","Xiaomi","Router Series",2999,4.4,86,0,0],

# SHOES
["Shoes","Nike","Pegasus Series",8999,4.6,93,0,0],
["Shoes","Adidas","Ultraboost",9999,4.6,92,0,0],
["Shoes","Puma","Running Series",4999,4.4,86,0,0],
["Shoes","ASICS","Gel Series",7999,4.6,94,0,0],
["Shoes","Skechers","Go Walk Series",5999,4.5,88,0,0],
["Shoes","New Balance","Fresh Foam",8999,4.6,93,0,0],
["Shoes","Reebok","Running Series",4499,4.3,84,0,0],

# BAG
["Bag","Wildcraft","Laptop Backpack",2499,4.4,84,0,0],
["Bag","American Tourister","College Backpack",2999,4.5,86,0,0],
["Bag","Samsonite","Travel Backpack",7999,4.6,92,0,0],
["Bag","Skybags","College Backpack",1999,4.3,80,0,0],
["Bag","Safari","Laptop Backpack",2199,4.3,82,0,0],
["Bag","Lenovo","Laptop Backpack",1799,4.2,78,0,0],

# AC
["Air Conditioner","Daikin","1.5 Ton Inverter",42990,4.6,93,92,0],
["Air Conditioner","LG","1.5 Ton DualCool",41990,4.6,92,91,0],
["Air Conditioner","Samsung","1.5 Ton Inverter",39990,4.5,90,90,0],
["Air Conditioner","Voltas","1.5 Ton Inverter",36990,4.4,86,89,0],
["Air Conditioner","Blue Star","1.5 Ton Inverter",38990,4.5,89,90,0],
["Air Conditioner","Panasonic","1.5 Ton Inverter",37990,4.4,88,91,0],
["Air Conditioner","Hitachi","1.5 Ton Inverter",40990,4.5,91,90,0],

# REFRIGERATOR
["Refrigerator","Samsung","Bespoke Series",49990,4.6,93,90,0],
["Refrigerator","LG","Double Door Series",45990,4.6,91,92,0],
["Refrigerator","Whirlpool","Double Door Series",39990,4.4,86,89,0],
["Refrigerator","Godrej","Double Door Series",37990,4.3,84,88,0],
["Refrigerator","Haier","Double Door Series",38990,4.4,87,90,0],
["Refrigerator","Bosch","Double Door Series",52990,4.6,94,91,0],

# WASHING MACHINE
["Washing Machine","LG","Top Load Series",32990,4.6,92,90,0],
["Washing Machine","Samsung","Top Load Series",31990,4.5,90,91,0],
["Washing Machine","Bosch","Front Load Series",39990,4.7,95,92,0],
["Washing Machine","Whirlpool","Top Load Series",27990,4.4,85,89,0],
["Washing Machine","IFB","Front Load Series",34990,4.5,91,91,0],
["Washing Machine","Godrej","Top Load Series",25990,4.2,82,88,0],
["Washing Machine","Haier","Front Load Series",29990,4.3,86,89,0],

# COFFEE MAKER
["Coffee Maker","Philips","Coffee Maker Series",5999,4.4,84,88,0],
["Coffee Maker","De'Longhi","Automatic Series",29990,4.7,95,90,0],
["Coffee Maker","Breville","Barista Series",49990,4.8,97,92,0],
["Coffee Maker","Morphy Richards","Coffee Maker",7999,4.3,82,86,0],
["Coffee Maker","Agaro","Imperial Series",6999,4.2,80,85,0],
["Coffee Maker","Prestige","Coffee Maker",3999,4.1,76,83,0],

# FITNESS
["Fitness Equipment","Decathlon","Exercise Cycle",11999,4.5,88,92,0],
["Fitness Equipment","Cult","Home Gym",19999,4.4,90,88,0],
["Fitness Equipment","Lifelong","Exercise Cycle",8999,4.3,82,90,0],
["Fitness Equipment","Reach","Exercise Bike",10999,4.4,85,91,0],
["Fitness Equipment","PowerMax","Fitness Series",14999,4.4,88,89,0],
["Fitness Equipment","Cockatoo","Fitness Series",9999,4.2,80,87,0],

# BICYCLE
["Bicycle","Hero","Sprint Series",12999,4.4,84,0,0],
["Bicycle","Hercules","Roadeo Series",15999,4.5,88,0,0],
["Bicycle","Firefox","Mountain Series",22999,4.6,93,0,0],
["Bicycle","Montra","Trance Series",19999,4.5,91,0,0],
["Bicycle","Schnell","MTB Series",24999,4.6,94,0,0],
["Bicycle","Ninety One","Drift Series",17999,4.4,89,0,0],
["Bicycle","Leader","MTB Series",10999,4.2,80,0,0],
["Bicycle","Ladybird","City Bike Series",9999,4.2,78,0,0],

# CAR ACCESSORIES
["Car Accessories","70mai","Dash Cam Series",7999,4.6,92,0,0],
["Car Accessories","DDPAI","Dash Cam Series",6999,4.5,89,0,0],
["Car Accessories","Portronics","Car Accessories",1999,4.2,78,0,0],
["Car Accessories","Philips","Car Accessories",2999,4.3,82,0,0],
["Car Accessories","Blaupunkt","Dash Cam Series",5999,4.4,86,0,0],
["Car Accessories","Qubo","Dash Cam Series",4999,4.3,84,0,0],

# TOYS
["Toys","LEGO","Technic Series",4999,4.7,94,0,0],
["Toys","Funskool","Educational Series",1499,4.4,82,0,0],
["Toys","Mattel","Educational Series",1999,4.5,86,0,0],
["Toys","Hasbro","Gaming Series",2499,4.5,87,0,0],
["Toys","Smartivity","STEM Series",1799,4.5,89,0,0],
["Toys","Hot Wheels","Car Series",999,4.4,81,0,0],

# BOOKS
["Books","O'Reilly","Programming Series",999,4.7,95,0,0],
["Books","Manning","Machine Learning Series",1299,4.7,94,0,0],
["Books","Packt","AI Programming Series",899,4.4,87,0,0],
["Books","Pearson","Computer Science Series",799,4.5,89,0,0],
["Books","McGraw Hill","Engineering Series",699,4.4,86,0,0],
["Books","Wiley","AI Reference Series",1099,4.6,92,0,0],

]


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    products,
    columns=[
        "Category",
        "Brand",
        "Model",
        "Price",
        "Rating",
        "Performance",
        "Battery",
        "Storage"
    ]
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ ShopShield AI")

    st.write(
        f"Welcome, **{st.session_state.user_name}**!"
    )

    st.markdown("---")

    st.subheader("🤖 Agent Pipeline")

    st.write("1️⃣ Requirement Agent")
    st.write("2️⃣ Product Agent")
    st.write("3️⃣ Comparison Agent")
    st.write("4️⃣ Budget Agent")
    st.write("5️⃣ Risk Agent")
    st.write("6️⃣ Regret Agent")
    st.write("7️⃣ Decision Agent")

    st.markdown("---")

    st.info(
        "Product images are retrieved using model-specific "
        "image searches. Prices and ratings are illustrative."
    )


# ============================================================
# DASHBOARD
# ============================================================

st.title("🛍️ Smart Shopping Dashboard")

st.write(
    "Compare multiple brands and models and find the product "
    "that best matches your budget."
)

st.markdown("---")


# ============================================================
# SEARCH
# ============================================================

col1, col2 = st.columns(2)

with col1:

    category = st.selectbox(
        "🛒 Select Product",
        sorted(df["Category"].unique())
    )

with col2:

    budget = st.number_input(
        "💰 Maximum Budget (₹)",
        min_value=500,
        max_value=1000000,
        value=30000,
        step=500
    )


requirement = st.text_area(
    "📝 What do you need?",
    placeholder="Example: good camera, battery, coding, gaming, lightweight..."
)


if st.button(
    "🔎 Analyze & Find Best Product",
    use_container_width=True
):

    # ========================================================
    # REQUIREMENT AGENT
    # ========================================================

    st.markdown("---")
    st.header("🤖 1. Requirement Agent")

    text = requirement.lower()

    detected = []

    keywords = {
        "battery": "🔋 Long battery life",
        "camera": "📷 Good camera",
        "performance": "⚡ High performance",
        "gaming": "🎮 Gaming performance",
        "storage": "💾 More storage",
        "lightweight": "🪶 Lightweight",
        "portable": "🎒 Portable",
        "coding": "💻 Coding",
        "programming": "💻 Programming",
        "student": "🎓 Student friendly",
        "college": "🎓 College use",
        "study": "📚 Study",
        "display": "🖥️ Good display",
        "sound": "🔊 Good sound",
        "wireless": "📡 Wireless",
        "fast": "⚡ Fast"
    }

    for key, value in keywords.items():

        if key in text:
            detected.append(value)

    if detected:

        for item in detected:
            st.success(item)

    else:

        st.info(
            "No specific requirement detected. "
            "ShopShield will compare products using budget, "
            "rating and performance."
        )


    # ========================================================
    # PRODUCT AGENT
    # ========================================================

    st.header("🛍️ 2. Product Agent")

    category_products = df[
        df["Category"] == category
    ].copy()

    affordable = category_products[
        category_products["Price"] <= budget
    ].copy()

    if len(affordable) == 0:

        st.error(
            "No product is available within this budget."
        )

        st.stop()

    st.success(
        f"{len(affordable)} brand/model options found."
    )


    # ========================================================
    # COMPARISON AGENT
    # ========================================================

    st.header("⚖️ 3. Comparison Agent")

    affordable["Budget Used (%)"] = (
        affordable["Price"] / budget * 100
    )

    affordable["Budget Score"] = (
        100 - affordable["Budget Used (%)"]
    ).clip(lower=0)

    affordable["ShopShield Score"] = (
        (affordable["Rating"] / 5) * 30
        + affordable["Performance"] * 0.35
        + affordable["Battery"] * 0.10
        + affordable["Budget Score"] * 0.25
    ).round(1)

    affordable = affordable.sort_values(
        "ShopShield Score",
        ascending=False
    ).reset_index(drop=True)

    affordable.insert(
        0,
        "Rank",
        range(1, len(affordable) + 1)
    )


    # ========================================================
    # PRODUCT CARDS
    # ========================================================

    st.subheader("📸 Products Compared")

    for i, row in affordable.iterrows():

        product_image = get_product_image(
            row["Brand"],
            row["Model"],
            row["Category"]
        )

        with st.container():

            col1, col2, col3 = st.columns([1.2, 2.5, 1])

            with col1:

                st.image(
                    product_image,
                    use_container_width=True
                )

            with col2:

                st.markdown(
                    f"### #{row['Rank']} {row['Brand']} {row['Model']}"
                )

                st.write(
                    f"⭐ Rating: **{row['Rating']}/5**"
                )

                st.write(
                    f"⚡ Performance: **{row['Performance']}/100**"
                )

                if row["Battery"] > 0:
                    st.write(
                        f"🔋 Battery: **{row['Battery']}/100**"
                    )

                if row["Storage"] > 0:
                    st.write(
                        f"💾 Storage: **{row['Storage']} GB**"
                    )

            with col3:

                st.metric(
                    "Price",
                    f"₹{row['Price']:,.0f}"
                )

                st.metric(
                    "Score",
                    f"{row['ShopShield Score']}/100"
                )

            st.markdown("---")


    # ========================================================
    # BEST PRODUCT
    # ========================================================

    best = affordable.iloc[0]

    best_image = get_product_image(
        best["Brand"],
        best["Model"],
        best["Category"]
    )

    st.header("🏆 Best Match")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.image(
            best_image,
            use_container_width=True
        )

    with col2:

        st.success(
            f"🏆 **{best['Brand']} {best['Model']}**"
        )

        st.write(
            f"### ₹{best['Price']:,.0f}"
        )

        st.write(
            f"⭐ Rating: **{best['Rating']}/5**"
        )

        st.write(
            f"⚡ Performance: **{best['Performance']}/100**"
        )

        st.write(
            f"🏅 ShopShield Score: "
            f"**{best['ShopShield Score']}/100**"
        )


    # ========================================================
    # BUDGET AGENT
    # ========================================================

    st.header("💰 4. Budget Agent")

    price = best["Price"]

    used = price / budget * 100

    remaining = budget - price

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Product Price",
            f"₹{price:,.0f}"
        )

    with c2:
        st.metric(
            "Budget Used",
            f"{used:.1f}%"
        )

    with c3:
        st.metric(
            "Remaining",
            f"₹{remaining:,.0f}"
        )

    st.progress(
        min(used / 100, 1)
    )


    # ========================================================
    # RISK AGENT
    # ========================================================

    st.header("🛡️ 5. Risk Agent")

    risks = []

    if used > 85:
        risks.append(
            "⚠️ This product uses most of your budget."
        )

    if best["Rating"] < 4.2:
        risks.append(
            "⚠️ Rating is relatively low."
        )

    if best["Performance"] < 70:
        risks.append(
            "⚠️ Performance score is relatively low."
        )

    if risks:

        for risk in risks:
            st.warning(risk)

    else:

        st.success(
            "✅ No major prototype risks detected."
        )


    # ========================================================
    # REGRET AGENT
    # ========================================================

    st.header("😟 6. Buyer Regret Agent")

    regret = (
        used * 0.55
        + (5 - best["Rating"]) * 12
    )

    regret = max(
        0,
        min(100, regret)
    )

    regret = round(regret)

    if regret <= 30:
        regret_level = "🟢 LOW"

    elif regret <= 60:
        regret_level = "🟡 MEDIUM"

    else:
        regret_level = "🔴 HIGH"


    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Buyer Regret Score",
            f"{regret}/100"
        )

    with c2:
        st.metric(
            "Risk Level",
            regret_level
        )

    st.caption(
        "Prototype estimate based mainly on budget usage and rating. "
        "It is not a scientifically validated prediction."
    )


    # ========================================================
    # DECISION AGENT
    # ========================================================

    st.header("🧠 7. Decision Agent")

    score = best["ShopShield Score"]

    if score >= 80 and regret <= 40:

        decision = "🟢 BUY"

        message = (
            "Strong overall match with good value and manageable risk."
        )

    elif score >= 65 and regret <= 65:

        decision = "🟡 CONSIDER"

        message = (
            "Good option, but compare alternatives before purchasing."
        )

    else:

        decision = "🔴 AVOID"

        message = (
            "The product does not provide a strong enough "
            "value-risk balance."
        )


    st.subheader(decision)

    st.write(message)


    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    st.markdown("---")

    st.header("🎯 Final ShopShield Recommendation")

    st.success(
        f"""
🏆 **{best['Brand']} {best['Model']}**

💰 Price: ₹{best['Price']:,.0f}

⭐ Rating: {best['Rating']}/5

📊 ShopShield Score: {best['ShopShield Score']}/100

😟 Buyer Regret Score: {regret}/100

🎯 Final Decision: {decision}
"""
    )


    # ========================================================
    # PIPELINE
    # ========================================================

    st.markdown("---")

    st.header("🔗 Agentic Decision Pipeline")

    st.write(
        "👤 User Requirement"
        " → 🤖 Requirement Agent"
        " → 🛍️ Product Agent"
        " → ⚖️ Comparison Agent"
        " → 💰 Budget Agent"
        " → 🛡️ Risk Agent"
        " → 😟 Regret Agent"
        " → 🧠 Decision Agent"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🛡️ ShopShield AI | Agentic Shopping Guardian | "
    "Model-specific image search | Illustrative product data"
)