from flask import Blueprint, render_template, request
from flaskcasts.models import Post, User
from flaskcasts.common.pagination import paginate
from flaskcasts.common.decorators import requires_login

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
    author = User.get_user(post['author'])
    return render_template('home/post.html', post=post, author=author['fullname'])


@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pass

    return render_template('home/login.html')

@home.route('/create', methods=['GET', 'POST'])
@requires_login
def create():
    pass


@home.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@requires_login
def edit(post_id):
    pass
