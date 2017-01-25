Marreta
#######

Marreta is a project to create a dual custody password systems.

Marreta can not be used yet. It is in planning phase yet.

Devel
=====

Creating a devel environment

Database:
---------

1. Install the MySQL
2. Create a table with name marreta
3. Edit {web2py}/Contents/Resources/applications/marreta/private/appconfig.ini

   - Include the correct information for DB Access

     ``uri       = mysql://root:marreta_dev_password@localhost/marreta``


Marreta (and web2py)
--------------------

1. Go to http://web2py.com and Download web2py for your OS
2. Unzip/Uncompress the web2py
3. Go to directory Contents/Resources/applications/
4. Do the git clone for this review
5. Run the web2py.py (Contents/Resources/)
6. Got to http://127.0.0.1/marreta/
7. Select Marreta Administration
8. Default login: admin@marreta.org / abc1234

How to submit reviews
---------------------


1. Create a new branch: ``git checkout -b my_new_feature``
2. Edit/correct/create your new code
3. Submit via git-review: ``git review``