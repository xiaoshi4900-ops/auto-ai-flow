<template>
  <div class="reference-shell">
    <aside class="reference-sidebar glass-card" data-testid="reference-sidebar">
      <div class="brand">
        <p class="brand__kicker">AutoAiFlow UI Prototype</p>
        <h2>Reference Pages</h2>
        <span class="brand__badge">Design + Spec + Playwright</span>
      </div>
      <nav class="reference-nav">
        <RouterLink
          v-for="item in items"
          :key="item.to"
          :to="item.to"
          class="reference-nav__item"
          :class="{ 'reference-nav__item--active': route.path === item.to }"
        >
          <span class="reference-nav__dot" :style="{ background: item.color }"></span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>

    <main class="reference-main">
      <header class="reference-header glass-card">
        <div>
          <p class="reference-header__eyebrow">{{ eyebrow }}</p>
          <h1>{{ title }}</h1>
          <p class="reference-header__subtitle">{{ subtitle }}</p>
        </div>
        <div class="reference-header__meta">
          <div v-for="metric in metrics" :key="metric.label" class="metric-card">
            <span>{{ metric.label }}</span>
            <strong>{{ metric.value }}</strong>
          </div>
        </div>
      </header>

      <section class="reference-content">
        <slot />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

type NavItem = {
  to: string
  label: string
  color: string
}

type Metric = {
  label: string
  value: string
}

defineProps<{
  eyebrow: string
  title: string
  subtitle: string
  metrics: readonly Metric[]
  items: readonly NavItem[]
}>()

const route = useRoute()
</script>

<style scoped>
.reference-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 256px minmax(0, 1fr);
  gap: 20px;
  padding: 20px;
}

.reference-sidebar {
  padding: 18px;
  border-radius: 24px;
}

.brand {
  padding: 16px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(86, 240, 192, 0.14), rgba(60, 185, 255, 0.12));
  border: 1px solid rgba(86, 240, 192, 0.16);
}

.brand__kicker {
  margin: 0 0 8px;
  font-size: 11px;
  color: var(--accent-primary);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.brand h2 {
  margin: 0;
  font-size: 24px;
}

.brand__badge {
  display: inline-flex;
  margin-top: 10px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-secondary);
  font-size: 12px;
}

.reference-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 18px;
}

.reference-nav__item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  color: var(--text-secondary);
  text-decoration: none;
  border: 1px solid transparent;
}

.reference-nav__item:hover,
.reference-nav__item--active {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-strong);
}

.reference-nav__dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  flex: 0 0 auto;
}

.reference-main {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.reference-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 22px 24px;
  border-radius: 24px;
}

.reference-header__eyebrow {
  margin: 0 0 8px;
  color: var(--accent-secondary);
  font-size: 12px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.reference-header h1 {
  margin: 0;
  font-size: 32px;
}

.reference-header__subtitle {
  max-width: 760px;
  margin: 12px 0 0;
  color: var(--text-secondary);
}

.reference-header__meta {
  display: grid;
  grid-template-columns: repeat(3, minmax(110px, 1fr));
  gap: 10px;
  min-width: 360px;
}

.metric-card {
  padding: 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
}

.metric-card span {
  display: block;
  color: var(--text-muted);
  font-size: 12px;
}

.metric-card strong {
  display: block;
  margin-top: 8px;
  font-size: 22px;
}

.reference-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

@media (max-width: 1360px) {
  .reference-shell {
    grid-template-columns: 1fr;
  }

  .reference-header {
    flex-direction: column;
  }

  .reference-header__meta {
    min-width: 0;
  }
}
</style>
