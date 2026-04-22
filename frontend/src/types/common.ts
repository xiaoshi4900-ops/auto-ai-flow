export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T = unknown> {
  total: number
  page: number
  page_size: number
  items: T[]
}
