# coding: utf8
db.define_table('users',
                auth.signature
                )
db.define_table('post',
                Field('rece','reference users'),
                Field('body','text'),
                auth.signature
                )
