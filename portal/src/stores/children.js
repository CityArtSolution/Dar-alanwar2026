import { defineStore } from 'pinia'
import { ref } from 'vue'
import { childrenApi, attendanceApi } from '@/services/api'

export const useChildrenStore = defineStore('children', () => {
  const children = ref([])
  const selectedChild = ref(null)
  const loading = ref(false)

  async function fetchChildren() {
    loading.value = true
    try {
      const { data } = await childrenApi.getAll()
      children.value = data.children || []
    } catch (err) {
      console.error('Failed to fetch children:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchChildDetail(id) {
    loading.value = true
    try {
      const { data } = await childrenApi.getDetail(id)
      selectedChild.value = data
    } catch (err) {
      console.error('Failed to fetch child detail:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchAttendanceSummary(id) {
    try {
      const { data } = await attendanceApi.getSummary(id)
      return data
    } catch (err) {
      console.error('Failed to fetch attendance:', err)
      return null
    }
  }

  return {
    children, selectedChild, loading,
    fetchChildren, fetchChildDetail, fetchAttendanceSummary,
  }
})
