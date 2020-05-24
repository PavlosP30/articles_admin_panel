from app import app, db
from models import Authors, Articles, News_categories, AuthorsSchema, ArticlesSchema, News_categoriesSchema
from flask import render_template, url_for, request, redirect, session, jsonify
from passlib.hash import sha256_crypt

@app.route('/')
def index():
    if 'user_name' in session:
        articles = Articles.query\
            .join(Authors, Articles.author_id == Authors.id)\
            .join(News_categories, Articles.category_id == News_categories.id)\
            .all()

        viewData = {
            'title' : 'Admin Panel',
            'list_item_active' : 'admin_panel',
            'articles' : articles
        }
        return render_template('index.html', data = viewData)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/user/login', methods = ['POST', 'GET'])
def login():
    if 'user_name' in session:
        return redirect(url_for('index'))
    else:
        viewData = {
            'title' : 'Login',
            'list_item_active' : 'login'
        }
        
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = Authors.query.filter_by(email = email).first()
            if user:
                if sha256_crypt.verify(password, user.hashedPass):
                    session['userID'] = user.id
                    session['user_name'] = user.userName
                    session['first_name'] = user.firstName
                    session['last_name'] = user.lastName
                    session['email'] = user.email
                    return redirect(url_for('index', data = viewData))

                else:
                    viewData = {
                        'title' : 'Login',
                        'list_item_active' : 'login',
                        'error_message' : 'Wrong password!'
                    }

                    return render_template('login.html', data = viewData)

            else:
                viewData = {
                    'title' : 'Login',
                    'list_item_active' : 'login',
                    'error_message' : 'Wrong email password!'
                }

                return render_template('login.html', data = viewData)
        else:
            return render_template('login.html', data = viewData)

@app.route('/article_add', methods = ['POST', 'GET'])
def article_add():
    if 'user_name' in session:
        # Fetch News Categories from DB
        news_categories = News_categories.query.order_by(News_categories.date_created).all()

        viewData = {
            'title' : 'Add Article',
            'list_item_active' : 'article_add',
            'news_categories': news_categories
        }

        if request.method == 'POST':
            category_id = request.form['category_id']
            author_id = session['userID']
            title = request.form['title']
            summary = request.form['summary']
            content = request.form['content']
            pub_status = request.form['pub_status']

            article = Articles(category_id = category_id, author_id = author_id, title = title, summary = summary, content = content, pub_status = pub_status)

            try:
                db.session.add(article)
                db.session.commit()

                return redirect(url_for('index'))

            except:
                return 'There was an issue with creating new Article!'
        else:
            return render_template('article_add.html', data = viewData)
    else:
        return redirect(url_for('login'))

@app.route('/articles/delete/<int:id>')
def delete(id):
    article = Articles.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()

        return redirect(url_for('index'))

    except:
        return 'There was an issue with deleting Article!'

@app.route('/articles/edit/<int:id>', methods = ['POST', 'GET'])
def edit(id):

    article = Articles.query.get_or_404(id)

    if request.method == 'POST':
        article.category_id = request.form['category_id']
        article.author_id = session['userID']
        article.title = request.form['title']
        article.summary = request.form['summary']
        article.content = request.form['content']
        article.pub_status = request.form['pub_status']

        try:
            db.session.commit()

            return redirect(url_for('index'))

        except:
            return 'There was an issue with updating Article!'
    else:
        # Fetch News Categories from DB
        news_categories = News_categories.query.order_by(News_categories.date_created).all()

        viewData = {
            'title' : 'Edit Article',
            'list_item_active' : 'article_edit',
            'news_categories': news_categories,
            'article': article
        }

        return render_template('article_edit.html', data = viewData)

#API for fetching all Articles
@app.route('/articles', methods = ['GET'])
def get_articles():
    articles_schema = ArticlesSchema(many = True)
    
    articles = Articles.query\
        .join(Authors, Articles.author_id == Authors.id)\
        .join(News_categories, Articles.category_id == News_categories.id)\
        .all()
        
    articleList = {
        'articleList' : articles_schema.dump(articles)
    }

    return jsonify(articleList)

#API for fetching all Authors
@app.route('/authors', methods = ['GET'])
def get_authors():
    authors_schema = AuthorsSchema(many = True)

    authors = Authors.query.all()

    authorsList = {
        'authorsList' : authors_schema.dump(authors)
    }

    return jsonify(authorsList)

#API for fetching all News Categories
@app.route('/news_categories', methods = ['GET'])
def get_news_categories():
    cat_schema = News_categoriesSchema(many = True)

    news_cat = News_categories.query.all()

    newsCatList = {
        'newsCatList' : cat_schema.dump(news_cat)
    }

    return jsonify(newsCatList)