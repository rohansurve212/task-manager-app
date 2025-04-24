/** @format */

import React from 'react'
import TaskItem from './TaskItem'

const TaskList = ({ tasks, onDelete, onEdit, onToggleComplete }) => {
  if (!tasks || tasks.length === 0) {
    return (
      <p className='no-tasks'>
        No tasks available. Add some tasks to get started!
      </p>
    )
  }

  return (
    <div className='task-list'>
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onDelete={onDelete}
          onEdit={onEdit}
          onToggleComplete={onToggleComplete}
        />
      ))}
    </div>
  )
}

export default TaskList
