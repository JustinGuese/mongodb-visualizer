from werkzeug.security import generate_password_hash

user = input("please enter user")
pwhash = generate_password_hash(input("please enter password"))

print("please add the following to app.py at users = { '%s':'%s'}"%(user,pwhash))
