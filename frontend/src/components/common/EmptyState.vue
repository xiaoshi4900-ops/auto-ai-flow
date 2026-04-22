<template>
  <div class="empty-state">
    <el-empty :description="description" />
  </div>
</template>

<script setup lang="ts">
defineProps<{ description?: string }>()
</script>

<style scoped>
.empty-state {
  padding: 40px;
  text-align: center;
}
</style>
