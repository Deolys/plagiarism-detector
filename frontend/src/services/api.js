import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const checkCode = async (code) => {
  try {
    const response = await api.post('/check', { code })
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      error.response?.data?.error || 
      'Failed to check code'
    )
  }
}

export const uploadFile = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      error.response?.data?.error || 
      'Failed to upload file'
    )
  }
}

export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    throw new Error('API health check failed')
  }
}

export default api

