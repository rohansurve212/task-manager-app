/** @format */

import axios from 'axios'

// Get the API URL from environment variables
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'
const API_PREFIX = '/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API methods for tasks
const taskService = {
  // Get all tasks
  getAllTasks: async () => {
    try {
      const response = await apiClient.get(`${API_PREFIX}/tasks`)
      return response.data
    } catch (error) {
      console.error('Error fetching tasks:', error)
      throw error
    }
  },

  // Get a specific task
  getTask: async (id) => {
    try {
      const response = await apiClient.get(`${API_PREFIX}/tasks/${id}`)
      return response.data
    } catch (error) {
      console.error(`Error fetching task ${id}:`, error)
      throw error
    }
  },

  // Create a new task
  createTask: async (taskData) => {
    try {
      const response = await apiClient.post(`${API_PREFIX}/tasks`, taskData)
      return response.data
    } catch (error) {
      console.error('Error creating task:', error)
      throw error
    }
  },

  // Update a task
  updateTask: async (id, taskData) => {
    try {
      const response = await apiClient.put(
        `${API_PREFIX}/tasks/${id}`,
        taskData
      )
      return response.data
    } catch (error) {
      console.error(`Error updating task ${id}:`, error)
      throw error
    }
  },

  // Delete a task
  deleteTask: async (id) => {
    try {
      await apiClient.delete(`${API_PREFIX}/tasks/${id}`)
      return true
    } catch (error) {
      console.error(`Error deleting task ${id}:`, error)
      throw error
    }
  },
}

export default taskService
