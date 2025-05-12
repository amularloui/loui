<template>
    <div>
        <h3 class="mt-4">All Transactions</h3>
        <div class="table-responsive">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Book</th>
                        <th>Borrow Date</th>
                        <th>Return Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="t in transactions" :key="t.id">
                        <td>{{ t.id }}</td>
                        <td>{{ t.user_username }}</td>
                        <td>{{ t.book_title }}</td>
                        <td>{{ t.borrow_date }}</td>
                        <td>{{ t.return_date || '—' }}</td>
                        <td>
                            <span :class="t.status === 'RETURNED' ? 'badge bg-success' : 'badge bg-warning'">
                                {{ t.status }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTransactions } from '../services/api'

const transactions = ref([])

async function fetchData() {
    const res = await getTransactions()
    transactions.value = res.data.map(t => ({
        ...t,
        user_username: t.user_username || t.user,
        book_title: t.book_title || 'N/A'
    }))
}

defineExpose({ fetchData })

onMounted(fetchData)
</script>
