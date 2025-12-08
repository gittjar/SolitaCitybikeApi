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
                <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 hover:shadow-md hover:border-slate-300 transition-all">
                    <div class="flex items-start justify-between mb-4 pb-4 border-b border-slate-100">
                        <div class="flex-1">
                            <h4 class="text-lg font-light text-slate-900 mb-1">${station.Nimi || station.Name || 'N/A'}</h4>
                            ${station.Name && station.Name !== station.Nimi ? 
                                `<p class="text-sm text-slate-500 font-light">${station.Name}</p>` : 
                                ''
                            }
                        </div>
                        <span class="px-2.5 py-1 bg-slate-100 text-slate-600 text-xs rounded-full font-mono">#${station.ID || 'N/A'}</span>
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
