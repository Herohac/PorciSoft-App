document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURACIÓN ---
    const API_BASE_URL = 'http://127.0.0.1:5000';

    // --- SELECTORES DEL MÓDULO DE LOTES ---
    const tableHead = document.getElementById('lote-table-head');
    const tableBody = document.getElementById('lote-table-body');
    const modal = document.getElementById('lote-modal');
    const addBtn = document.getElementById('add-lote-btn');
    const closeBtn = document.getElementById('close-lote-modal-btn');
    const cancelBtn = document.getElementById('cancel-lote-form-btn');
    const form = document.getElementById('lote-form');
    const modalTitle = document.getElementById('lote-modal-title');
    const formResponse = document.getElementById('lote-form-response');

    let allLotes = []; // Guarda todos los lotes

    // --- MÉTODOS ---

    const renderTableHeaders = () => {
        const headers = ['ID', 'Nombre del Lote', 'Descripción', 'Fecha Creación', 'Acciones'];
        tableHead.innerHTML = `<tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
    };

    const showLoadingState = () => {
        tableBody.innerHTML = `<tr><td colspan="5" class="text-center p-6 text-slate-500">Cargando lotes...</td></tr>`;
    };

    const renderTable = (lotes) => {
        tableBody.innerHTML = '';
        if (lotes.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center p-6 text-slate-500">No hay lotes registrados.</td></tr>`;
            return;
        }
        lotes.forEach(lote => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><span class="font-bold text-slate-800">${lote.id}</span></td>
                <td>${lote.nombre_lote}</td>
                <td>${lote.descripcion || '-'}</td>
                <td>${lote.fecha_creacion}</td>
                <td class="flex items-center gap-2">
                    <button class="edit-lote-btn text-slate-500 hover:text-green-600" data-id="${lote.id}" title="Editar"><i data-lucide="pencil" class="w-5 h-5"></i></button>
                    <button class="delete-lote-btn text-slate-500 hover:text-red-600" data-id="${lote.id}" title="Eliminar"><i data-lucide="trash-2" class="w-5 h-5"></i></button>
                </td>
            `;
            tableBody.appendChild(tr);
        });
        lucide.createIcons();
    };

    const openModalForCreate = () => {
        form.reset();
        modalTitle.textContent = 'Registrar Nuevo Lote';
        document.getElementById('lote_id_form').value = '';
        formResponse.textContent = '';
        modal.style.display = 'flex';
    };

    const openModalForEdit = (lote) => {
        form.reset();
        modalTitle.textContent = 'Editar Lote';
        document.getElementById('lote_id_form').value = lote.id;
        document.getElementById('nombre_lote').value = lote.nombre_lote;
        document.getElementById('descripcion').value = lote.descripcion;
        formResponse.textContent = '';
        modal.style.display = 'flex';
    };

    const hideModal = () => {
        modal.style.display = 'none';
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const loteId = data.id;
        delete data.id;

        const method = loteId ? 'PUT' : 'POST';
        const url = loteId ? `${API_BASE_URL}/api/lotes/${loteId}` : `${API_BASE_URL}/api/lotes`;

        formResponse.textContent = 'Guardando...';
        formResponse.className = 'text-blue-600';

        try {
            const response = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Ocurrió un error');

            formResponse.textContent = result.message;
            formResponse.className = 'text-green-600';
            setTimeout(() => {
                hideModal();
                fetchAndRenderLotes();
            }, 1000);
        } catch (error) {
            formResponse.textContent = `Error: ${error.message}`;
            formResponse.className = 'text-red-600';
        }
    };

    const handleTableActions = (e) => {
        const editBtn = e.target.closest('.edit-lote-btn');
        if (editBtn) {
            const loteId = editBtn.dataset.id;
            const lote = allLotes.find(l => l.id == loteId);
            openModalForEdit(lote);
        }

        const deleteBtn = e.target.closest('.delete-lote-btn');
        if (deleteBtn) {
            const loteId = deleteBtn.dataset.id;
            if (confirm(`¿Estás seguro de que quieres eliminar el lote ${loteId}?`)) {
                deleteLote(loteId);
            }
        }
    };

    const deleteLote = async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/lotes/${id}`, { method: 'DELETE' });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Error al eliminar');
            alert(result.message);
            fetchAndRenderLotes();
        } catch (error) {
            alert(error.message);
        }
    };

    async function fetchAndRenderLotes() {
        showLoadingState();
        try {
            const response = await fetch(`${API_BASE_URL}/api/lotes`);
            if (!response.ok) throw new Error('Error al cargar los lotes');
            const lotes = await response.json();
            allLotes = lotes;
            renderTable(lotes);
        } catch (error) {
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center p-6 text-red-500">${error.message}</td></tr>`;
        }
    }

    // --- INICIALIZACIÓN ---
    addBtn.addEventListener('click', openModalForCreate);
    closeBtn.addEventListener('click', hideModal);
    cancelBtn.addEventListener('click', hideModal);
    form.addEventListener('submit', handleSubmit);
    tableBody.addEventListener('click', handleTableActions);
    
    renderTableHeaders();
    fetchAndRenderLotes();
    lucide.createIcons();

    // Búsqueda instantánea
    const loteSearchInput = document.getElementById('lote-search-input');
    if (loteSearchInput) {
        loteSearchInput.addEventListener('input', () => {
            const q = loteSearchInput.value.trim().toLowerCase();
            if (!q) {
                renderTable(allLotes);
                return;
            }
            const filtered = allLotes.filter(lote =>
                (lote.nombre_lote || '').toLowerCase().includes(q) ||
                (lote.descripcion || '').toLowerCase().includes(q)
            );
            renderTable(filtered);
        });
    }

    // --- NUEVO CÓDIGO PARA MANEJO DE FORMULARIO ---
    const loteForm = document.getElementById('lote-form');
    const loteModal = document.getElementById('lote-modal');

    loteForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // <-- Esto es clave

        // Tu lógica para guardar o editar el lote (fetch POST/PUT)
        // Ejemplo:
        const formData = new FormData(loteForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('http://127.0.0.1:5000/api/lotes', {
                method: data.id ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Error al guardar el lote');
            // Cierra el modal
            loteModal.classList.add('hidden');
            // Actualiza la tabla de lotes SIN recargar la página
            fetchLotes();
        } catch (error) {
            // Muestra el error en el formulario
            document.getElementById('lote-form-response').textContent = error.message;
        }
    });

    // Similar para eliminar: después de eliminar, solo llama fetchLotes()

    async function eliminarLote(id) {
        if (!confirm('¿Seguro que deseas eliminar este lote?')) return;
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/lotes/${id}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Error al eliminar');
            fetchLotes(); // Solo actualiza la tabla
        } catch (error) {
            alert(error.message);
        }
    }
});