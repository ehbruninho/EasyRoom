function abrirModalImagem(src) {
    const imagem = document.getElementById("imagemExpandida");
    imagem.src = src;
    const modal = new bootstrap.Modal(document.getElementById('modalImagem'));
    modal.show();
}
