import { ref, computed } from 'vue'

export function usePagination(defaultPageSize = 20) {
  const page = ref(1)
  const pageSize = ref(defaultPageSize)
  const total = ref(0)

  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

  function setPage(p: number) {
    page.value = p
  }

  function setTotal(t: number) {
    total.value = t
  }

  function reset() {
    page.value = 1
    total.value = 0
  }

  return { page, pageSize, total, totalPages, setPage, setTotal, reset }
}
