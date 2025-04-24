/** @format */

import React, { useState, useEffect } from 'react'
import './App.css'
import TaskForm from './components/TaskForm'
import TaskList from './components/TaskList'
import taskService from './services/api'

function App() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    try {
      setLoading(true)
      const data = await taskService.getAllTasks()
      setTasks(data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch tasks. Please try again later.')
      console.error('Error fetching tasks:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTask = async (taskData) => {
    try {
      const newTask = await taskService.createTask(taskData)
      setTasks([...tasks, newTask])
    } catch (err) {
      setError('Failed to create task. Please try again.')
      console.error('Error creating task:', err)
    }
  }

  const handleUpdateTask = async (id, taskData) => {
    try {
      const updatedTask = await taskService.updateTask(id, taskData)
      setTasks(tasks.map((task) => (task.id === id ? updatedTask : task)))
    } catch (err) {
      setError('Failed to update task. Please try again.')
      console.error('Error updating task:', err)
    }
  }

  const handleDeleteTask = async (id) => {
    try {
      await taskService.deleteTask(id)
      setTasks(tasks.filter((task) => task.id !== id))
    } catch (err) {
      setError('Failed to delete task. Please try again.')
      console.error('Error deleting task:', err)
    }
  }

  const handleToggleComplete = async (id, taskData) => {
    await handleUpdateTask(id, taskData)
  }

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>Task Manager</h1>
        <p>A simple CRUD application with FastAPI and React</p>
      </header>

      <main className='App-main'>
        <section className='form-section'>
          <h2>Add New Task</h2>
          <TaskForm onSubmit={handleCreateTask} />
        </section>

        {error && <div className='error-message'>{error}</div>}

        <section className='list-section'>
          <h2>Your Tasks</h2>
          {loading ? (
            <p className='loading'>Loading tasks...</p>
          ) : (
            <TaskList
              tasks={tasks}
              onDelete={handleDeleteTask}
              onEdit={handleUpdateTask}
              onToggleComplete={handleToggleComplete}
            />
          )}
        </section>
      </main>

      <footer className='App-footer'>
        <p>&copy; {new Date().getFullYear()} Task Manager App</p>
      </footer>
    </div>
  )
}

export default App
