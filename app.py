from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import requests
from data_base import create_table_users



app = Flask(__name__)
app.secret_key = '123'

create_table_users()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()
        conn.close()

        if existing_user:
            error_message = "Пользователь с таким адресом электронной почты уже существует."
            return render_template('register.html', error_message=error_message)
        else:
            # Если пользователь с таким адресом электронной почты не существует, добавляем его в базу данных
            conn = sqlite3.connect('recipes.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))

# Выход пользователя
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')


def get_recipes():
    query = request.args.get('q', '')
    if query != '':
        query = f'/search?q={query}'
    url = f'https://dummyjson.com/recipes{query}'
    response = requests.get(url)
    print("get_recipes")
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data['recipes']
    else:
        print('Ошибка при получении рецептов:', response.status_code)
        return None


@app.route('/main_page')
def main_page():
    print("main_page")
    recipes = get_recipes()

    return render_template('main_page.html', recipes=recipes)


def get_recipe_by_id(recipe_id):
    url = f'https://dummyjson.com/recipe/{recipe_id}'

    response = requests.get(url)

    if response.status_code == 200:
        recipe = response.json()
        return recipe
    else:
        print('Ошибка при получении информации о рецепте:', response.status_code)
        return None

@app.route('/recipe/<recipe_id>')
def recipe_detail(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)





if __name__ == '__main__':
    app.run(debug=True )

