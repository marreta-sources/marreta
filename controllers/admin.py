# -*- coding: utf-8 -*-
#
#

@auth.requires_login()
def index():
    return locals()

#
# User Administration
#
@auth.requires(auth.has_membership('marreta_admin'))
def add_user():
    form = SQLFORM(db.auth_user, submit_button='Save',
            labels={'first_name':'First Name',
            'last_name':'Last Name',
            'email':'E-Mail',
            'password':'password',
            'address':'Address'})
    if form.process().accepted:
        response.flash = 'User Added!'
    elif form.errors:
        response.flash = 'Error to add user! Verify data.'
    return dict(form=form)


@auth.requires(auth.has_membership('marreta_admin'))
def list_users():
    btn = lambda row: A("Edit", _href=URL('manage_user', args=row.auth_user.id))
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = ["ID", "Name", "Last Name", "Email", "Edit"]
    fields = ['id', 'first_name', 'last_name', "email", "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)

@auth.requires(auth.has_membership('marreta_admin'))
def manage_user():
    user_id = request.args(0) or redirect(URL('list_users'))
    form = SQLFORM(db.auth_user, user_id, deletable=True).process()
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                             args=[user_id],
                             ajax=True)
    return dict(form=form,membership_panel=membership_panel)

@auth.requires(auth.has_membership('marreta_admin'))
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=True,
                       details=False,
                       selectable=False,
                       csv=False,
                       user_signature=False)  # change to True in production
    return form

#
# DC Management
#
@auth.requires(auth.has_membership('marreta_admin'))
def add_dc():
    form = SQLFORM(db.dc, submit_button='Save',
            labels={'dc':'Data Center Name'})
    if form.process().accepted:
        response.flash = 'Data Center Added!'
    elif form.errors:
        response.flash = 'Error to add Data Center! Verify data.'
    return dict(form=form)

@auth.requires(auth.has_membership('marreta_admin'))
def list_dcs():
    btn = lambda row: A("Edit", _href=URL('manage_dc', args=row.dc.id))
    db.dc.edit = Field.Virtual(btn)
    rows = db(db.dc).select()
    headers = ["ID", "Data Center Name", "Edit"]
    fields = ['id', 'dc', "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)

@auth.requires(auth.has_membership('marreta_admin'))
def manage_dc():
    dc_id = request.args(0) or redirect(URL('list_dcs'))
    form = SQLFORM(db.dc, dc_id, deletable=True).process()
    return dict(form=form)


#
# IC Management
#
@auth.requires(auth.has_membership('marreta_admin'))
def add_ci():
    form = SQLFORM(db.ci, submit_button='Save',
            labels={'ci':'Configuration Item',
                    'hostname': 'IC Hostname',
                    'ip_address': 'IP Address or name'})

    """
    It is necessary add here the functions using the MARRETA Engine
    """
    if form.process().accepted:
        response.flash = 'IC Added!'
    elif form.errors:
        response.flash = 'Error to add IC! Verify data.'
    return dict(form=form)