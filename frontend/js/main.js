document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURACIÓN ---
    const API_BASE_URL = 'http://127.0.0.1:5000';

    // --- SELECTORES DEL DOM ---
    const mainNav = document.getElementById('main-nav');
    const contentPanels = document.getElementById('content-panels');
    const tableHead = document.getElementById('table-head');
    const tableBody = document.getElementById('table-body');

    // Selectores del Modal
    const animalModal = document.getElementById('animal-modal');
    const addAnimalBtn = document.getElementById('add-animal-btn');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const cancelFormBtn = document.getElementById('cancel-form-btn');
    const animalForm = document.getElementById('animal-form');
    const modalTitle = document.getElementById('modal-title');
    const formResponse = document.getElementById('form-response');

    // --- LÓGICA DE NAVEGACIÓN ---
    mainNav.addEventListener('click', (e) => {
        e.preventDefault();
        const navLink = e.target.closest('.nav-link');
        if (!navLink) return;
        mainNav.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        navLink.classList.add('active');
        const targetId = navLink.dataset.target;
        contentPanels.querySelectorAll('.content-panel').forEach(panel => panel.classList.add('hidden'));
        document.getElementById(targetId).classList.remove('hidden');
    });

    // --- LÓGICA DEL MODAL ---
    const openModalForCreate = () => {
        modalTitle.textContent = 'Registrar Nuevo Animal';
        animalForm.reset();
        document.getElementById('id').value = ''; // Asegurar que no haya ID
        formResponse.textContent = '';
        animalModal.style.display = 'flex';
        lucide.createIcons();
    };

    const openModalForEdit = async (animalId) => {
        animalForm.reset();
        formResponse.textContent = '';
        modalTitle.textContent = 'Editar Animal';

        try {
            const response = await fetch(`${API_BASE_URL}/api/animales/${animalId}`);
            if (!response.ok) throw new Error('No se pudo cargar la información del animal.');
            const animal = await response.json();
            
            // Poblar el formulario con los datos del animal
            for (const key in animal) {
                const input = document.getElementById(key);
                if (input) {
                    if (input.type === 'checkbox') {
                        input.checked = !!animal[key];
                    } else {
                        input.value = animal[key] || '';
                    }
                }
            }
            animalModal.style.display = 'flex';
            lucide.createIcons();
        } catch (error) {
            alert(error.message);
        }
    };

    const openModalForView = async (animalId) => {
        animalForm.reset();
        formResponse.textContent = '';
        modalTitle.textContent = 'Ver Animal';

        // Deshabilita todos los campos del formulario
        Array.from(animalForm.elements).forEach(el => el.disabled = true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/animales/${animalId}`);
            if (!response.ok) throw new Error('No se pudo obtener el animal');
            const animal = await response.json();

            for (const key in animal) {
                if (animalForm.elements[key]) {
                    animalForm.elements[key].value = animal[key] || '';
                }
            }
            animalModal.style.display = 'flex';
            lucide.createIcons();
        } catch (error) {
            alert(error.message);
        }
    };

    const hideModal = () => {
        animalModal.style.display = 'none';
        // Habilita los campos para futuros usos (crear/editar)
        Array.from(animalForm.elements).forEach(el => el.disabled = false);
    };

    addAnimalBtn.addEventListener('click', openModalForCreate);
    closeModalBtn.addEventListener('click', hideModal);
    cancelFormBtn.addEventListener('click', hideModal);

    // --- LÓGICA DE LA API (Inventario) ---
    
    /**
     * Dibuja las cabeceras de la tabla.
     */
    const renderTableHeaders = () => {
        const headers = ['Arete', 'Nombre', 'Raza', 'Sexo', 'Edad (días)', 'Estado', 'Acciones'];
        const tr = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            tr.appendChild(th);
        });
        tableHead.innerHTML = '';
        tableHead.appendChild(tr);
    };

    /**
     * Muestra un estado de carga en la tabla.
     */
    const showLoadingState = () => {
        tableBody.innerHTML = `<tr><td colspan="${tableHead.firstElementChild.childElementCount}" class="text-center p-6 text-slate-500">Cargando animales...</td></tr>`;
    };

    /**
     * Calcula la edad en días a partir de una fecha de nacimiento.
     */
    const calculateAgeInDays = (birthDate) => {
        if (!birthDate) return 'N/A';
        const today = new Date();
        const dob = new Date(birthDate);
        const diffTime = Math.abs(today - dob);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    };

    let allAnimals = []; // Guarda todos los animales

    // Modifica fetchAnimals para guardar los datos originales
    async function fetchAnimals() {
        if (!tableBody) return;
        showLoadingState();

        try {
            const url = `${API_BASE_URL}/api/animales`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
            allAnimals = await response.json(); // Guarda todos los animales
            renderAnimals(allAnimals);
            updateSummary(allAnimals); // <--- agrega esto
            fillRazaFilter(allAnimals); // <-- llena el filtro de razas
        } catch (error) {
            tableBody.innerHTML = `<tr><td colspan="${tableHead.firstElementChild.childElementCount}" class="text-center p-6 text-red-500">Error al cargar los datos.</td></tr>`;
            console.error('Error en fetchAnimals:', error);
        }
    }

    // Función para renderizar animales
    function renderAnimals(animals) {
        tableBody.innerHTML = '';
        if (animals.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="${tableHead.firstElementChild.childElementCount}" class="text-center p-6 text-slate-500">No hay animales registrados.</td></tr>`;
            return;
        }
        animals.forEach(animal => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><span class="font-bold text-slate-800">${animal.arete_id || '-'}</span></td>
                <td>${animal.nombre || '-'}</td>
                <td>${animal.raza || '-'}</td>
                <td>${animal.sexo || '-'}</td>
                <td>${calculateAgeInDays(animal.fecha_nacimiento)}</td>
                <td><span class="status-badge ${animal.estado ? animal.estado.toLowerCase() : ''}">${animal.estado || '-'}</span></td>
                <td class="flex items-center gap-2">
                    <button class="view-btn text-slate-500 hover:text-blue-600" data-id="${animal.id}" title="Ver Detalles"><i data-lucide="eye" class="w-5 h-5"></i></button>
                    <button class="edit-btn text-slate-500 hover:text-green-600" data-id="${animal.id}" title="Editar"><i data-lucide="pencil" class="w-5 h-5"></i></button>
                    <button class="delete-btn text-slate-500 hover:text-red-600" data-id="${animal.id}" title="Eliminar"><i data-lucide="trash-2" class="w-5 h-5"></i></button>
                </td>
            `;
            tableBody.appendChild(tr);
        });
        lucide.createIcons();
    }

    // Barra de búsqueda (asegúrate de tener los elementos en tu HTML)
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const razaFilter = document.getElementById('raza-filter');

    // Llenar el filtro de razas dinámicamente
    function fillRazaFilter(animals) {
        const razas = Array.from(new Set(animals.map(a => a.raza).filter(Boolean)));
        razaFilter.innerHTML = `<option value="">Todas las razas</option>` +
            razas.map(raza => `<option value="${raza}">${raza}</option>`).join('');
    }

    // Filtrar y renderizar animales según búsqueda y raza
    function filterAndRenderAnimals() {
        const q = searchInput.value.trim().toLowerCase();
        const raza = razaFilter.value;
        let filtered = allAnimals;

        if (q) {
            filtered = filtered.filter(animal =>
                (animal.nombre || '').toLowerCase().includes(q) ||
                (animal.arete_id || '').toLowerCase().includes(q) ||
                (animal.raza || '').toLowerCase().includes(q) ||
                (animal.sexo || '').toLowerCase().includes(q) ||
                (animal.estado || '').toLowerCase().includes(q)
            );
        }
        if (raza) {
            filtered = filtered.filter(animal => animal.raza === raza);
        }
        renderAnimals(filtered);
    }

    // Eventos para búsqueda y filtro
    searchInput.addEventListener('input', filterAndRenderAnimals);
    razaFilter.addEventListener('change', filterAndRenderAnimals);

    /**
     * Maneja el envío del formulario para crear o actualizar un animal.
     */
    animalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(animalForm);
        const data = Object.fromEntries(formData.entries());
        
        // Manejar checkbox
        data.es_reproductor = document.getElementById('es_reproductor').checked;
        
        // Limpiar campos vacíos para que la DB use sus defaults
        for(const key in data) {
            if(data[key] === '' || data[key] === null) {
                delete data[key];
            }
        }

        const animalId = data.id;
        delete data.id; // No enviar el id en el cuerpo del JSON

        const method = animalId ? 'PUT' : 'POST';
        const url = animalId ? `${API_BASE_URL}/api/animales/${animalId}` : `${API_BASE_URL}/api/animales`;
        
        formResponse.textContent = 'Guardando...';
        formResponse.className = 'text-blue-600';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await response.json();

            if (response.ok) {
                formResponse.textContent = result.message || '¡Operación exitosa!';
                formResponse.className = 'text-green-600';
                setTimeout(() => {
                    hideModal();
                    fetchAnimals();
                }, 1000);
            } else {
                throw new Error(result.error || 'Ocurrió un error en el servidor.');
            }
        } catch (error) {
            formResponse.textContent = `Error: ${error.message}`;
            formResponse.className = 'text-red-600';
        }
    });

    /**
     * Maneja los clics en los botones de acción de la tabla (editar, eliminar).
     */
    tableBody.addEventListener('click', (e) => {
        const viewBtn = e.target.closest('.view-btn');
        const editBtn = e.target.closest('.edit-btn');
        const deleteBtn = e.target.closest('.delete-btn');
        if (viewBtn) {
            const animalId = viewBtn.dataset.id;
            openModalForView(animalId);
        } else if (editBtn) {
            const animalId = editBtn.dataset.id;
            openModalForEdit(animalId);
        } else if (deleteBtn) {
            const animalId = deleteBtn.dataset.id;
            if (confirm(`¿Estás seguro de que quieres eliminar el animal con ID ${animalId}?`)) {
                // Lógica para eliminar
                fetch(`${API_BASE_URL}/api/animales/${animalId}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message) {
                        fetchAnimals(); // Recarga la tabla
                    } else {
                        alert(result.error || 'No se pudo eliminar el animal.');
                    }
                })
                .catch(error => {
                    alert('Error al eliminar: ' + error.message);
                });
            }
        }
    });


    // --- INICIALIZACIÓN ---
    renderTableHeaders();
    fetchAnimals();
    lucide.createIcons();

    function updateSummary(animals) {
        // Total animales
        document.getElementById('total-animales').textContent = animals.length;

        // Total reproductoras (hembra y es_reproductor true)
        const reproductoras = animals.filter(a =>
            (a.sexo || '').toLowerCase() === 'hembra' && (a.es_reproductor === true || a.es_reproductor === 1 || a.es_reproductor === '1')
        );
        document.getElementById('total-reproductoras').textContent = reproductoras.length;

        // Total machos
        const machos = animals.filter(a =>
            (a.sexo || '').toLowerCase() === 'macho'
        );
        document.getElementById('total-machos').textContent = machos.length;

        // Peso promedio
        const pesos = animals
            .map(a => parseFloat(a.peso_nacimiento_kg || a.peso_destete_kg || a.peso || 0))
            .filter(p => !isNaN(p) && p > 0);
        const promedio = pesos.length ? (pesos.reduce((a, b) => a + b, 0) / pesos.length) : 0;
        document.getElementById('peso-promedio').textContent = `${promedio.toFixed(0)} kg`;
    }
});

