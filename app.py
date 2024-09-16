import streamlit as st
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Function to create PDF invoice
def create_invoice_pdf(invoice_data, filename, template_name):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_name)
    html_out = template.render(invoice_data)
    HTML(string=html_out).write_pdf(filename)

# Streamlit app
st.title("Proforma Invoice Generator")

st.subheader("Create Proforma Invoice")
# Form to create proforma invoice
with st.form(key='proforma_invoice_form'):
    # Company and Invoice Details
    company_name = st.text_input("Company Name")
    company_address = st.text_input("Company Address")
    company_mobile = st.text_input("Company Mobile Number")
    company_gst = st.text_input("Company GST Number")
    invoice_number = st.text_input("Proforma Invoice Number")
    date = st.date_input("Invoice Date")
    due_date = st.date_input("Valid Until")

    # Shipping Details
    shipping_company_address = st.text_input("Shipping Company Address")

    # Item Details
    num_items = st.number_input("Number of Items", min_value=1, step=1)
    items = []
    for i in range(num_items):
        item_name = st.text_input(f"Item {i+1} Name", key=f'proforma_item_name_{i}')
        item_hsn = st.text_input(f"Item {i+1} HSN Code", key=f'proforma_item_hsn_{i}')
        item_quantity = st.number_input(f"Item {i+1} Quantity", min_value=1, step=1, key=f'proforma_item_quantity_{i}')
        item_uom = st.text_input(f"Item {i+1} UOM", key=f'proforma_item_uom_{i}')
        item_price = st.number_input(f"Item {i+1} Unit Price", min_value=0.0, key=f'proforma_item_price_{i}')
        item_total = item_quantity * item_price
        items.append({'name': item_name, 'hsn': item_hsn, 'quantity': item_quantity, 'uom': item_uom, 'price': f'{item_price:.2f}', 'total': f'{item_total:.2f}'})
    
    # Tax and Discount
    cgst = st.number_input("CGST (%)", min_value=0.0, step=0.1)
    sgst = st.number_input("SGST (%)", min_value=0.0, step=0.1)
    discount = st.number_input("Discount (%)", min_value=0.0, step=0.1)

    # Additional Costs
    material_loading_cost = st.number_input("Material Loading Cost", min_value=0.0, step=0.1)
    transportational_cost = st.number_input("Transportational Cost", min_value=0.0, step=0.1)

    submit_button = st.form_submit_button(label='Create Proforma Invoice')

if submit_button:
    subtotal = sum(float(item['total']) for item in items)
    cgst_amount = subtotal * cgst / 100
    sgst_amount = subtotal * sgst / 100
    discount_amount = subtotal * discount / 100

    # Calculating total and rounding off
    total = subtotal + cgst_amount + sgst_amount - discount_amount + material_loading_cost + transportational_cost
    total = round(total)

    # Preparing invoice data
    invoice_data = {
        'invoice_number': invoice_number,
        'date': date.strftime('%Y-%m-%d'),
        'due_date': due_date.strftime('%Y-%m-%d'),
        'company_name': company_name,
        'company_address': company_address,
        'company_mobile': company_mobile,
        'company_gst': company_gst,
        'shipping_company_address': shipping_company_address,
        'items': items,
        'subtotal': f'{subtotal:.2f}',
        'cgst': cgst,
        'cgst_amount': f'{cgst_amount:.2f}',
        'sgst': sgst,
        'sgst_amount': f'{sgst_amount:.2f}',
        'discount': discount,
        'discount_amount': f'{discount_amount:.2f}',
        'material_loading_cost': f'{material_loading_cost:.2f}',
        'transportational_cost': f'{transportational_cost:.2f}',
        'total': f'{total:.2f}'
    }

    create_invoice_pdf(invoice_data, "proforma_invoice.pdf", 'proforma_invoice_template.html')
    st.success("Proforma Invoice created successfully!")
    st.download_button('Download Proforma Invoice', data=open('proforma_invoice.pdf', 'rb'), file_name='proforma_invoice.pdf')
