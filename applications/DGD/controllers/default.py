# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
POST_PER_PAGE = 10
def get_category():
    category_name=request.args(0)
    category=db.category(name=category_name)
    if not category:
        session.flash = "Page not found"
        redirect(URL('index'))
    return category

def index():
    category = db(db.category.name).select()
    page = request.args(0,cast=int,default=0)
    start = page*POST_PER_PAGE
    stop = start + POST_PER_PAGE
    posts = db(db.post).select(orderby=~db.post.created_on,limitby=(start,stop))
    posts1 = db(db.post).select(orderby=~db.post.votes,limitby=(start,stop))
    return locals()


def create_post():
    category=get_category()
    db.post.category.default = category.id
    form = SQLFORM(db.post).process(next='view_post/[id]')
    return locals()

def edit_post():
    id = request.args(0,cast=int)
    form = SQLFORM(db.post,id,showid=False).process(next='view_post/[id]')
    return locals()

def list_posts_by_datetime():
    response.view = 'default/list_posts_by_votes.html'
    category = get_category()
    page = request.args(1,cast=int,default=0)
    start = page*POST_PER_PAGE
    stop = start + POST_PER_PAGE
    rows = db(db.post.category==category.id).select(orderby=~db.post.created_on,limitby=(start,stop))
    return locals()

def list_posts_by_votes():
    category=get_category()
    page = request.args(1,cast=int,default=0)
    start = page*POST_PER_PAGE
    stop = start + POST_PER_PAGE
    rows = db(db.post.category==category.id).select(orderby=~db.post.votes,limitby=(start,stop))
    return locals()

def list_posts_by_author():
    user_id = request.args(0,cast=int)
    profile_pic = db(db.profile.created_by==user_id).select(orderby=~db.profile.created_on)
    form = SQLFORM(db.profile).process(next='index')
    page = request.args(1,cast=int,default=0)
    start = page*POST_PER_PAGE
    stop = start + POST_PER_PAGE
    rows = db(db.post.created_by==user_id).select(orderby=~db.post.created_on,limitby=(start,stop))
    posts1 = db(db.post).select(orderby=~db.post.votes,limitby=(start,stop))
    category = db(db.category).select()
    return locals()

def view_post():
    id1 = request.args(0,cast=int)
    category = db(db.category.name).select()
    post = db.post(id=id1) or redirect(URL('index'))
    db.comm.post.default = post.id
    form = SQLFORM(db.comm).process()
    comments = db(db.comm.post==post.id).select(orderby=~db.comm.created_on)
    answers = db(db.comm.post == post.id).count()
    posts1 = db(db.post).select(orderby=~db.post.votes,limitby=(1,10))
    return locals()

def vote_callback():
    vars = request.get_vars
    if vars:
        id = vars.id
        direction = +1 if vars.directon == 'up' else -1
        post = db.post(id)
        if post:
            post.update_record(votes=post.votes+direction)
    return str(post.votes)

def comm_vote_callback():
    id = request.args(0,cast=int)
    direc = request.args(1,cast=int)
    return locals()
def download():
    import os
    path=os.path.join(request.folder,'uploads',request.args[0])
    return response.stream(path)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
