from urllib.parse import parse_qs

HELLO_WORLD = """<html>
<body><h1>Welcome to Test</h1><form action="./goDo" method="GET">
<p>First name: <input type="text" name="first_name">
<p>Last name: <input type="text" name="last_name">
<p><input type="submit" name="Submit"></form></body>
</html>"""

myQueryString = ""
myoutput = ""

def dothis():
    global myoutput
    global myQueryString

    myFirstName = myQueryString['first_name'][0]
    myLastName  = myQueryString['last_name'][0]

    if (myFirstName == None) :
        myFirstName = 'No'
        myLastName = 'One'

    myoutput += "Hello there " + myFirstName + myLastName
    myoutput += "<p><a href="">Start over</a>"

def application(environ, start_response):
    global myoutput
    global myQueryString

    match(environ.get('PATH_INFO')):
        case '/':
            status = '200 OK'
            content = HELLO_WORLD

        case'/goDo':
            myQueryString = parse_qs(environ.get('QUERY_STRING'))
            dothis()
            status = '200 OK'
            content = myoutput

        case _ :
            status = '404 NOT FOUND'
            content = 'Page not found.'

    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
    start_response(status, response_headers)

    yield content.encode('utf8')

