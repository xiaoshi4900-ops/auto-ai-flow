<template>
  <div class="page-header">
    <h2>{{ title }}</h2>
    <el-button v-if="addText" type="primary" :data-testid="buttonTestId" @click="$emit('add')">{{ addText }}</el-button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ title: string; addText?: string }>()
defineEmits<{ add: [] }>()

const buttonTestId = computed(() => {
  if (props.title === 'Projects') return 'project-create-button'
  if (props.title === 'Agents') return 'agent-create-button'
  if (props.title === 'Workflows') return 'workflow-create-button'
  return 'create-button'
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-header h2 {
  margin: 0;
}
</style>
