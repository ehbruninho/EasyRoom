document.getElementById('date_init').addEventListener('change', function () {
    let dateInit = this.value;

    if (!dateInit) return;

    fetch(`/reserves/get_available_rooms?date_init=${encodeURIComponent(dateInit)}`)
        .then(response => response.json())
        .then(data => {
            let roomSelect = document.getElementById('room_id');
            roomSelect.innerHTML = '<option value="" disabled selected>Selecione uma sala</option>';

            if (data.error) {
                alert(data.error);
                return;
            }

            // Criar um grupo para separar salas disponíveis e ocupadas
            let availableGroup = document.createElement('optgroup');
            availableGroup.label = "Salas Disponíveis";

            let occupiedGroup = document.createElement('optgroup');
            occupiedGroup.label = "Salas Ocupadas";

            // Adicionar salas disponíveis
            data.available_rooms.forEach(room => {
                let option = document.createElement('option');
                option.value = room.id;
                option.textContent = `${room.name} - Capacidade: ${room.capacity}`;
                availableGroup.appendChild(option);
            });

            // Adicionar salas ocupadas em vermelho e desabilitadas
            data.occupied_rooms.forEach(room => {
                let option = document.createElement('option');
                option.value = room.id;
                option.textContent = `${room.name} - Capacidade: ${room.capacity} (Ocupada)`;
                option.style.color = "red";  // Aparece em vermelho
                option.disabled = true; // Impede a seleção
                occupiedGroup.appendChild(option);
            });

            // Adicionar os grupos ao select
            if (availableGroup.children.length > 0) roomSelect.appendChild(availableGroup);
            if (occupiedGroup.children.length > 0) roomSelect.appendChild(occupiedGroup);
        })
        .catch(error => console.error('Erro ao buscar salas disponíveis:', error));
});


