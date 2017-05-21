from . import articles
from flask_login import login_required, current_user
from flask import render_template, url_for, redirect, request
from ..models import Article, Tag
from .forms import ArticleForm 
from .. import db



@articles.route('/articles')
@login_required
def allarticles():
   articles = Article.get_published()
   popular_tags = Tag.get_popular_tags()
   return render_template('articles/articles.html', articles=articles, popular_tags=popular_tags)




@articles.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data, status=form.status.data, user=current_user)
        article.create_tags(form.tags.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('articles.allarticles'))
        

    return render_template('articles/write.html', form=form)


@articles.route('/drafts', methods=['GET', 'POST'])
@login_required
def drafts():
    drafts = Article.query.filter_by(status='D', user=current_user)
    return render_template('articles/drafts.html', drafts=drafts)
    
@articles.route('/editdraft/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    article = Article.query.filter_by(id=id).first()  
    form = ArticleForm()
    if article is not None:
        form.title.data = article.title
        form.content.data = article.content
        form.tags = article.tags
    if form.validate_on_submit():
        #db.session.add(article)
        #db.session.commit()
        #article.title = form.title.data
        #article.content = form.content.data
        #article.create_tags(form.tags.data)
        return redirect(url_for('articles.allarticles'))
    
    return render_template('articles/edit.html', form=form)
        
@articles.route('/article-tag/<tag>')
@login_required
def tag(tag):
    tags = Tag.query.filter_by(tag=tag) 
    articles = []
    
    for tag in tags:
        if tag.article.status == Article.PUBLISHED:
            articles.append(tag.article)
    
    popular_tags = Tag.get_popular_tags()
    return render_template('articles/articles.html', articles=articles, popular_tags=popular_tags )

@articles.route('/article/<id>')
@login_required
def article(id):
    article = Article.query.filter_by(id=id).first()
    return render_template('articles/article.html', article=article)

