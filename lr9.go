package main

import (
 "encoding/json"
 "fmt"
 "html/template"
 "net/http"
 "strings"
 "time"

 "github.com/go-chi/chi/v5"
 "github.com/go-chi/chi/v5/middleware"
 "golang.org/x/time/rate"
)

type User struct {
 Username string `json:"username"`
}

var users = make(map[string]User)

// Шаблон HTML для главной страницы
var indexHTML = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Management</title>
</head>
<body>
    <h1>User Management</h1>
    <button onclick="viewUsers()">View Users</button>
    <div id="userList"></div>
    <h2>Add User</h2>
    <input type="text" id="username" placeholder="Enter username">
    <button onclick="addUser()">Add User</button>
    <h2>Delete User</h2>
    <input type="text" id="deleteUsername" placeholder="Enter username to delete">
    <button onclick="deleteUser()">Delete User</button>
    <script>
        function viewUsers() {
            fetch('/users')
                .then(response => response.json())
                .then(data => {
                    let userList = '<h3>Users:</h3><ul>';
                    data.forEach(user => {
                        userList += '<li>' + user.username + '</li>';
                    });
                    userList += '</ul>';
                    document.getElementById('userList').innerHTML = userList;
                })
                .catch(error => console.error('Error:', error));
        }

        function addUser() {
            const username = document.getElementById('username').value;
            fetch('/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username })
            })
            .then(response => response.text())
            .then(data => {
                alert(data);
                viewUsers();
            })
            .catch(error => console.error('Error:', error));
        }

        function deleteUser() {
            const username = document.getElementById('deleteUsername').value;
            fetch('/users/' + username, {
                method: 'DELETE'
            })
            .then(response => response.text())
            .then(data => {
                alert(data);
                viewUsers();
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
`

// Basic Auth middleware
func basicAuth(next http.Handler) http.Handler {
 return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
  username, password, ok := r.BasicAuth()
  if !okror));
        }
    </scripassword != "password" {
   w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
   http.Error(w, "Unauthorized", http.StatusUnauthorized)
   return
  }
  next.ServeHTTP(w, r)
 })
}

// Rate limiter middleware
func rateLimiter(rps int, burst int) func(http.Handler) http.Handler {
 limiter := rate.NewLimiter(rate.Limit(rps), burst)
 return func(next http.Handler) http.Handler {
  return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
   if !limiter.Allow() {
    http.Error(w, "Too Many Requests", http.StatusTooManyRequests)
    return
   }
   next.ServeHTTP(w, r)
  })
 })
}

func main() {
 r := chi.NewRouter()
 r.Use(middleware.Logger)
 r.Use(middleware.Recoverer)

 // Добавляем middleware для Basic Auth и Rate Limiter
 r.Use(basicAuth)
 r.Use(rateLimiter(2, 5)) // 2 запроса в секунду, максимум 5 в буфере

 // Главная страница
 r.Get("/", func(w http.ResponseWriter, r *http.Request) {
  tmpl := template.New("index")
  tmpl, _ = tmpl.Parse(indexHTML)
  tmpl.Execute(w, nil)
 })

 // Маршруты для пользователей
 r.Route("/users", func(r chi.Router) {
  r.Get("/", getUsers)
  r.Post("/", addUser)
  r.Delete("/{username}", deleteUser)
 })

 // Запуск сервера
 fmt.Println("Server running at http://localhost:8080")
 if err := http.ListenAndServe(":8080", r); err != nil {
  panic(err)
 }
}

func getUsers(w http.ResponseWriter, _ *http.Request) {
 w.Header().Set("Content-Type", "application/json")

userList := make([]User, 0, len(users))
 for _, user := range users {
  userList = append(userList, user)
 }
 json.NewEncoder(w).Encode(userList)
}

func addUser(w http.ResponseWriter, r *http.Request) {
 var newUser User
 if err := json.NewDecoder(r.Body).Decode(&newUser); err != nil {
  http.Error(w, err.Error(), http.StatusBadRequest)
  return
 }
 if newUser.Username == "" {
  http.Error(w, "Username cannot be empty", http.StatusBadRequest)
  return
 }
 users[newUser.Username] = newUser
 fmt.Fprintf(w, "User %s added", newUser.Username)
}

func deleteUser(w http.ResponseWriter, r *http.Request) {
 username := chi.URLParam(r, "username")
 if _, exists := users[username]; exists {
  delete(users, username)
  fmt.Fprintf(w, "User %s deleted", username)
 } else {
  http.Error(w, "User not found", http.StatusNotFound)
 }
}
