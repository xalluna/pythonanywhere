import mysql.connector
from threading import Lock
from urllib.parse import parse_qs

#Singleton implementation credit: [refactoring.guru](https://refactoring.guru/design-patterns/singleton/python/example#example-1)
class SingletonMeta(type):
  _instances = {}
  _lock: Lock = Lock()

  def __call__(cls, *args, **kwargs):
      with cls._lock:
          if cls not in cls._instances:
              instance = super().__call__(*args, **kwargs)
              cls._instances[cls] = instance
      return cls._instances[cls]


class Database(metaclass=SingletonMeta):
  def __init__(self) -> None:
      user = "alluna"
      password = "1q1q1q1q!Q!Q!Q!Q"
      database = "alluna$Bookstore"
      host = "alluna.mysql.pythonanywhere-services.com"
      self.connection = mysql.connector.connect(host=host, user=user, passwd=password, database=database)


class HttpStatus:
  OK = '200 OK'
  CREATED = '201 CREATED'
  NO_CONTENT = '202 NO CONTENT'

  BAD_REQUEST = '400 BAD REQUEST'
  NOT_FOUND = '404 NOT FOUND'


STYLES = """
<style>
  body {
    --background-color: #222;
    --primary-color: aliceblue;
    ---tranparent: #00000000;
    --lighten: #ffffff0f;
    --darken: #00000030;
    --border-radius: 0.25rem;
    --h-gap: 10px;
    --v-gap: 5px;
    --padding: 4px;

    font-family: Verdana, Geneva, Tahoma, sans-serif;
    display: flex;
    justify-content: center;
    background-color: var(--background-color);
    color: var(--primary-color);
  }

  h3 {
    font-weight: 200;
  }

  input {
    border-radius: var(--border-radius);
    background-color: var(---darken);
    color: var(--primary-color);
    box-shadow: none;
    border: solid 1px;
    padding: var(--padding);
  }

  .action-button {
    background-color: var(---tranparent);
    color: var(--primary-color);
    border-radius: var(--border-radius);
    border: solid 2px var(--primary-color);
    padding: 5px 10px;
    cursor: pointer;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    font-size: medium;
  }

  .action-button.secondary {
    border: 0px;
    background-color: var(--primary-color);
    color: var(--background-color);
  }

  a.action-button {
    text-decoration: none;
  }

  .actions {
    display: flex;
    gap: var(--h-gap);
    width: fit-content;
    margin: auto;
  }

  .basic-page {
    width: 70%;
    background-color: var(--lighten);
    border-radius: var(--border-radius);
  }

  form {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(2 * var(--v-gap));
  }

  form div.form-row p {
    margin: 0px;
    padding: var(--padding);
  }

  form div.form-fields {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: var(--v-gap);
  }

  form div.form-fields div.form-row {
    display: flex;
    align-items: flex-end;
    gap: var(--h-gap);
  }

  table {
    border-right: solid 2px var(--primary-color);
    border-bottom: solid 2px var(--primary-color);
    border-spacing: 0px;
  }

  th {
    border-top: solid 2px var(--primary-color);
    border-bottom: solid 1px var(--primary-color);
    border-left: solid 2px var(--primary-color);
  }

  td {
    border-top: solid 1px var(--primary-color);
    border-left: solid 2px var(--primary-color);
  }

  th,
  td {
    padding: 4px 10px;
  }

  .error {
    color: red;
  }

  .required {
    color: red;
  }

  form table {
    border: 0px;
    padding: 0px;
    border-spacing: 10px;
  }

  form table tr {
    border: 0px;
  }

  form table td {
    border: 0px;
    padding: 0px;
  }

  form table td label {
    border: 0px;
    padding: 0px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
  
  form table td label p {
    margin: 0px;
  }
</style>
"""


def home_page():
  return (HttpStatus.OK, f"""
{STYLES}

<body>
  <div class="basic-page">
    <h3 style="text-align: center">What action would you like to perform?</h3>
    <div class="actions">
      <a
        class="action-button"
        href="books/create"
      >
        Create
      </a>
      <a
        class="action-button"
        href="/books"
        >Search</a
      >
    </div>
  </div>
</body>
""")


def search_page(query_string):
  query = parse_qs(query_string)
  results = []

  book = {
    "title": '' if query.get('title') is None else query.get('title')[0],
    "author": '' if query.get('author') is None else query.get('author')[0],
    "isbn": '' if query.get('isbn') is None else query.get('isbn')[0],
    "publisher": '' if query.get('publisher') is None else query.get('publisher')[0],
    "year": '' if query.get('year') is None else query.get('year')[0]
  }

  database = Database()
  cursor = database.connection.cursor()

  sql_command = "SELECT * FROM Books "
  commands = []

  if book['title']:
      commands.append(f"Title like '%{book['title']}%'")

  if book['author']:
      commands.append(f"Author like '%{book['author']}%'")

  if book['isbn']:
      commands.append(f"ISBN like '%{book['isbn']}%'")
      
  if book['publisher']:
      commands.append(f"Publisher like '%{book['publisher']}%'")
      
  if book['year']:
      commands.append(f"Year = '{book['year']}'")

  for (command, i) in zip(commands, range(len(commands))):
    sql_command += f'{"WHERE" if i == 0 else "AND"} {command}'

  if(query_string):
    cursor.execute(sql_command)
    results = cursor.fetchall()

  items = ''
  for (title, author, isbn, publisher, year) in results:
    items += f"""
      <tr>
        <td>{title}</td>
        <td>{author}</td>
        <td>{isbn}</td>
        <td>{publisher}</td>
        <td>{year}</td>
      </tr>
    """
  
  table = f"""
      <div style="display: flex; justify-content: center">
        <table>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Publisher</th>
            <th>Year</th>
          </tr>

          {items}
        </table>
      </div>
"""

  return (HttpStatus.OK, f"""
{STYLES}
            
<body>
  <div class="basic-page">
    <form action="/books" method="GET">
      <table>
        <tr>
          <td><label>Title</label></td>
          <td><input type="text" name="title" value="{book['title']}" /></td>
        </tr>

        <tr>
          <td><label>Author</label></td>
          <td><input type="text" name="author" value="{book['author']}" /></td>
        </tr>

        <tr>
          <td><label>ISBN</label></td>
          <td><input type="text" name="isbn" value="{book['isbn']}" /></td>
        </tr>

        <tr>
          <td><label>Publisher</label></td>
          <td><input type="text" name="publisher" value="{book['publisher']}" /></td>
        </tr>

        <tr>
          <td><label>Year</label></td>
          <td><input type="text" name="year" value="{book['year']}" /></td>
        </tr>
      </table>

      <div class="actions">
        <button
          class="action-button"
          type="submit"
        >
          Search
        </button>
        <a
          class="action-button secondary"
          type="button"
          href="/"
          >Back</a
        >
      </div>
    </form>
    {'' if not results else table}
    {'' if not query_string or results else f'<p style="text-align: center; padding-top: 5px">No results found</p>'}
  </div>
</body>
""")

DEFAULT_RESPONSE = {
     'data': None,
     'errors': {
        "title": None,
        "author": None,
        "isbn": None,
        "publisher": None,
        "year": None
     },
     'hasErrors': False
  }

def create_page(response: dict = DEFAULT_RESPONSE):
  response_code = HttpStatus.OK

  if response['hasErrors'] == True:
    response_code = HttpStatus.BAD_REQUEST

  if not response['data'] == None:
    response_code = HttpStatus.CREATED

  return (response_code, f"""
{STYLES}
            
<body>
  <div class="basic-page">
    <form action="/books/create" method="PUT">
      <table>
        <tr>
          <td><label>Title<p class="required">*</p></label></td>
          <td><input type="text" name="title" /></td>
          {'' if response['errors']['title'] == None else f'<td><p class="error">{response["errors"]["title"]}</p></td>'}
        </tr>

        <tr>
          <td><label>Author<p class="required">*</p></label></td>
          <td><input type="text" name="author" /></td>
          {'' if response['errors']['author'] == None else f'<td><p class="error">{response["errors"]["author"]}</p></td>'}
        </tr>

        <tr>
          <td><label>ISBN<p class="required">*</p></label></td>
          <td><input type="text" name="isbn" /></td>
          {'' if response['errors']['isbn'] == None else f'<td><p class="error">{response["errors"]["isbn"]}</p></td>'}
        </tr>

        <tr>
          <td><label>Publisher<p class="required">*</p></label></td>
          <td><input type="text" name="publisher" /></td>
          {'' if response['errors']['publisher'] == None else f'<td><p class="error">{response["errors"]["publisher"]}</p></td>'}
        </tr>

        <tr>
          <td><label>Year<p class="required">*</p></label></td>
          <td><input type="text" name="year" /></td>
          {'' if response['errors']['year'] == None else f'<td><p class="error">{response["errors"]["year"]}</p></td>'}
        </tr>
      </table>

      <div class="actions">
        <button
          class="action-button"
          type="submit"
        >
          Create
        </button>
        <a
          class="action-button secondary"
          type="button"
          href="/"
          >Back</a
        >
      </div>
    </form>

    {'' if response['data'] == None else f'<p style="text-align: center; padding-top: 5px">Record for {response["data"]["isbn"]} created</p>'}
  </div>
</body>
""")

def submit_book(query_string):
  query = parse_qs(query_string)
  response = {
     'data': None,
     'errors': {
        "title": None,
        "author": None,
        "isbn": None,
        "publisher": None,
        "year": None
     },
     'hasErrors': False
  }

  book = {
    "title": '' if query.get('title') is None else query.get('title')[0],
    "author": '' if query.get('author') is None else query.get('author')[0],
    "isbn": '' if query.get('isbn') is None else query.get('isbn')[0],
    "publisher": '' if query.get('publisher') is None else query.get('publisher')[0],
    "year": '' if query.get('year') is None else query.get('year')[0]
  }

  if not book['title']:
    response['hasErrors'] = True
    response['errors']['title'] = 'Title is required'
  
  if not book['author']:
    response['hasErrors'] = True
    response['errors']['author'] = 'Author is required'

  if not book['isbn']:
    response['hasErrors'] = True
    response['errors']['isbn'] = 'ISBN is required'
  
  if not book['publisher']:
    response['hasErrors'] = True
    response['errors']['publisher'] = 'Publisher is required'
  
  if not book['year']:
    response['hasErrors'] = True
    response['errors']['year'] = 'Year is required'

  if response['hasErrors']:
    return create_page(response)

  database = Database()
  cursor = database.connection.cursor()

  cursor.execute(f"SELECT COUNT(*) FROM Books WHERE ISBN = {book['isbn']}")
  
  if cursor.fetchall()[0][0] > 0:
    response['hasErrors'] = True
    response['errors']['isbn'] = 'Book with ISBN exists'
    return create_page(response)
  
  cursor.reset()
  cursor.execute(f"INSERT INTO Books (Title, Author, ISBN, Publisher, Year) VALUES ('{book['title']}', '{book['author']}', '{book['isbn']}', '{book['publisher']}', '{book['year']}');")
  
  response['data'] = book

  return create_page(response)
    

def not_found():
  return (HttpStatus.NOT_FOUND, "no tings found")


def application(environ: dict, start_response):
  match (environ.get('PATH_INFO'), environ.get('REQUEST_METHOD')):
      case ('/', 'GET'):
          (status, content) = home_page()
      case ('/books', 'GET'):
          (status, content) = search_page(environ.get('QUERY_STRING'))
      case ('/books/create', 'PUT'):
          (status, content) = submit_book(environ.get('QUERY_STRING'))
      case ('/books/create', 'GET'):
          query_string = environ.get('QUERY_STRING')
          (status, content) = create_page() if not query_string else submit_book(query_string)
      case _: 
          (status, content) = not_found()

  response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
  start_response(status, response_headers)

  yield content.encode('utf8')