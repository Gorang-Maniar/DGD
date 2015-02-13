# coding: utf8


db.define_table('category',
                Field('name',requires=(IS_SLUG(),IS_LOWER(),IS_NOT_IN_DB(db,'category.name'))))
db.define_table('post',
                Field('category','reference category',readable=False,writable=False),
                Field('title','string',requires=IS_NOT_EMPTY()),
                Field('Url',requires=IS_EMPTY_OR(IS_URL())),
                Field('body','text',requires=IS_NOT_EMPTY()),
                Field('file_name','upload'),
                Field('tags','text',requires=IS_NOT_EMPTY(),default=None),
                Field('votes','integer',default=0,readable=False,writable=False),
                auth.signature)

db.define_table('votes',
                Field('post','reference post'),
                Field('score','integer',default=+1),
                auth.signature)
db.define_table('comm',
                Field('post','reference post',readable=False,writable=False),
                Field('votes','integer',readable=False,writable=False),
                Field('body','text',requires=IS_NOT_EMPTY()),
                auth.signature)
db.define_table('comm_votes',
                Field('comm','reference comm'),
                Field('score','integer',default=+1),
                auth.signature)
db.define_table('profile',
                Field('profile_pic','upload'),
                auth.signature)
def writer(id):
    if id is None:
        return "Unknown"
    else:
        user = db.auth_user(id)
        return A('%(first_name)s %(last_name)s' % user,_style="color:gold;",_href=URL('list_posts_by_author',args=user.id))
