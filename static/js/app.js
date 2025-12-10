// Toast notification system
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastContent = document.getElementById('toastContent');
    const toastIcon = document.getElementById('toastIcon');
    const toastMessage = document.getElementById('toastMessage');
    
    // Set content based on type
    if (type === 'success') {
        toastContent.className = 'bg-white rounded-xl shadow-lg border border-green-200 px-6 py-4 flex items-center gap-3 min-w-[300px]';
        toastIcon.textContent = '✓';
        toastIcon.className = 'text-2xl text-green-600';
        toastMessage.className = 'text-sm font-light flex-1 text-slate-900';
    } else if (type === 'error') {
        toastContent.className = 'bg-white rounded-xl shadow-lg border border-red-200 px-6 py-4 flex items-center gap-3 min-w-[300px]';
        toastIcon.textContent = '✕';
        toastIcon.className = 'text-2xl text-red-600';
        toastMessage.className = 'text-sm font-light flex-1 text-slate-900';
    } else if (type === 'info') {
        toastContent.className = 'bg-white rounded-xl shadow-lg border border-blue-200 px-6 py-4 flex items-center gap-3 min-w-[300px]';
        toastIcon.textContent = 'ⓘ';
        toastIcon.className = 'text-2xl text-blue-600';
        toastMessage.className = 'text-sm font-light flex-1 text-slate-900';
    }
    
    toastMessage.textContent = message;
    toast.classList.remove('hidden');
    
    // Auto-hide after 4 seconds
    setTimeout(() => {
        hideToast();
    }, 4000);
}

function hideToast() {
    const toast = document.getElementById('toast');
    toast.classList.add('hidden');
}

// Load cities on page load
window.onload = function() {
    fetch('/api/cities')
        .then(response => response.json())
        .then(cities => {
            const select = document.getElementById('cityFilter');
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading cities:', error));
};

function searchStations() {
    const searchText = document.getElementById('searchText').value.trim();
    const city = document.getElementById('cityFilter').value;
    const sortBy = document.getElementById('sortBy').value;
    const sortOrder = document.getElementById('sortOrder').value;
    
    const resultsSection = document.getElementById('resultsSection');
    const stationsList = document.getElementById('stationsList');
    
    resultsSection.style.display = 'block';
    stationsList.innerHTML = `
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 text-center">
            <div class="inline-block animate-spin text-4xl text-slate-300 mb-2">↻</div>
            <p class="text-slate-500 font-light">Loading stations...</p>
        </div>
    `;
    
    let url = '/api/stations';
    const params = new URLSearchParams();
    
    if (city) params.append('city', city);
    if (sortBy) params.append('sort_by', sortBy);
    if (sortOrder) params.append('order', sortOrder);
    
    if (searchText) {
        url = `/api/stations/${encodeURIComponent(searchText)}`;
        if (params.toString()) {
            url += '?' + params.toString();
        }
    } else if (params.toString()) {
        url += '?' + params.toString();
    }
    
    fetch(url)
        .then(response => response.json())
        .then(stations => {
            if (stations.error) {
                stationsList.innerHTML = `
                    <div class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
                        <div class="text-3xl text-red-400 mb-2">↯</div>
                        <p class="text-red-700 font-light">${stations.error}</p>
                    </div>
                `;
                return;
            }
            
            document.getElementById('resultCount').textContent = stations.length;
            
            if (stations.length === 0) {
                stationsList.innerHTML = `
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-12 text-center">
                        <div class="text-6xl text-slate-200 mb-4">↓</div>
                        <h3 class="text-lg font-light text-slate-900 mb-2">No stations found</h3>
                        <p class="text-slate-500 font-light">Try adjusting your search criteria</p>
                    </div>
                `;
                return;
            }
            
            stationsList.innerHTML = stations.map(station => `
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 hover:shadow-md hover:border-slate-300 transition-all cursor-pointer group" onclick="window.location.href='/station/${station.ID}'">
                    <div class="flex items-start justify-between mb-4 pb-4 border-b border-slate-100">
                        <div class="flex-1">
                            <h4 class="text-lg font-light text-slate-900 mb-1 group-hover:text-slate-600 transition-colors">${station.Nimi || station.Name || 'N/A'}</h4>
                            ${station.Name && station.Name !== station.Nimi ? 
                                `<p class="text-sm text-slate-500 font-light">${station.Name}</p>` : 
                                ''
                            }
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-1 bg-slate-100 text-slate-600 text-xs rounded-full font-mono">#${station.ID || 'N/A'}</span>
                            <button onclick="event.stopPropagation(); openEditModal(${station.ID})" class="opacity-0 group-hover:opacity-100 px-2 py-1 text-slate-600 hover:text-slate-900 transition-all">
                                ✎
                            </button>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="flex items-start gap-3">
                            <span class="text-slate-300 mt-0.5">→</span>
                            <div class="flex-1">
                                <div class="text-xs text-slate-500 uppercase tracking-wide mb-1">Address</div>
                                <div class="text-sm text-slate-900 font-light">${station.Osoite || station.Adress || 'N/A'}</div>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-slate-300 mt-0.5">→</span>
                            <div class="flex-1">
                                <div class="text-xs text-slate-500 uppercase tracking-wide mb-1">City</div>
                                <div class="text-sm text-slate-900 font-light">${station.Kaupunki || 'N/A'}</div>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-slate-300 mt-0.5">→</span>
                            <div class="flex-1">
                                <div class="text-xs text-slate-500 uppercase tracking-wide mb-1">Capacity</div>
                                <div class="inline-block px-2.5 py-1 bg-slate-900 text-white text-xs rounded-full font-light">
                                    ${station.Kapasiteet || 'N/A'} bikes
                                </div>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-slate-300 mt-0.5">→</span>
                            <div class="flex-1">
                                <div class="text-xs text-slate-500 uppercase tracking-wide mb-1">Operator</div>
                                <div class="text-sm text-slate-900 font-light">${station.Operaattor || 'N/A'}</div>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            stationsList.innerHTML = `
                <div class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center">
                    <div class="text-3xl text-red-400 mb-2">↯</div>
                    <p class="text-red-700 font-light">Error: ${error.message}</p>
                </div>
            `;
        });
}

function clearSearch() {
    document.getElementById('searchText').value = '';
    document.getElementById('cityFilter').value = '';
    document.getElementById('sortBy').value = 'Nimi';
    document.getElementById('sortOrder').value = 'ASC';
    document.getElementById('resultsSection').style.display = 'none';
}

// Allow Enter key to trigger search
document.getElementById('searchText').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchStations();
    }
});

// Modal functions
function openCreateModal() {
    document.getElementById('modalTitle').textContent = 'New Station';
    document.getElementById('stationForm').reset();
    document.getElementById('editId').value = '';
    document.getElementById('formModal').classList.remove('hidden');
}

function openEditModal(stationId) {
    document.getElementById('modalTitle').textContent = 'Edit Station';
    document.getElementById('formModal').classList.remove('hidden');
    
    // Fetch station data
    fetch(`/api/station/${stationId}`)
        .then(response => response.json())
        .then(station => {
            document.getElementById('editId').value = station.ID;
            document.getElementById('formNimi').value = station.Nimi || '';
            document.getElementById('formNamn').value = station.Namn || '';
            document.getElementById('formName').value = station.Name || '';
            document.getElementById('formOsoite').value = station.Osoite || '';
            document.getElementById('formAdress').value = station.Adress || '';
            document.getElementById('formKaupunki').value = station.Kaupunki || '';
            document.getElementById('formOperaattor').value = station.Operaattor || '';
            document.getElementById('formKapasiteet').value = station.Kapasiteet || '';
            document.getElementById('formFID').value = station.FID || '';
            document.getElementById('formStad').value = station.Stad || '';
            document.getElementById('formX').value = station.x || '';
            document.getElementById('formY').value = station.y || '';
            document.getElementById('formKuva').value = station.Kuva || '';
        })
        .catch(error => alert('Error loading station: ' + error.message));
}

function closeFormModal() {
    document.getElementById('formModal').classList.add('hidden');
}

// Handle form submission
document.getElementById('stationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const editId = document.getElementById('editId').value;
    const isEdit = editId !== '';
    
    const stationData = {
        Nimi: document.getElementById('formNimi').value,
        Namn: document.getElementById('formNamn').value,
        Name: document.getElementById('formName').value,
        Osoite: document.getElementById('formOsoite').value,
        Adress: document.getElementById('formAdress').value,
        Kaupunki: document.getElementById('formKaupunki').value,
        Operaattor: document.getElementById('formOperaattor').value,
        Kapasiteet: parseInt(document.getElementById('formKapasiteet').value),
        FID: parseInt(document.getElementById('formFID').value),
        Stad: document.getElementById('formStad').value,
        x: parseFloat(document.getElementById('formX').value),
        y: parseFloat(document.getElementById('formY').value),
        Kuva: document.getElementById('formKuva').value
    };
    
    const url = isEdit ? `/api/station/${editId}` : '/api/stations';
    const method = isEdit ? 'PUT' : 'POST';
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(stationData)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            showToast(result.error, 'error');
            return;
        }
        closeFormModal();
        const message = isEdit ? 'Station updated successfully!' : 'Station created successfully!';
        showToast(message, 'success');
        searchStations(); // Refresh the list
    })
    .catch(error => {
        showToast('Error: ' + error.message, 'error');
    });
});
