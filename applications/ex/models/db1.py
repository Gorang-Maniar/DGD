# coding: utf8
db.define_table('post',
                Field('Email',requires=IS_EMAIL()),
                Field('filen','upload'),
                auth.signature)
