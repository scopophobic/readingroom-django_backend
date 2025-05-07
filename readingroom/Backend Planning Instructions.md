# 📘 Reading Room — Backend Instructions

This document outlines the logic and backend flow for the Reading Room project, which is a book-centered social media platform. It is intended for developers working on the backend to understand how the system is designed and how to extend or debug it.

---

## 🚀 Project Overview

**Reading Room** is a Django-based backend for a platform where users can:
- Browse books (via Google Books API)
- Create posts about books or general reading thoughts
- Comment on posts
- Follow other readers
- Get AI-based recommendations (planned)
- Handle user authentication via JWT/OAuth

---

## 📚 Book Management

### 📥 Book Fetching

Currently, the system fetches book data from the **Google Books API** using `volumeId`. The retrieved data includes:
- Title
- Authors
- Description
- ISBN
- Publisher
- Cover image
- Genres (if available)
- Google Book ID

### ✅ To Do: Book Storage

Currently, the book is only fetched but **not stored**. Here's how to persist the book:

```python
def save_fetched_book(data):
    book, created = Book.objects.get_or_create(
        google_book_id=data['id'],
        defaults={
            "title": data["volumeInfo"].get("title", "Untitled")[:255],
            "authors": ", ".join(data["volumeInfo"].get("authors", []))[:512],
            "description": data["volumeInfo"].get("description", "") or "",
            "publication_date": extract_date(data["volumeInfo"].get("publishedDate")),
            "cover_image_url": data["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
            "isbn": extract_isbn(data["volumeInfo"]),
            "publisher": data["volumeInfo"].get("publisher", "")[:255],
        }
    )
    return book
```

**Note:** `extract_date()` and `extract_isbn()` are helper functions you’ll need to define to parse raw Google Books values.

---

## 📝 Posting System

### 🧵 Posting Types

There are **two types** of post creation:

#### 1. **From Book Page** (`/posts/create/<book_id>/`)
- Automatically links post to the book with the given `google_book_id`
- Prefills the book info if not already in DB (creates and saves it)
- Displays post form with a hidden or disabled book selector

#### 2. **From Home Page** (`/posts/create/`)
- User optionally selects a book (via dropdown/autocomplete/search)
- Allows general posts too (with no book selected)

### ✅ Post Form

Your `PostForm` should support:
- `content` (Text)
- `image` (Optional FileField/ImageField)
- `book` (ForeignKey optional)

Example:

```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🖼️ Image Upload Handling in Django

1. In your **model** (e.g., Post), use:

```python
image = models.ImageField(upload_to='posts/', blank=True, null=True)
```

2. In your **settings.py**:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

3. In your **project urls.py**:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

4. In your **form template**:

```html
<form method="POST" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Post">
</form>
```

5. In your **view**:

```python
if form.is_valid():
    post = form.save(commit=False)
    post.user = request.user
    if book:  # Book fetched from book_id or form input
        post.book = book
    post.save()
```

---

## 💬 Comments

- Each comment is linked to a `Post`
- Basic model:

```python
# posts/models.py

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

```

- Render comments under each post using `post.comments.all` in your templates.

---

## 📑 URL Patterns Overview

```txt
/posts/create/ — Create a general post (optional book)
/posts/create/<book_id>/ — Create a post for a specific book
/books/<book_id>/ — View book details
/posts/<post_id>/ — View a post and its comments
```

---

## 🔐 Authentication

- Currently uses `@login_required` decorators.
- Can be replaced or augmented with JWT/OAuth in the future for mobile or API access.
- Consider using Django AllAuth or djangorestframework-simplejwt for advanced cases.

---

## 🛠 Planned Improvements

- Book autocomplete or search on post creation form (using AJAX or JavaScript)
- AI-assisted tagging of book genres
- Image compression/resizing on upload
- Separate Book model admin for review/cleanup
- Add "trending posts", "most commented", or "recommended" sections

---

## ✅ Summary

| Feature                  | Status     |
|--------------------------|------------|
| Book fetching (Google)   | ✅ Done     |
| Book persistence         | ⏳ To do    |
| Post creation (2 ways)   | ✅ In prog  |
| Image upload             | ✅ Works    |
| Comments                 | ✅ Basic    |
| Book dropdown on post    | ⏳ To add   |

---

## 📂 Folder Structure (Important Files)

```txt
readingroom/
├── books/
│   └── models.py
│   └── views.py (Google Books fetch)
├── posts/
│   └── models.py (Post, Comment)
│   └── views.py (create_post, post_detail)
├── templates/
│   └── posts/
│       └── create_post.html
│       └── post_detail.html
├── media/         ← uploaded images
├── static/        ← CSS/JS
```

---

## 🧠 Tips

- Always truncate Google Books fields (like title, publisher) before saving.
- Use `ImageField` for uploads, not `FileField`.
- Use a rich text editor like `django-ckeditor` if you want formatting support in posts.
- For AJAX-based book search dropdown, use `Select2` or `Alpine.js`.

---