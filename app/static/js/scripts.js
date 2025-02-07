document.addEventListener('DOMContentLoaded', function () {
    // Função para criar categoria
    const novaCategoriaForm = document.getElementById('novaCategoriaForm');
    if (novaCategoriaForm) {
        novaCategoriaForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Impede o envio padrão do formulário
            const nomeCategoria = document.getElementById('nomeCategoria').value;
            fetch('/criar_categoria', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome: nomeCategoria }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('novaCategoriaModal'));
                        modal.hide();
                        const selectCategoria = document.querySelector('#categoria');
                        const novaOpcao = new Option(nomeCategoria, data.categoria_id, true, true);
                        selectCategoria.add(novaOpcao);
                        alert('Categoria criada com sucesso!');
                    } else {
                        alert('Erro ao criar categoria.');
                    }
                })
                .catch(error => console.error('Erro:', error));
        });
    }
});

    // Manipular categorias
    const selectCategoria = document.getElementById('categoria');
    const editarCategoriaBtn = document.getElementById('editarCategoriaBtn');
    const excluirCategoriaBtn = document.getElementById('excluirCategoriaBtn');
    if (selectCategoria && editarCategoriaBtn && excluirCategoriaBtn) {
        selectCategoria.addEventListener('change', function () {
            if (selectCategoria.value) {
                editarCategoriaBtn.disabled = false;
                excluirCategoriaBtn.disabled = false;
            } else {
                editarCategoriaBtn.disabled = true;
                excluirCategoriaBtn.disabled = true;
            }
        });

        editarCategoriaBtn.addEventListener('click', function () {
            const categoriaId = selectCategoria.value;
            const modal = new bootstrap.Modal(document.getElementById('editarCategoriaModal'));
            modal.show();
            const nomeCategoria = selectCategoria.options[selectCategoria.selectedIndex].text;
            document.getElementById('novoNomeCategoria').value = nomeCategoria;

            document.getElementById('editarCategoriaForm').addEventListener('submit', function (event) {
                event.preventDefault();
                const novoNome = document.getElementById('novoNomeCategoria').value;
                fetch(`/editar_categoria/${categoriaId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome: novoNome }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Categoria editada com sucesso!');
                            location.reload();
                        } else {
                            alert('Erro ao editar categoria.');
                        }
                    });
            });
        });

        excluirCategoriaBtn.addEventListener('click', function () {
            const categoriaId = selectCategoria.value;
            if (confirm('Tem certeza de que deseja excluir esta categoria?')) {
                fetch(`/excluir_categoria/${categoriaId}`, {
                    method: 'DELETE',
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Categoria excluída com sucesso!');
                            location.reload();
                        } else {
                            alert('Erro ao excluir categoria.');
                        }
                    });
            }
        });
    }

    // Expandir/Recolher Menu
    document.addEventListener('DOMContentLoaded', function () {
        const menuToggle = document.getElementById('menuToggle');
        const sidebarMenu = document.getElementById('sidebarMenu');
    
        if (menuToggle && sidebarMenu) {
            menuToggle.addEventListener('click', function () {
                if (sidebarMenu.classList.contains('collapsed')) {
                    // Expandir o menu com animação backInLeft
                    sidebarMenu.classList.remove('animate__backOutLeft');
                    sidebarMenu.classList.add('animate__backInLeft', 'animate__animated', 'animate__fast');
                    sidebarMenu.classList.remove('collapsed');
                } else {
                    // Recolher o menu com animação backOutLeft
                    sidebarMenu.classList.remove('animate__backInLeft');
                    sidebarMenu.classList.add('animate__backOutLeft', 'animate__animated', 'animate__fast');
                    setTimeout(() => {
                        sidebarMenu.classList.add('collapsed');
                    }, 500); // Aguarda o tempo da animação (500ms)
                }
            });
        }
    });