<template>
  <div class="container py-4" style="background-color: #fafafa;">
    <h2 class="mb-4 text-center fw-bold" style="color: #262626;">📚 Book List</h2>
    
    <div class="d-flex justify-content-end mb-3">
      <button class="btn btn-gradient btn-lg rounded-pill shadow-sm" @click="openAddModal">
        ➕ Add Book
      </button>
    </div>

    <div class="table-responsive shadow-sm rounded-4 overflow-hidden">
      <table class="table table-bordered table-hover align-middle mb-0">
        <thead class="table-light text-center">
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Copies Available</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id" class="text-center">
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.copies_available }}</td>
            <td>
              <button class="btn btn-sm btn-outline-warning me-2 rounded-pill" @click="editBook(book)">
                ✏️ Edit
              </button>
              <button class="btn btn-sm btn-outline-danger rounded-pill"
                :disabled="hasActiveBorrow(book.id)" @click="deleteBook(book.id)">
                🗑️ Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Teleport backdrop -->
    <teleport to="body" v-if="isModalOpen">
      <div class="modal-backdrop fade show"></div>
    </teleport>

    <!-- Add/Edit Modal -->
    <div v-if="isModalOpen" class="modal fade show d-block" tabindex="-1" @click.self="closeModal" aria-modal="true" role="dialog">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">
          <form @submit.prevent="saveBook" novalidate>
            <div class="modal-header border-0">
              <h5 class="modal-title fw-semibold">
                {{ editingBook.id ? 'Edit Book' : 'Add Book' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>

            <div class="modal-body">
              <!-- TITLE -->
              <div class="mb-3">
                <label class="form-label">Title</label>
                <input v-model="editingBook.title" type="text" class="form-control rounded-3"
                  :class="{ 'is-invalid': errors.title }" />
                <div class="invalid-feedback">{{ errors.title?.[0] }}</div>
              </div>

              <!-- AUTHOR -->
              <div class="mb-3">
                <label class="form-label">Author</label>
                <input v-model="editingBook.author" type="text" class="form-control rounded-3"
                  :class="{ 'is-invalid': errors.author }" />
                <div class="invalid-feedback">{{ errors.author?.[0] }}</div>
              </div>

              <!-- ISBN -->
              <div class="mb-3">
                <label class="form-label">ISBN</label>
                <input v-model="editingBook.isbn" type="text" class="form-control rounded-3"
                  :class="{ 'is-invalid': errors.isbn }" />
                <div class="invalid-feedback">{{ errors.isbn?.[0] }}</div>
              </div>

              <!-- COPIES AVAILABLE -->
              <div class="mb-3">
                <label class="form-label">Copies Available</label>
                <input v-model.number="editingBook.copies_available" type="number" min="0"
                  class="form-control rounded-3" :class="{ 'is-invalid': errors.copies_available }" />
                <div class="invalid-feedback">{{ errors.copies_available?.[0] }}</div>
              </div>
            </div>

            <div class="modal-footer border-0">
              <button type="submit" class="btn btn-gradient rounded-pill">
                💾 Save
              </button>
              <button type="button" class="btn btn-outline-secondary rounded-pill" @click="closeModal">
                ❌ Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import {
    getBooks,
    getTransactions,
    createBook,
    updateBook,
    deleteBook as apiDeleteBook
} from '../services/api'

const books = ref([])
const transactions = ref([])
const editingBook = ref({})
const isModalOpen = ref(false)
const errors = ref({})

async function fetchData() {
    const [bRes, tRes] = await Promise.all([
        getBooks(),
        getTransactions()
    ])
    books.value = bRes.data
    transactions.value = tRes.data
}
defineExpose({ fetchData })
onMounted(fetchData)

function openAddModal() {
    editingBook.value = { title: '', author: '', isbn: '', copies_available: 1 }
    errors.value = {}
    isModalOpen.value = true
}

function editBook(book) {
    editingBook.value = { ...book }
    errors.value = {}
    isModalOpen.value = true
}

function closeModal() {
    isModalOpen.value = false
}

async function saveBook() {
    // Front-end sanity check
    if (editingBook.value.copies_available < 0) {
        errors.value = { copies_available: ['Invalid. Cannot be negative'] }
        return
    }

    try {
        if (editingBook.value.id) {
            await updateBook(editingBook.value.id, editingBook.value)
        } else {
            await createBook(editingBook.value)
        }
        await fetchData()
        closeModal()
    } catch (err) {
        if (err.response?.status === 400 || err.response?.status === 422) {
            errors.value = err.response.data
        } else {
            alert('An unexpected error occurred.')
        }
    }
}

async function deleteBook(id) {
    if (confirm('Are you sure you want to delete this book?')) {
        await apiDeleteBook(id)
        await fetchData()
    }
}

function hasActiveBorrow(bookId) {
    return transactions.value.some(
        txn => txn.book === bookId && txn.status === 'BORROWED'
    )
}
</script>

<style scoped>
.btn-gradient {
  background: linear-gradient(135deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);
  color: white;
  border: none;
  transition: background 0.3s ease;
}
.btn-gradient:hover {
  filter: brightness(1.1);
  color: white;
}
</style>

