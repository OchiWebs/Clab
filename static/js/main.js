document.addEventListener('DOMContentLoaded', () => {
    const taskListDiv = document.getElementById('task-list');
    if (!taskListDiv) return;

    fetch(`/api/proyek/${PROJECT_UUID}/tasks`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || `HTTP error! status: ${response.status}`) });
            }
            return response.json();
        })
        .then(data => {
            console.log("API Response Received:", data);
            
            taskListDiv.innerHTML = ''; 

            if (data.error) {
                taskListDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                return;
            }
            
            if (data.tasks.length === 0) {
                taskListDiv.innerHTML = '<div class="alert alert-secondary">No tasks have been created for this project yet.</div>';
                return;
            }

            const ul = document.createElement('ul');
            ul.className = 'list-group list-group-flush';

            data.tasks.forEach(task => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                
                let taskTitle = task.completed
                    ? `<s>${task.title}</s>`
                    : task.title;

                li.innerHTML = `
                    <span>
                        <i class="bi ${task.completed ? 'bi-check-circle-fill text-success' : 'bi-hourglass-split text-warning'} me-2"></i>
                        ${taskTitle}
                    </span>
                    <span class="badge bg-${task.completed ? 'success' : 'warning'} rounded-pill">
                        ${task.completed ? 'Completed' : 'Pending'}
                    </span>
                `;
                ul.appendChild(li);
            });
            taskListDiv.appendChild(ul);
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
            taskListDiv.innerHTML = `<div class="alert alert-danger">Failed to load tasks: ${error.message}</div>`;
        });
});