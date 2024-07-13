from flask import render_template, redirect, url_for, request, flash, jsonify

from os import path
from forms import AddItemForm, RegistrationForm, LoginForm, CommentForm, CardForm, BasketForm
from ext import app, login_manager
from models import db, Guitar, Bass, Keyboard, Microphone, Accessory, User, Comment, Card, Basket
from flask_login import login_user, logout_user, login_required, current_user

role = "Guest"



@app.route("/")
def home():
    return render_template("index.html", guitars=Guitar)

@app.route("/guitar")
def show_guitars():
    guitars = Guitar.query.all()
    return render_template("guitars.html", guitars=guitars)



@app.route('/guitar/<int:guitar_id>')
def guitar_detail(guitar_id):
    guitar = Guitar.query.get_or_404(guitar_id)
    comments = Comment.query.filter_by(product_id=guitar_id, product_type='guitar').all()
    form = BasketForm()  # Define your form here if it's needed

    return render_template("guitars.details.html", guitar=guitar, comments=comments, form=form)
@app.route("/basses")
def show_basses():
    basses = Bass.query.all()
    return render_template("bass.html", basses=basses)

@app.route('/bass/<int:bass_id>')
def bass_detail(bass_id):
    bass = Bass.query.get(bass_id)
    if bass:
        comments = Comment.query.filter_by(product_id=bass_id, product_type='bass').all()
        return render_template("bass.details.html", bass=bass, comments=comments)
    else:
        return "Bass not found", 404


@app.route("/keyboards")
def show_keyboards():
    keyboards = Keyboard.query.all()
    return render_template("keyboard.html", keyboards=keyboards)

@app.route("/keyboard/<int:keyboard_id>")
def keyboard_detail(keyboard_id):
    keyboard = Keyboard.query.get(keyboard_id)
    if keyboard:
        comments = Comment.query.filter_by(product_id=keyboard_id, product_type='keyboard').all()
        return render_template("keyboard.details.html", keyboard=keyboard, comments=comments)
    else:
        return "Keyboard not found", 404

@app.route("/microphones")
def show_microphones():
    microphones = Microphone.query.all()
    return render_template("microphone.html", microphones=microphones)



@app.route("/microphone/<int:microphone_id>")
def microphone_detail(microphone_id):
    microphone = Microphone.query.get(microphone_id)
    if microphone:
        comments = Comment.query.filter_by(product_id=microphone_id, product_type='microphone').all()
        return render_template("microphone.details.html", microphone=microphone, comments=comments)
    else:
        return "Microphone not found", 404

@app.route("/accessories")
def show_accessories():
    accessories = Accessory.query.all()
    return render_template("accessory.html", accessories=accessories)

@app.route("/accessory/<int:accessory_id>")
def accessory_detail(accessory_id):
    accessory = Accessory.query.get(accessory_id)
    if accessory:
        comments = Comment.query.filter_by(product_id=accessory_id, product_type='accessory').all()
        return render_template("accessory.details.html", accessory=accessory, comments=comments)
    else:
        return "Accessory not found", 404



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Directly compare the plain text password
            login_user(user, remember=form.remember.data)
            flash('Login successful.', 'success')
            return redirect(url_for('home'))  # Replace 'home' with your actual home route
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if current_user.role != 'Admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    form = AddItemForm()
    if form.validate_on_submit():
        category = form.category.data
        name = form.name.data
        price = form.price.data
        img = form.img.data
        item_id = form.id.data

        if category == 'guitar':
            new_item = Guitar(id=item_id, name=name, price=price, img=img)
        elif category == 'bass':
            new_item = Bass(id=item_id, name=name, price=price, img=img)
        elif category == 'keyboard':
            new_item = Keyboard(id=item_id, name=name, price=price, img=img)
        elif category == 'microphone':
            new_item = Microphone(id=item_id, name=name, price=price, img=img)
        elif category == 'accessory':
            new_item = Accessory(id=item_id, name=name, price=price, img=img)

        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully.', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding item: {str(e)}', 'danger')
            return render_template('add_item.html', form=form)

    return render_template('add_item.html', form=form)


@app.route('/submit_comment/<int:product_id>/<product_type>', methods=['POST'])
def submit_comment(product_id, product_type):
    text = request.form.get('comment_text')

    # Ensure the product type is valid and retrieve the product
    if product_type == 'guitar':
        product = Guitar.query.get_or_404(product_id)
        endpoint = 'guitar_detail'
    elif product_type == 'bass':
        product = Bass.query.get_or_404(product_id)
        endpoint = 'bass_detail'
    elif product_type == 'keyboard':
        product = Keyboard.query.get_or_404(product_id)
        endpoint = 'keyboard_detail'
    elif product_type == 'microphone':
        product = Microphone.query.get_or_404(product_id)
        endpoint = 'microphone_detail'
    elif product_type == 'accessory':
        product = Accessory.query.get_or_404(product_id)
        endpoint = 'accessory_detail'
    else:
        return "Invalid product type", 400

    # Create new comment
    new_comment = Comment(product_id=product_id, product_type=product_type, text=text)

    try:
        db.session.add(new_comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Error adding comment', 'danger')
        return redirect(url_for(endpoint, **{f'{product_type}_id': product_id}))

    return redirect(url_for(endpoint, **{f'{product_type}_id': product_id}))




@app.route('/add_card/<int:product_id>/<string:product_type>', methods=['GET', 'POST'])
def add_card(product_id, product_type):
    form = CardForm()
    if form.validate_on_submit():
        card = Card(
            account_number=form.account_number.data,
            address=form.address.data,
            phone_number=form.phone_number.data
        )
        db.session.add(card)
        db.session.commit()

        Basket.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()


        flash('Card details added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add_card.html', form=form, product_id=product_id, product_type=product_type)

@app.route('/add_to_basket/<product_type>/<int:product_id>', methods=['POST'])
@login_required
def add_to_basket(product_type, product_id):
    # Retrieve quantity from form
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if quantity is not provided or invalid

    # Determine the product type and retrieve the corresponding item from the database
    if product_type == 'guitar':
        product = Guitar.query.get_or_404(product_id)
        endpoint = 'guitar_detail'
    elif product_type == 'bass':
        product = Bass.query.get_or_404(product_id)
        endpoint = 'bass_detail'
    elif product_type == 'keyboard':
        product = Keyboard.query.get_or_404(product_id)
        endpoint = 'keyboard_detail'
    elif product_type == 'microphone':
        product = Microphone.query.get_or_404(product_id)
        endpoint = 'microphone_detail'
    elif product_type == 'accessory':
        product = Accessory.query.get_or_404(product_id)
        endpoint = 'accessory_detail'
    else:
        flash('Invalid product type', 'error')
        return redirect(url_for('home'))

    # Check if the item is already in the basket
    basket_item = Basket.query.filter_by(
        user_id=current_user.id,
        product_id=product_id,
        product_type=product_type
    ).first()

    if basket_item:
        # If the item is already in the basket, update the quantity
        basket_item.quantity += quantity
    else:
        # Create a new basket item
        basket_item = Basket(
            user_id=current_user.id,
            product_id=product_id,
            product_type=product_type,
            quantity=quantity  # Set quantity from form
        )
        db.session.add(basket_item)

    try:
        db.session.commit()
        flash(f'{product_type.capitalize()} added to basket', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding to basket', 'danger')

    return redirect(url_for(endpoint, **{f'{product_type}_id': product_id}))


# Route for viewing basket

@app.route('/basket/<int:user_id>')
@login_required
def view_basket(user_id):
    basket_items = Basket.query.filter_by(user_id=user_id).all()
    detailed_items = []
    total_price = 0

    for item in basket_items:
        product = None
        if item.product_type == 'guitar':
            product = Guitar.query.get(item.product_id)
        elif item.product_type == 'bass':
            product = Bass.query.get(item.product_id)
        elif item.product_type == 'keyboard':
            product = Keyboard.query.get(item.product_id)
        elif item.product_type == 'microphone':
            product = Microphone.query.get(item.product_id)
        elif item.product_type == 'accessory':
            product = Accessory.query.get(item.product_id)

        if product:
            detailed_item = {
                'basket_item': item,
                'product': product,
                'image_src': url_for('static', filename=product.img)
            }
            total_price += product.price * item.quantity
            detailed_items.append(detailed_item)

    return render_template('basket.html', basket_items=detailed_items, total_price=total_price)





@app.route('/remove_from_basket/<product_type>/<int:product_id>', methods=['POST'])
@login_required
def remove_from_basket(product_type, product_id):
    basket_item = Basket.query.filter_by(
        user_id=current_user.id,
        product_type=product_type,
        product_id=product_id
    ).first_or_404()

    db.session.delete(basket_item)
    db.session.commit()

    flash(f'{product_type.capitalize()} removed from basket', 'success')
    return redirect(url_for('view_basket', user_id=current_user.id))





