from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)

def initDB():
    conn = sql.connect('database.db')
    print("Opened database successfully")   
    conn.execute('''CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ad_number TEXT,
        description TEXT,
        price REAL,
        city TEXT,
        image TEXT,
        category TEXT,
        sub_category TEXT
    );''')
    print("Table created successfully")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ads")
    if cursor.fetchone()[0] == 0:
        ads = [
            ('Toyota Corolla', 'AD001', 'A reliable and fuel-efficient sedan.', 20000, 'Ankara', 'static/images/day-exterior-04_785.png', 'Vehicle', 'Automobile'),
            ('Jeep Wrangler', 'AD002', 'Perfect for off-road adventures.', 35000, 'Istanbul', 'static/images/JEEP-WRANGLER-SAHARA-MY25-PHEV-BLACK-FIGURINES.png', 'Vehicle', 'Off-Road, SUV, & Pickup'),
            ('Luxury Villa', 'AD003', 'Spacious villa with a sea view.', 500000, 'Antalya', 'static/images/Luxury-Villa-Izmir-Turkish-Rivie.png', 'Estate', 'Residence'),
            ('Downtown Office', 'AD004', 'Modern office space in the city center.', 120000, 'Izmir', 'static/images/houston-downtown-office-03jpg.png', 'Estate', 'Workplace'),
            ('Farmland', 'AD005', 'Perfect for agricultural purposes.', 80000, 'Bursa', 'static/images/3435a010b919179736bb326768dd813f.png', 'Estate', 'Land'),
            ('Honda Civic', 'AD006', 'A compact car with excellent features.', 18000, 'Konya', 'static/images/x5_1215292231e19.png', 'Vehicle', 'Automobile'),
            ('Ford Ranger', 'AD007', 'Durable and versatile pickup truck.', 30000, 'Adana', 'static/images/552227f577eea17e45aa3b5e96df60ef.png', 'Vehicle', 'Off-Road, SUV, & Pickup'),
            ('City Apartment', 'AD008', 'Cozy apartment in the heart of the city.', 250000, 'Mersin', 'static/images/Altinyildiz.png', 'Estate', 'Residence'),
            ('Workshop', 'AD009', 'Ideal for a small manufacturing business.', 95000, 'Gaziantep', 'static/images/engineering-workshop-at-the-rail.png', 'Estate', 'Workplace'),
            ('Residential Land', 'AD010', 'Ready to build your dream home.', 70000, 'Trabzon', 'static/images/StockImage_Aerial_view_of_a_resi.png', 'Estate', 'Land'),
            ('Shanty House', 'AD011', 'If you really do not have any money...', 500, 'Istanbul', 'static/images/8474245714_d5db70de35_b.png', 'Estate', 'Residence'),
            ('Tesla Model Y', 'AD012', 'The latest technology electric car.', 50000, 'Izmir', 'static/images/GUID-1F2D8746-336F-4CF9-9A04-F35E960F31FE-online-en-US.png', 'Vehicle', 'Automobile')
        ]
        
        conn.executemany('INSERT INTO ads (name, ad_number, description, price, city, image, category, sub_category) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ads)
        print("Initial records inserted successfully")
    else:
        print("Database already contains data, skipping initial insert.")
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    
    if search_query:
        cursor.execute("""
            SELECT * FROM ads 
            WHERE LOWER(name) LIKE ? OR
                  LOWER(ad_number) LIKE ? OR
                  LOWER(description) LIKE ? OR
                  LOWER(city) LIKE ? OR
                  LOWER(category) LIKE ? OR
                  LOWER(sub_category) LIKE ? OR
                  CAST(price AS TEXT) LIKE ?""",
                       tuple([f"%{search_query}%"] * 7))
    else:
        cursor.execute("SELECT * FROM ads")
    
    ads = cursor.fetchall()

    category_counts = {}
    for ad in ads:
        main_category = ad["category"]
        sub_category = ad["sub_category"]

        key = f"{main_category}, {sub_category}" if sub_category else main_category
        if key in category_counts:
            category_counts[key] += 1
        else:
            category_counts[key] = 1

        if main_category in category_counts:
            category_counts[main_category] += 1
        else:
            category_counts[main_category] = 1

    conn.close()
    return render_template('home.html', ads=ads, category_counts=category_counts, search_query=search_query)


@app.route('/item/<int:item_id>')
def item_detail(item_id):
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads WHERE id = ?", (item_id,))
    ad = cursor.fetchone()
    conn.close()
    return render_template('itempage.html', ad=ad)


if __name__ == '__main__':
    initDB()
    app.run(debug=True)
