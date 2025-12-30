import gradio as gr
import pandas as pd
import requests
from supabase import create_client, Client

# --- 1. CONFIGURATION & CREDENTIALS ---
# Supabase Secrets
SUPABASE_URL = "https://fdpvzupvueiagjtnhzwz.supabase.co"
SUPABASE_KEY = "sb_publishable_Pd_v8ertyBownbj07IdYjA_40JZLJRk"

# GitHub Assets
LOGO_URL = "https://raw.githubusercontent.com/KaranKool/mishtee-magic/refs/heads/main/mishTee_logo.png"
STYLE_PY_URL = "https://raw.githubusercontent.com/KaranKool/mishtee-magic/refs/heads/main/style.py"

# Initialize Database Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. ASSET HELPERS ---
def fetch_branding_style():
    """
    Fetches the custom CSS variable 'mishtee_css' from the remote style.py file.
    """
    fallback_css = ".gradio-container {background-color: #FAF9F6;}"
    try:
        response = requests.get(STYLE_PY_URL)
        if response.status_code == 200:
            namespace = {}
            exec(response.text, namespace)
            return namespace.get('mishtee_css', fallback_css)
    except Exception as e:
        print(f"Style fetch failed: {e}")
    return fallback_css

# Load Styles Immediately
app_css = fetch_branding_style()


# --- 3. DATABASE LOGIC ---
def get_customer_history(phone_number):
    """
    Retrieves customer name and order history based on phone number.
    """
    if not phone_number:
        return "Please enter a valid phone number.", pd.DataFrame()
    
    try:
        # A. Fetch Customer Name
        cust_response = supabase.table('customers')\
            .select('full_name')\
            .eq('phone', phone_number)\
            .execute()
            
        if not cust_response.data:
            return "Welcome! We don't have a record of this number yet.", pd.DataFrame()

        name = cust_response.data[0]['full_name']
        greeting = f"## Namaste, {name} ji! Great to see you again."

        # B. Fetch Orders
        orders_response = supabase.table('orders')\
            .select('order_id, order_date, status, qty_kg, order_value_inr, products(sweet_name, variant_type)')\
            .eq('cust_phone', phone_number)\
            .order('order_date', desc=True)\
            .execute()

        data = orders_response.data
        if not data:
            return greeting, pd.DataFrame(columns=["Date", "Sweet", "Variant", "Qty (Kg)", "Total (₹)", "Status"])

        # C. Format Data
        clean_rows = []
        for row in data:
            prod = row.get('products', {}) or {}
            clean_rows.append({
                "Date": row['order_date'],
                "Sweet": prod.get('sweet_name', 'Unknown'),
                "Variant": prod.get('variant_type', '-'),
                "Qty (Kg)": row['qty_kg'],
                "Total (₹)": row['order_value_inr'],
                "Status": row['status']
            })
            
        return greeting, pd.DataFrame(clean_rows)

    except Exception as e:
        return f"System Error: {str(e)}", pd.DataFrame()

def get_trending_products():
    """
    Calculates top 4 best-selling products.
    """
    try:
        # A. Fetch all orders (simplistic aggregation)
        response = supabase.table('orders').select('product_id, qty_kg').execute()
        if not response.data:
            return pd.DataFrame()

        df = pd.DataFrame(response.data)
        # B. Group by Product ID and Sum Quantity
        trending = df.groupby('product_id')['qty_kg'].sum().reset_index()
        trending = trending.sort_values(by='qty_kg', ascending=False).head(4)
        
        if trending.empty:
             return pd.DataFrame()

        # C. Get Product Details
        top_ids = trending['product_id'].tolist()
        prod_res = supabase.table('products')\
            .select('item_id, sweet_name, variant_type, price_per_kg')\
            .in_('item_id', top_ids)\
            .execute()
        
        products_map = {p['item_id']: p for p in prod_res.data}
        
        # D. Format Final Table
        final_rows = []
        for _, row in trending.iterrows():
            pid = row['product_id']
            details = products_map.get(pid, {})
            final_rows.append({
                "Sweet Name": details.get('sweet_name', 'Unknown'),
                "Variant": details.get('variant_type', '-'),
                "Price / Kg": f"₹{details.get('price_per_kg', 0)}",
                "Total Kgs Sold": f"{row['qty_kg']} kg"
            })
            
        return pd.DataFrame(final_rows)

    except Exception as e:
        print(f"Trending Error: {e}")
        return pd.DataFrame()

def app_login_logic(phone):
    """
    Wrapper to trigger both functions on button click.
    """
    greeting, history_df = get_customer_history(phone)
    trending_df = get_trending_products()
    return greeting, history_df, trending_df


# --- 4. GRADIO INTERFACE CONSTRUCTION ---
with gr.Blocks(css=app_css, title="MishTee-Magic") as demo:
    
    # --- HEADER SECTION ---
    with gr.Row(elem_classes=["center-content"]):
        with gr.Column(scale=1):
            # HTML Logo
            gr.HTML(f"""
            <div style="text-align: center; margin-top: 25px; margin-bottom: 10px;">
                <img src="{LOGO_URL}" alt="MishTee Magic" style="max-width: 220px; height: auto; display: block; margin: 0 auto;">
            </div>
            """)
            # Slogan
            gr.Markdown(
                """
                <div style="text-align: center; font-size: 1.1em; letter-spacing: 2px; color: #C06C5C; text-transform: uppercase;">
                Purity and Health
                </div>
                """
            )

    # --- LOGIN SECTION ---
    with gr.Row():
        with gr.Column(scale=1): pass # Spacer
        with gr.Column(scale=2):
            with gr.Group():
                gr.Markdown("### Client Access")
                phone_input = gr.Textbox(
                    placeholder="Enter your registered mobile number (e.g. 9876543210)", 
                    label="Phone Number", 
                    show_label=False
                )
                login_btn = gr.Button("View My Dashboard")
                
                # Dynamic Greeting Output
                greeting_output = gr.Markdown(value="")
        with gr.Column(scale=1): pass # Spacer

    gr.HTML("<hr style='margin: 30px 0; border-top: 1px solid #E0E0E0;'>")

    # --- DATA DISPLAY SECTION ---
    with gr.Tabs():
        # TAB 1: TRENDING (Default View)
        with gr.TabItem("Trending Today"):
            gr.Markdown("### The Saffron Collection: Most Loved")
            trending_table = gr.Dataframe(
                headers=["Sweet Name", "Variant", "Price / Kg", "Total Kgs Sold"],
                interactive=False,
                wrap=True
            )
            
        # TAB 2: HISTORY
        with gr.TabItem("My Order History"):
            gr.Markdown("### Your Past Indulgences")
            history_table = gr.Dataframe(
                headers=["Date", "Sweet", "Variant", "Qty (Kg)", "Total (₹)", "Status"],
                interactive=False,
                wrap=True
            )

    # --- EVENT LISTENERS ---
    # When button is clicked, update Greeting, History Table, and Trending Table
    login_btn.click(
        fn=app_login_logic,
        inputs=[phone_input],
        outputs=[greeting_output, history_table, trending_table]
    )
    
    # Also load trending items on app launch (optional, creates a nice default state)
    demo.load(fn=get_trending_products, outputs=trending_table)

if __name__ == "__main__":
    demo.launch()
