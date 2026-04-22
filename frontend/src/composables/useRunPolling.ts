import { ref, onUnmounted } from 'vue'
import type { Ref } from 'vue'

export function useRunPolling(runId: Ref<number | null>, intervalMs = 3000) {
  const status = ref<string | null>(null)
  const isPolling = ref(false)
  let timer: ReturnType<typeof setInterval> | null = null

  async function poll() {
    if (!runId.value) return
    try {
      const { apiGet } = await import('@/api/client')
      const data = await apiGet<{ status: string }>(`/runs/${runId.value}`)
      status.value = data.status
      if (data.status === 'success' || data.status === 'failed' || data.status === 'cancelled') {
        stop()
      }
    } catch {
      stop()
    }
  }

  function start() {
    if (timer) return
    isPolling.value = true
    poll()
    timer = setInterval(poll, intervalMs)
  }

  function stop() {
    isPolling.value = false
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onUnmounted(stop)

  return { status, isPolling, start, stop }
}
