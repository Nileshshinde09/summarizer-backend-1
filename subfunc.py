def is_valid_input(data):
    if data is not None and len(data) > 100:
        return True
    return False

def sanitize_input(data):
    # Implement your data sanitization logic here
    return data.strip()
def input_for_ca(data):
    splt= data.split(' ')
    username=splt[0]
    fname=splt[1]
    lname=splt[2]
    email=splt[3]
    password=splt[4]
    return username,fname,lname,email,password