import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Automatically install required libraries
try:
    subprocess.check_output(["pip", "install", "Flask==2.0.1"])
except subprocess.CalledProcessError as e:
    print("Error installing Flask:", e.output)

# Sample eBook data with quantity property
ebooks = [
    {"id": 1, "title": "The Great Gatsby", "price": 10.99, "quantity": 1, "image": "images/ebook1.jpg", "description": "Set in the roaring 1920s, this classic novel explores themes of wealth, love, and the American Dream. F. Scott Fitzgerald's masterful storytelling captures the decadence and disillusionment of the Jazz Age."},
    {"id": 2, "title": "Sapiens: A Brief History of Humankind", "price": 8.99, "quantity": 1, "image": "images/ebook2.jpg", "description": "Yuval Noah Harari takes readers on a captivating journey through the history of our species, exploring the cognitive, agricultural, and scientific revolutions that shaped human civilization. A thought-provoking exploration of our shared past."},
    {"id": 3, "title": "The Hitchhiker's Guide to the Galaxy", "price": 12.99, "quantity": 1, "image": "images/ebook3.jpg", "description": "Join Arthur Dent as he embarks on a hilarious and absurd intergalactic journey after Earth's unexpected destruction. Douglas Adams' sci-fi comedy is a cult classic, known for its wit and satirical take on the universe."},
    ]



# Shopping cart (a dictionary where keys are book IDs and values are quantities)
cart = {}

@app.route("/")
def index():
    return render_template("index.html", ebooks=ebooks)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    ebook_id = int(request.form.get("ebook_id"))
    if ebook_id in cart:
        cart[ebook_id] += 1  # Increase quantity if book is already in the cart
    else:
        cart[ebook_id] = 1  # Add the book to the cart with a quantity of 1
    return redirect(url_for("index"))

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    ebook_id = int(request.form.get("ebook_id"))
    if ebook_id in cart:
        if cart[ebook_id] > 1:
            cart[ebook_id] -= 1  # Decrease quantity if more than 1
        else:
            del cart[ebook_id]  # Remove the book from the cart if only 1 left
    return redirect(url_for("view_cart"))

@app.route("/cart")
def view_cart():
    cart_items = []
    for ebook in ebooks:
        ebook_id = ebook["id"]
        if ebook_id in cart:
            cart_items.append({"book": ebook, "quantity": cart[ebook_id]})
    return render_template("cart.html", cart_items=cart_items)

@app.route("/update_cart", methods=["POST"])
def update_cart():
    to_remove = []  # Create a list to store items to be removed
    for ebook in ebooks:
        ebook_id = ebook["id"]
        quantity_field_name = f"quantity_{ebook_id}"
        new_quantity = request.form.get(quantity_field_name)
        
        # Check if new_quantity is not None and is convertible to an integer
        if new_quantity is not None and new_quantity.isdigit():
            new_quantity = int(new_quantity)
            if new_quantity > 0:
                cart[ebook_id] = new_quantity
            else:
                to_remove.append(ebook_id)
    
    # Remove items with quantity zero
    for ebook_id in to_remove:
        del cart[ebook_id]

    return redirect(url_for("view_cart"))

@app.route("/checkout")
def checkout():
    total_price = sum(ebook["price"] * cart[ebook["id"]] for ebook in ebooks if ebook["id"] in cart)
    return render_template("checkout.html", total_price=total_price)

@app.route("/purchase", methods=["POST"])
def purchase():
    # Here, you can implement the purchase logic, e.g., handle payment processing
    # For this example, let's clear the cart as a placeholder.
    cart.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
