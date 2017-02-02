# -*- coding: utf-8 -*-
#
# Copyright 2016, 2017 Marreta.Org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Index
#
@auth.requires_login()
def index():
    return locals()

#
# User Administration
#
@auth.requires(auth.has_membership('Marreta Administrator'))
def add_user():
    form = SQLFORM(db.auth_user, submit_button='Save',
            labels={'first_name':'First Name',
            'last_name':'Last Name',
            'email':'E-Mail',
            'password':'password',
            'address':'Address'})


    if form.process().accepted:
        # include user on Marreta User Group as default
        db.auth_membership.insert(user_id=form.vars.id, group_id=2)
        response.flash = 'User Added!'
    elif form.errors:
        response.flash = 'Error to add user! Verify data.'


    return dict(form=form)


@auth.requires(auth.has_membership('Marreta Administrator'))
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

@auth.requires(auth.has_membership('Marreta Administrator'))
def manage_user():
    user_id = request.args(0) or redirect(URL('list_users'))
    form = SQLFORM(db.auth_user, user_id, deletable=True).process()

    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                             args=[user_id],
                             ajax=True)

    membership_dc_panel = LOAD(request.controller,
                            'manage_dc_membership.html',
                             args=[user_id],
                             ajax=True)

    return dict(form=form,
                membership_panel=membership_panel,
                membership_dc_panel=membership_dc_panel)

@auth.requires(auth.has_membership('Marreta Administrator'))
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form_user = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=True,
                       details=False,
                       selectable=False,
                       csv=False,
                       user_signature=False)  # change to True in production
    return form_user

@auth.requires(auth.has_membership('Marreta Administrator'))
def manage_dc_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_dc_membership.auth_id.default = int(user_id)
    db.auth_dc_membership.auth_id.writable = False
    form_dc = SQLFORM.grid(db.auth_dc_membership.auth_id == user_id,
                       args=[user_id],
                       searchable=False,
                       deletable=True,
                       details=False,
                       selectable=False,
                       csv=False,
                       user_signature=True)  # change to True in production

    auth.add_permission(2, 'dc_admin', 'auth_dc_membership' )
    return form_dc
#
# DC Management
#
@auth.requires(auth.has_membership('Marreta Administrator'))
def add_dc():
    form = SQLFORM(db.DataCenter, submit_button='Save',
            labels={'DC':'Data Center', 'DCInfo': 'Data Center information'},
                   )
    if form.process().accepted:
        response.flash = 'Data Center {} added !'.format(form.vars.dc)
    elif form.errors:
        response.flash = 'Error to add Data Center! Verify data.'
    return dict(form=form)


@auth.requires(auth.has_membership('Marreta Administrator') or
               auth.has_membership('Data Center Administrator')
              )
def list_dcs():
    # get current logged user ID
    current_user = auth.user_id
    # get the current logged user groups ids (list)
    current_user_groups = auth.user_groups.values()
    btn = lambda row: A("Edit", _href=URL('manage_dc', args=row.DataCenter.id))
    db.DataCenter.edit = Field.Virtual(btn)

    # list only datacenters that the user is member
    if 'Marreta Administrator' in current_user_groups:
        rows = db(db.DataCenter).select()
    else:
        # get the list of datacenters membership of current logged user
        dc_member = db(db.auth_dc_membership.auth_id == current_user).select()
        dc_list = []
        for dc in dc_member:
            dc_list.append(int(dc.dc))

        rows = db(db.DataCenter.id.belongs(dc_list)).select()

    headers = ["ID", "Data Center Name", "Edit"]
    fields = ['id', 'DC', "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields]) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)

@auth.requires(auth.has_membership('Marreta Administrator') or
               auth.has_membership('Data Center Administrator')
              )
def manage_dc():
    # get current logged user ID
    current_user = auth.user_id
    # get the current logged user groups ids (list)
    current_user_groups = auth.user_groups.values()
    # get the list of datacenters membership of current logged user
    dc_member = db(db.auth_dc_membership.auth_id == current_user).select()
    # create a datacenter list
    dc_list = []
    for dc in dc_member:
        dc_list.append(int(dc.dc))

    # enables deletable only for Marreta Administrators
    if 'Marreta Administrator' in current_user_groups:
        deletable_value=True
    else:
        deletable_value=False

    dc_id = request.args(0) or redirect(URL('list_dcs'))
    # shows the editable form only if the user is datacenter admin of this dc
    if 'Marreta Administrator' in current_user_groups or int(dc_id) in dc_list:
        form = SQLFORM(db.DataCenter, dc_id, deletable=deletable_value).process()
    else:
        form = 'User not allowed to manage this Data Center.'

    manage_approvers_panel = LOAD(request.controller,
                                  'manage_approvers.html',
                                  args=[dc_id],
                                  ajax=True)

    return dict(form=form,
                manage_approvers_panel=manage_approvers_panel)

@auth.requires(auth.has_membership('Marreta Administrator'))
def manage_approvers():
    dc_id = request.args(0) or redirect(URL('list_dcs'))
    db.auth_dc_approvers.dc.default = int(dc_id)
    db.auth_dc_approvers.dc.writable = False
    form_approvers = SQLFORM.grid(db.auth_dc_approvers.dc == dc_id,
                                  args=[dc_id],
                                  searchable=False,
                                  deletable=True,
                                  details=False,
                                  selectable=False,
                                  csv=False,
                                  user_signature=False)  # change to True in production
    return form_approvers

#
# IC Management
#
@auth.requires(auth.has_membership('Marreta Administrator'))
def add_ci():
    form = SQLFORM(db.ConfigurationItem, submit_button='Save',
                    labels={'CI': 'Configuration Item', 'DC': 'Data Center', 'AddedDate' : 'Added Date',
                            'ServerStatus' : 'Server Status', 'LastServerCHK' : 'Last Server Check'
                            },
                   )
    # TODO: Form should not show options to fillup Server Status, LastServerChk or AddedDate.
    # TODO: This should be filled by appliacion itself.

    """
     is necessary add here the functions using the MARRETA Engine
    """
    if form.process().accepted:
        response.flash = 'IC Added!'
    elif form.errors:
        response.flash = 'Error to add IC! Verify data.'
    return dict(form=form)
