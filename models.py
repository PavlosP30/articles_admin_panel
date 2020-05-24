from app import db, ma
from datetime import datetime
from passlib.hash import sha256_crypt

# Define table for Authors
class Authors(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    hashedPass = db.Column(db.String(200), nullable = False)
    userName = db.Column(db.String(50), nullable = False)
    firstName = db.Column(db.String(50), nullable = True)
    lastName = db.Column(db.String(50), nullable = True)
    articles = db.relationship('Articles', backref = 'authors', lazy = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # Function that returns a string upon creating new db record
    def __repr__(self):
        return "User Successfully Created(id='%s', email='%s', userName='%s')" % (self.id, self.email, self.userName)

#Define output format with Marshmallow
class AuthorsSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ("id", "email", "userName", "firstName", "lastName", "date_created")

# Define table for Articles
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('news_categories.id'), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable = False)
    title = db.Column(db.String(200), nullable = False)
    summary = db.Column(db.String(200), nullable = False)
    content = db.Column(db.Text, nullable = False)
    pub_status = db.Column(db.Integer, nullable = False, default="0")
    pub_date = db.Column(db.DateTime, default = datetime.utcnow)

    # Function that returns a string upon creating new db record
    def __repr__(self):
        return "Article Successfully Created(id='%s', category_id='%s', title='%s')" % (self.id, self.category_id, self.title)

#Define output format with Marshmallow
class ArticlesSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ("id", "category_id", "news_categories.title", 
            "author_id", "authors.userName", "authors.userName",
            "authors.firstName", "authors.lastName",
            "title", "summary", "content", "pub_status", "pub_date")

# Define table for Articles
class News_categories(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), nullable = False)
    articles = db.relationship('Articles', backref = 'news_categories', lazy = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # Function that returns a string upon creating new db record
    def __repr__(self):
        return "News Category Successfully Created(id='%s', title='%s')" % (self.id, self.title)

#Define output format with Marshmallow
class News_categoriesSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ("id", "title", "date_created")

#Drop all tables and create again - for the purpose of this assignment
db.drop_all()
db.create_all()

# Create an admin User on creation of table Authors
email = "admin@admin.com"
password = "admin1234"
hashedPass = sha256_crypt.encrypt(password)
user_name = "Admin_1"
first_name = "John"
last_name = "Doe"

author = Authors(email = email, hashedPass = hashedPass, userName = user_name, firstName = first_name, lastName = last_name)
news_category = News_categories(title = 'Local News')
news_category2 = News_categories(title = 'Science & Technology')
news_category3 = News_categories(title = 'Sports')
news_category4 = News_categories(title = 'Politics')
news_category5 = News_categories(title = 'Business')
news_category6 = News_categories(title = 'Education')

db.session.add(author)
db.session.add(news_category)
db.session.add(news_category2)
db.session.add(news_category3)
db.session.add(news_category4)
db.session.add(news_category5)
db.session.add(news_category6)

db.session.commit()