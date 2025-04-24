/** @format */

import React, { useState } from 'react'
import TaskForm from './TaskForm'

const TaskItem = ({ task, onDelete, onEdit, onToggleComplete }) => {
  const [isEditing, setIsEditing] = useState(false)

  const handleEdit = () => {
    setIsEditing(true)
  }

  const handleUpdate = (updatedTask) => {
    onEdit(task.id, updatedTask)
    setIsEditing(false)
  }

  const handleToggleComplete = () => {
    onToggleComplete(task.id, { is_completed: !task.is_completed })
  }

  // Format the date
  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    return new Date(dateString).toLocaleDateString(undefined, options)
  }

  if (isEditing) {
    return (
      <div className='task-item editing'>
        <h3>Edit Task</h3>
        <TaskForm onSubmit={handleUpdate} initialData={task} />
        <button
          onClick={() => setIsEditing(false)}
          className='btn btn-secondary'
        >
          Cancel
        </button>
      </div>
    )
  }

  return (
    <div className={`task-item ${task.is_completed ? 'completed' : ''}`}>
      <div className='task-header'>
        <h3>{task.title}</h3>
        <div className='task-controls'>
          <button onClick={handleEdit} className='btn btn-edit'>
            Edit
          </button>
          <button onClick={() => onDelete(task.id)} className='btn btn-delete'>
            Delete
          </button>
        </div>
      </div>

      <div className='task-content'>
        <p className='task-description'>{task.description}</p>
        <div className='task-meta'>
          <div className='task-dates'>
            <span>Created: {formatDate(task.created_at)}</span>
            {task.updated_at && (
              <span>Updated: {formatDate(task.updated_at)}</span>
            )}
          </div>
          <div className='task-completion'>
            <label className='checkbox-container'>
              <input
                type='checkbox'
                checked={task.is_completed}
                onChange={handleToggleComplete}
              />
              <span className='checkmark'></span>
              {task.is_completed ? 'Completed' : 'Mark as completed'}
            </label>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TaskItem
