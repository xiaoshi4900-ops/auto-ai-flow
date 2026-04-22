export const RUN_STATUSES = {
  pending: { label: 'Pending', type: 'info' as const },
  running: { label: 'Running', type: 'warning' as const },
  success: { label: 'Success', type: 'success' as const },
  failed: { label: 'Failed', type: 'danger' as const },
  cancelled: { label: 'Cancelled', type: 'info' as const },
} as const
