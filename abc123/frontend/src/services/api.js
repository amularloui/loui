import axios from 'axios'

// Create an Axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' }
})

// --- Users ---
export function getUsers() {
  return api.get('/users/')
}

export function createUser(userData) {
  // userData: { username, password, first_name, last_name, email }
  return api.post('/users/', userData)
}

export function updateUser(id, userData) {
  return api.put(`/users/${id}/`, userData)
}

export function deleteUser(id) {
  return api.delete(`/users/${id}/`)
}

// --- Books ---
export function getBooks() {
  return api.get('/books/')
}

export function createBook(bookData) {
  // bookData: { title, author, isbn, copies_available }
  return api.post('/books/', bookData)
}

export function updateBook(id, bookData) {
  return api.put(`/books/${id}/`, bookData)
}

export function deleteBook(id) {
  return api.delete(`/books/${id}/`)
}

// --- Borrow Transactions ---
export function getTransactions() {
  return api.get('/transactions/')
}

export function borrowBook(transactionData) {
  // transactionData: { user: userId, book: bookId, borrow_date: 'YYYY-MM-DD' }
  return api.post('/borrow/', transactionData)
}

// --- Return Book ---
export function returnBook(txnId, returnDate) {
  // returnDate: 'YYYY-MM-DD'
  return api.post(`/return/${txnId}/`, { return_date: returnDate })
}

// If you still need the raw axios instance:
export default api
