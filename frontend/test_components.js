/** @format */

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import TaskForm from './src/components/TaskForm'
import TaskItem from './src/components/TaskItem'
import TaskList from './src/components/TaskList'

// Mock data
const mockTask = {
  id: 1,
  title: 'Test Task',
  description: 'This is a test task',
  is_completed: false,
  created_at: new Date().toISOString(),
}

const mockTasks = [
  mockTask,
  {
    id: 2,
    title: 'Another Task',
    description: 'This is another test task',
    is_completed: true,
    created_at: new Date().toISOString(),
  },
]

// TaskForm tests
describe('TaskForm component', () => {
  test('renders empty form when no initial data is provided', () => {
    render(<TaskForm onSubmit={() => {}} />)

    expect(screen.getByLabelText(/title/i)).toHaveValue('')
    expect(screen.getByLabelText(/description/i)).toHaveValue('')
    expect(screen.getByRole('button')).toHaveTextContent('Add Task')
  })

  test('renders form with initial data when provided', () => {
    render(<TaskForm onSubmit={() => {}} initialData={mockTask} />)

    expect(screen.getByLabelText(/title/i)).toHaveValue('Test Task')
    expect(screen.getByLabelText(/description/i)).toHaveValue(
      'This is a test task'
    )
    expect(screen.getByLabelText(/completed/i)).not.toBeChecked()
    expect(screen.getByRole('button')).toHaveTextContent('Update Task')
  })

  test('calls onSubmit with form data when submitted', () => {
    const handleSubmit = jest.fn()
    render(<TaskForm onSubmit={handleSubmit} />)

    fireEvent.change(screen.getByLabelText(/title/i), {
      target: { value: 'New Task' },
    })

    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: 'New task description' },
    })

    fireEvent.click(screen.getByRole('button'))

    expect(handleSubmit).toHaveBeenCalledWith({
      title: 'New Task',
      description: 'New task description',
      is_completed: false,
    })
  })
})

// TaskItem tests
describe('TaskItem component', () => {
  test('renders task information correctly', () => {
    render(
      <TaskItem
        task={mockTask}
        onDelete={() => {}}
        onEdit={() => {}}
        onToggleComplete={() => {}}
      />
    )

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('This is a test task')).toBeInTheDocument()
    expect(screen.getByText(/Mark as completed/i)).toBeInTheDocument()
  })

  test('shows completed status when task is completed', () => {
    const completedTask = { ...mockTask, is_completed: true }
    render(
      <TaskItem
        task={completedTask}
        onDelete={() => {}}
        onEdit={() => {}}
        onToggleComplete={() => {}}
      />
    )

    expect(screen.getByText('Completed')).toBeInTheDocument()
    expect(screen.getByRole('checkbox')).toBeChecked()
  })

  test('calls onDelete when delete button is clicked', () => {
    const handleDelete = jest.fn()
    render(
      <TaskItem
        task={mockTask}
        onDelete={handleDelete}
        onEdit={() => {}}
        onToggleComplete={() => {}}
      />
    )

    fireEvent.click(screen.getByText('Delete'))
    expect(handleDelete).toHaveBeenCalledWith(mockTask.id)
  })

  test('shows edit form when edit button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onDelete={() => {}}
        onEdit={() => {}}
        onToggleComplete={() => {}}
      />
    )

    fireEvent.click(screen.getByText('Edit'))
    expect(screen.getByText('Edit Task')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument()
  })
})

// TaskList tests
describe('TaskList component', () => {
  test('renders a list of tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onDelete={() => {}}
        onEdit={() => {}}
        onToggleComplete={() => {}}
      />
    )

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Another Task')).toBeInTheDocument()
  })

  test('shows message when no tasks are available', () => {
    render(
      <TaskList
        tasks={[]}
        onDelete={() => {}}
        onEdit={() => {}}
        onToggleComplete={() => {}}
      />
    )

    expect(screen.getByText(/no tasks available/i)).toBeInTheDocument()
  })
})
