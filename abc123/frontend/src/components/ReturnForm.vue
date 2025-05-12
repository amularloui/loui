<template>
    <div class="d-flex justify-content-center mt-5">
        <div class="card w-100" style="max-width: 600px;">
            <!-- Green header like Borrow form -->
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">Return a Book</h5>
            </div>

            <div class="card-body p-4">
                <form @submit.prevent="returnBook">
                    <!-- Transaction Select -->
                    <div class="form-floating mb-3">
                        <select v-model.number="form.txnId" class="form-select" id="txnSelect" required>
                            <option value="" disabled>Select a borrowed book…</option>
                            <option v-for="t in activeTxns" :key="t.id" :value="t.id">
                                {{ t.user_username }} – {{ t.book_title }}
                            </option>
                        </select>
                        <label for="txnSelect">Borrowed Book</label>
                    </div>

                    <!-- Return Date -->
                    <div class="form-floating mb-3">
                        <input v-model="form.return_date" type="date" class="form-control" id="returnDate" :min="today"
                            required />
                        <label for="returnDate">Return Date</label>
                    </div>

                    <!-- Fade Alerts -->
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

            <!-- Green button like Borrow form -->
            <div class="card-footer text-end">
                <button type="submit" class="btn btn-success" @click.prevent="returnBook">
                    Return
                </button>
            </div>
        </div>
    </div>

    <!-- Currently Borrowed List -->
    <div class="container mt-4">
        <h3>Currently Borrowed</h3>
        <ul class="list-group">
            <li v-for="t in activeTxns" :key="t.id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>{{ t.user_username }}</strong> has
                    <em>{{ t.book_title }}</em>
                </div>
                <small class="text-muted">{{ t.borrow_date }}</small>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getTransactions, returnBook as apiReturn } from '@/services/api'

const transactions = ref([])
const form = ref({ txnId: null, return_date: '' })
const error = ref('')
const success = ref('')

const today = computed(() => new Date().toISOString().slice(0, 10))

async function fetchData() {
    const res = await getTransactions()
    transactions.value = res.data
}

defineExpose({ fetchData })

onMounted(() => {
    form.value.return_date = today.value
    fetchData()
})

const activeTxns = computed(() =>
    transactions.value.filter(t => t.status === 'BORROWED')
)

async function returnBook() {
    error.value = ''
    success.value = ''
    if (!form.value.txnId) return

    try {
        await apiReturn(form.value.txnId, form.value.return_date)
        success.value = 'Book returned successfully!'
        form.value.txnId = null
        form.value.return_date = today.value
        await fetchData()
    } catch (err) {
        error.value = err.response?.data?.detail || 'Unable to return'
    }
}
</script>

<style scoped>
.card {
    min-width: 300px;
}

/* Fade transition used in <transition name="fade"> */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
