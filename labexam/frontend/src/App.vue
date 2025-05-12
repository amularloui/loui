<template>
  <!-- Instagram-style Navbar -->
  <nav class="navbar navbar-expand-lg bg-white shadow-sm border-bottom" style="background: #fafafa;">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- Brand -->
      <a class="navbar-brand fw-bold gradient-text d-none d-lg-block" href="#">
        📚 Library System
      </a>

      <!-- Toggler -->
      <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>

    <!-- Navigation Links -->
    <div class="collapse navbar-collapse" id="navbarNav" ref="navbarRef">
      <ul class="navbar-nav ms-auto w-100 justify-content-lg-end text-center text-lg-start">
        <li class="nav-item">
          <a class="nav-link rounded-pill px-3 py-2" href="#"
            :class="{ active: view === 'books', 'active-nav': view === 'books' }"
            @click.prevent="changeView('books')">Books</a>
        </li>
        <li class="nav-item">
          <a class="nav-link rounded-pill px-3 py-2" href="#"
            :class="{ active: view === 'borrow', 'active-nav': view === 'borrow' }"
            @click.prevent="changeView('borrow')">Borrow</a>
        </li>
        <li class="nav-item">
          <a class="nav-link rounded-pill px-3 py-2" href="#"
            :class="{ active: view === 'return', 'active-nav': view === 'return' }"
            @click.prevent="changeView('return')">Return</a>
        </li>
        <li class="nav-item">
          <a class="nav-link rounded-pill px-3 py-2" href="#"
            :class="{ active: view === 'transactions', 'active-nav': view === 'transactions' }"
            @click.prevent="changeView('transactions')">Transactions</a>
        </li>
      </ul>
    </div>
  </nav>

  <component :is="currentComponent" ref="childRef" />
</template>



<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import BookList from './components/BookList.vue'
import BorrowForm from './components/BorrowForm.vue'
import ReturnForm from './components/ReturnForm.vue'
import TransactionTable from './components/TransactionTable.vue'

const view = ref('books')
const childRef = ref(null)
const navbarRef = ref(null)
let collapseInstance = null

const componentsMap = {
  books: BookList,
  borrow: BorrowForm,
  return: ReturnForm,
  transactions: TransactionTable
}

const currentComponent = computed(() => componentsMap[view.value])

onMounted(() => {
  // Initialize Bootstrap collapse instance
  if (window.bootstrap && navbarRef.value) {
    collapseInstance = new bootstrap.Collapse(navbarRef.value, {
      toggle: false
    })
  }
})

watch(view, async () => {
  await nextTick()
  childRef.value?.fetchData()

  // Collapse the navbar after navigation
  if (collapseInstance) {
    collapseInstance.hide()
  }
})

function changeView(val) {
  view.value = val
}
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-link {
  color: #555;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: #f0f0f0;
}

.active-nav {
  background: linear-gradient(135deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);
  color: white !important;
  font-weight: bold;
}
</style>

