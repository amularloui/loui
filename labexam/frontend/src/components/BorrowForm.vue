<template>
    <div class="d-flex justify-content-center mt-5">
        <div class="card w-100" style="max-width: 600px;">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">Borrow a Book</h5>
            </div>

            <div class="card-body p-4">
                <form @submit.prevent="borrowBook">
                    <!-- User Select -->
                    <div class="form-floating mb-3">
                        <select v-model.number="form.user" class="form-select" id="userSelect" required>
                            <option value="" disabled>Select user…</option>
                            <option v-for="u in users" :key="u.id" :value="u.id">
                                {{ u.username }}
                            </option>
                        </select>
                        <label for="userSelect">User</label>
                    </div>

                    <!-- Book Select -->
                    <div class="form-floating mb-3">
                        <select v-model.number="form.book" class="form-select" id="bookSelect" required>
                            <option value="" disabled>Select book…</option>
                            <option v-for="b in books" :key="b.id" :value="b.id" :disabled="b.copies_available < 1">
                                {{ b.title }} ({{ b.copies_available }} avail)
                            </option>
                        </select>
                        <label for="bookSelect">Book</label>
                    </div>

                    <!-- Borrow Date -->
                    <div class="form-floating mb-3">
                        <input v-model="form.borrow_date" type="date" class="form-control" id="borrowDate" :max="today"
                            required />
                        <label for="borrowDate">Borrow Date</label>
                    </div>

                    <!-- Messages -->
                    <transition name="fade">
                        <div v-if="error" class="alert alert-danger fade show">
                            {{ error }}
                        </div>
                    </transition>
                    <transition name="fade">
                        <div v-if="success" class="alert alert-success fade show">
                            {{ success }}
                        </div>
                    </transition>
                </form>
            </div>

            <div class="card-footer text-end">
                <button type="submit" class="btn btn-success" @click.prevent="borrowBook">
                    Borrow
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getUsers, getBooks, borrowBook as apiBorrowBook } from '@/services/api'

const users = ref([])
const books = ref([])
const form = ref({ user: null, book: null, borrow_date: '' })
const error = ref('')
const success = ref('')

// today in YYYY-MM-DD for max attribute
const today = computed(() => new Date().toISOString().slice(0, 10))

async function fetchData() {
    const [uRes, bRes] = await Promise.all([getUsers(), getBooks()])
    users.value = uRes.data
    books.value = bRes.data
}

// expose fetchData to parent
defineExpose({ fetchData })

onMounted(() => {
    form.value.borrow_date = today.value
    fetchData()
})

async function borrowBook() {
    // reset messages
    error.value = ''
    success.value = ''

    try {
        await apiBorrowBook(form.value)
        success.value = 'Book borrowed successfully!'
        // reset form
        form.value.borrow_date = today.value
        form.value.user = null
        form.value.book = null
        await fetchData()
    } catch (err) {
        error.value = err.response?.data?.error || 'Unable to borrow'
    }
}
</script>

<style scoped>
/* Fade transition, tied to the "fade" name in <transition> */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
