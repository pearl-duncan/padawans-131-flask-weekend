from app import app

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, BookForm 
from .models import db, User, Book

@app.route("/")
def index():
    return render_template("index.j2")

    
    
@app.route("/register", methods=["GET","POST"])
def register_page():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            
            new_user = User(email=email, password=password)
            new_user.save()
            
            return redirect(url_for('login_page'))

        else:
            return render_template("register.j2", form=form)
    else:
        return render_template("register.j2", form=form)


@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            
            user = User.query.filter_by(email=email).first()
            if not user:
                return render_template("login.j2", form=form)
            else:       
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for('books_page'))
                else:
                    return render_template("login.j2", form=form)
        else:
            return render_template("login.j2", form=form)
    else:
        return render_template("login.j2", form=form) 
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_page'))
    
@app.route("/books", methods=["GET","POST"])
@login_required
def books_page():
    form = BookForm()
    
    if request.method == "POST":
        if form.validate():
            name = form.name.data
            author = form.author.data

            new_book = Book(name=name, author=author, user_id=current_user.id) 
            new_book.save()

    books = Book.query.filter_by(user_id=current_user.id).all()

    return render_template("books.j2", form=form, books=books)