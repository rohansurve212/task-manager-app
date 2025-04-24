/** @format */

import React, { useState } from 'react'

const TaskForm = ({ onSubmit, initialData = null }) => {
  const [task, setTask] = useState({
    title: initialData?.title || '',
    description: initialData?.description || '',
    is_completed: initialData?.is_completed || false,
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setTask({
      ...task,
      [name]: type === 'checkbox' ? checked : value,
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(task)

    // Only clear form if it's a new task
    if (!initialData) {
      setTask({
        title: '',
        description: '',
        is_completed: false,
      })
    }
  }

  return (
    <form onSubmit={handleSubmit} className='task-form'>
      <div className='form-group'>
        <label htmlFor='title'>Title:</label>
        <input
          type='text'
          id='title'
          name='title'
          value={task.title}
          onChange={handleChange}
          placeholder='Enter task title'
          required
          className='form-control'
        />
      </div>

      <div className='form-group'>
        <label htmlFor='description'>Description:</label>
        <textarea
          id='description'
          name='description'
          value={task.description || ''}
          onChange={handleChange}
          placeholder='Enter task description'
          className='form-control'
          rows='3'
        />
      </div>

      {initialData && (
        <div className='form-group checkbox'>
          <label htmlFor='is_completed'>
            <input
              type='checkbox'
              id='is_completed'
              name='is_completed'
              checked={task.is_completed}
              onChange={handleChange}
            />
            Completed
          </label>
        </div>
      )}

      <button type='submit' className='btn btn-primary'>
        {initialData ? 'Update Task' : 'Add Task'}
      </button>
    </form>
  )
}

export default TaskForm
