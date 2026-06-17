<script setup>
import { ref, computed } from 'vue'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { api } from '../api'

const { selectedLocation, selectedCategory } = useFilters()
const { t, currentLocale } = useI18n()

const budget = ref(50000)
const recommendations = ref([])
const loading = ref(false)
const error = ref(null)
const hasCalculated = ref(false)

const totalCost = computed(() =>
  recommendations.value.reduce((sum, item) => sum + item.total_cost, 0)
)

const remainingBudget = computed(() => budget.value - totalCost.value)

const formatCurrency = (num) => {
  const locale = currentLocale.value === 'ja' ? 'ja-JP' : 'en-US'
  const currency = currentLocale.value === 'ja' ? 'JPY' : 'USD'
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    maximumFractionDigits: 2
  }).format(num)
}

const priorityClass = (priority) => {
  if (priority === 'high') return 'badge high'
  if (priority === 'medium') return 'badge medium'
  return 'badge low'
}

const priorityLabel = (priority) => {
  if (priority === 'high') return t('priority.high')
  if (priority === 'medium') return t('priority.medium')
  return t('priority.low')
}

const trendClass = (trend) => {
  if (trend === 'increasing') return 'badge increasing'
  if (trend === 'decreasing') return 'badge decreasing'
  return 'badge stable'
}

const trendLabel = (trend) => {
  if (trend === 'increasing') return t('trends.increasing')
  if (trend === 'decreasing') return t('trends.decreasing')
  return t('trends.stable')
}

const calculate = async () => {
  loading.value = true
  error.value = null
  hasCalculated.value = true
  try {
    const filters = {}
    if (selectedLocation.value !== 'all') filters.warehouse = selectedLocation.value
    if (selectedCategory.value !== 'all') filters.category = selectedCategory.value
    recommendations.value = await api.getRestockingRecommendations(budget.value, filters)
  } catch (err) {
    console.error('Failed to load restocking recommendations:', err)
    error.value = t('restocking.error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <!-- Budget Input -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">{{ t('restocking.budgetInput') }}</h3>
      </div>
      <div class="budget-form">
        <div class="budget-field">
          <label class="budget-label" for="budget-input">{{ t('restocking.budgetCeiling') }}</label>
          <div class="budget-input-row">
            <input
              id="budget-input"
              v-model.number="budget"
              type="number"
              min="0"
              step="1000"
              class="budget-input"
              :placeholder="t('restocking.budgetPlaceholder')"
            />
            <button class="calculate-btn" :disabled="loading" @click="calculate">
              <span v-if="loading">{{ t('common.loading') }}</span>
              <span v-else>{{ t('restocking.calculate') }}</span>
            </button>
          </div>
        </div>
        <p class="budget-hint">{{ t('restocking.budgetHint') }}</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>

    <!-- Error -->
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Results -->
    <template v-else-if="hasCalculated">
      <!-- Summary Bar -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">{{ t('restocking.totalItems') }}</div>
          <div class="stat-value">{{ recommendations.length }}</div>
        </div>
        <div class="stat-card" :class="totalCost > 0 ? 'info' : ''">
          <div class="stat-label">{{ t('restocking.totalEstimatedCost') }}</div>
          <div class="stat-value">{{ formatCurrency(totalCost) }}</div>
        </div>
        <div class="stat-card" :class="remainingBudget < 0 ? 'danger' : 'success'">
          <div class="stat-label">{{ t('restocking.remainingBudget') }}</div>
          <div class="stat-value">{{ formatCurrency(remainingBudget) }}</div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="recommendations.length === 0" class="card empty-state">
        <div class="empty-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <p class="empty-title">{{ t('restocking.emptyTitle') }}</p>
        <p class="empty-desc">{{ t('restocking.emptyDescription') }}</p>
      </div>

      <!-- Recommendations Table -->
      <div v-else class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendations') }}</h3>
          <span class="item-count">{{ recommendations.length }} {{ t('common.items') }}</span>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.itemName') }}</th>
                <th>{{ t('restocking.table.category') }}</th>
                <th>{{ t('restocking.table.warehouse') }}</th>
                <th>{{ t('restocking.table.currentStock') }}</th>
                <th>{{ t('restocking.table.reorderPoint') }}</th>
                <th>{{ t('restocking.table.recommendedQty') }}</th>
                <th>{{ t('restocking.table.unitCost') }}</th>
                <th>{{ t('restocking.table.totalCost') }}</th>
                <th>{{ t('restocking.table.priority') }}</th>
                <th>{{ t('restocking.table.demandTrend') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recommendations" :key="item.sku + '-' + item.warehouse">
                <td><strong>{{ item.sku }}</strong></td>
                <td>{{ item.item_name }}</td>
                <td>{{ item.category }}</td>
                <td>{{ item.warehouse }}</td>
                <td>{{ item.current_stock }}</td>
                <td>{{ item.reorder_point }}</td>
                <td><strong>{{ item.recommended_qty }}</strong></td>
                <td>{{ formatCurrency(item.unit_cost) }}</td>
                <td>{{ formatCurrency(item.total_cost) }}</td>
                <td>
                  <span :class="priorityClass(item.priority)">
                    {{ priorityLabel(item.priority) }}
                  </span>
                </td>
                <td>
                  <span :class="trendClass(item.demand_trend)">
                    {{ trendLabel(item.demand_trend) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.restocking {
  padding: 0;
}

.budget-form {
  padding: 0.25rem 0;
}

.budget-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 480px;
}

.budget-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.budget-input-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.budget-input {
  flex: 1;
  padding: 0.625rem 0.875rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.938rem;
  color: #0f172a;
  background: #fff;
  transition: border-color 0.15s ease;
  outline: none;
}

.budget-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.calculate-btn {
  padding: 0.625rem 1.5rem;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
  white-space: nowrap;
}

.calculate-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.calculate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.budget-hint {
  font-size: 0.813rem;
  color: #94a3b8;
  margin-top: 0.25rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-icon {
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 0.375rem;
}

.empty-desc {
  font-size: 0.875rem;
  color: #64748b;
}

.item-count {
  font-size: 0.813rem;
  color: #64748b;
  font-weight: 500;
  background: #f1f5f9;
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
}
</style>
