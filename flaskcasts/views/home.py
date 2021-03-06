from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flaskcasts.models import Post, User
from flaskcasts.common.pagination import paginate
from flaskcasts.common.decorators import requires_login
import flaskcasts.common.user_errors as error
import random

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/page/<int:page>')
def index(page=1):
    posts = Post.all_desc()
    paginated_posts = paginate(posts, page, per_page=5)
    return render_template('home/index.html',
                           paginated_posts=paginated_posts)


@home.route('/post/<string:slug>')
def post(slug):
    post = Post.get_post('slug', slug)
    author = User.get_user("_id", post['author'])
    return render_template('home/post.html', post=post, author=author['fullname'])


@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        try:
            if User.is_login_valid(user_id, password):
                session['user_id'] = user_id
                session['logged_in'] = True
                flash('You are now logged in.', 'success')
                return redirect(url_for('.index'))
        except error.UserError as e:
            # Flash error message...
            flash(e.message, 'danger')
            return render_template('home/login.html')

    return render_template('home/login.html')

@home.route('/logout')
def logout():
    if session.get('logged_in'):
        # Log out the user.
        session.clear()
        flash("You are now logged out", 'success')
        return redirect(url_for('.index'))
    else:
        flash("You have to login before you can logout!", 'warning')
        return render_template('home/login.html')


@home.route('/create', methods=['GET', 'POST'])
@requires_login
def create():
    # IF method = post, process the new post.
    # we need to make sure the slug generated is not a duplicate
    # if so, we will append a random number
    if request.method == 'POST':
        new_post = Post(request.form['title'],
                        request.form['content'],
                        session['user_id'])
        if Post.get_post('slug', new_post.slug) is None:
            # if there are no posts with this slug
            new_post.save()
        else:
            # append a random number string to the end of the slug
            new_post.slug += str(random.randint(0,100))
            new_post.save()
        flash('New post created.', 'success')
        return redirect(url_for('home.post', slug=new_post.slug))

    return render_template('home/create.html')


@home.route('/edit/<string:post_id>', methods=['GET', 'POST'])
@requires_login
def edit(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        Post.update(post_id, title, content)
        flash('Post successfully updated!!!', 'success')
        return redirect(url_for('home.post',
                                slug=Post.get_post("_id", post_id)['slug']))

    post = Post.get_post("_id", post_id)
    return render_template('home/edit.html', post=post)


@home.route('/remove/<string:post_id>')
@requires_login
def remove(post_id):
    Post.remove_post(post_id)
    flash("Post: {} removed.".format(post_id), 'warning')
    return redirect(url_for('.index'))


@home.route('/about')
def about():
    return render_template('home/about.html')


@home.route('/contact')
def contact():
    return render_template('home/contact.html')
