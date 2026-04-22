<template>
  <el-tag :type="statusConfig.type" effect="plain">{{ statusConfig.label }}</el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RUN_STATUSES } from '@/constants/statuses'

const props = defineProps<{ status: string }>()
const statusConfig = computed(() => RUN_STATUSES[props.status as keyof typeof RUN_STATUSES] || { label: props.status, type: 'info' as const })
</script>
