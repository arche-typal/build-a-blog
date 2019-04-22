from flask import Flask, request, redirect, render_template 
import cgi
import os
import jinja2

from flask_sqlalchemy import SQLAlchemy

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cheese@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))#

    def __init__(self, name, body):
        self.name = name
        self.body = body

def check_for_space(astring):
    if len(astring) == 0:
        return True
    else:
        return False

@app.route('/')
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.id.desc()).all()
    template = jinja_env.get_template('blog.html')
    return template.render(posts=posts)


@app.route('/addpost', methods=['POST', 'GET'])
def a_post():

    if request.method == 'POST':
        post_name = request.form['a_post'] #name= from .html
        post_body = request.form['a_body']
        post_error = ""

        if check_for_space(post_name) or check_for_space(post_body) or post_name.isspace() or post_body.isspace():
            post_error = "Please no posts that are empty or only spaces."
            template = jinja_env.get_template('addpost.html') 
            return template.render(post_name=post_name, post_body=post_body, post_error = post_error)

        else:
            #posts.append(post) #using list b4 sqlalchemy
            new_post = Post(post_name, post_body)#### next argument?(post_name, post_body)
            db.session.add(new_post)
            db.session.commit()

            template = jinja_env.get_template('viewblog2.html')
            return template.render(post_name=post_name, post_body=post_body)


    posts = Post.query.all()

    #b4jinja#return render_template('addpost.html', title ="A POST", posts=posts)
       
    template = jinja_env.get_template('addpost.html') 
    return template.render(posts=posts) #variables auto ="", no need to set-up


@app.route('/delete-post', methods=["POST"])
def delete_post():

    post_id = int(request.form['post-id'])
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit() 

    return redirect('/blog') 

@app.route('/view-post', methods=['POST', 'GET'])
def view_post():
    
    post_id = int(request.args.get('post-id'))
    post = Post.query.get(post_id)

    template = jinja_env.get_template('viewblog.html')
    return template.render(post=post)
    

if __name__ == '__main__':
    app.run()
