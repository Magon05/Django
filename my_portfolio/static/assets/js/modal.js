 const images = [
        'static/images/minishop1.png',
        'static/images/minishop2.png',
        'static/images/minishop3.png',
        'static/images/minishop4.png',
        'static/images/phonebook1.png',
        'static/images/phonebook2.png',
        'static/images/phonebook3.png',
        'static/images/phonebook4.png',
        'static/images/SnakeGame.jpg',
        'static/images/Менеджер паролей.png',
        'static/images/brainbuilder.jpg'
    ];
    let currentIndex = 0;

    function openModal(index) {
        currentIndex = index;
        var modal = document.getElementById("myModal");
        var modalImg = document.getElementById("img01");
        modal.style.display = "flex"; // Изменяем стиль на flex для отображения
        modalImg.src = images[currentIndex];
    }

    function closeModal() {
        var modal = document.getElementById("myModal");
        modal.style.display = "none"; // Скрываем модальное окно
    }

    function changeImage(direction) {
        currentIndex += direction;
        if (currentIndex < 0) {
            currentIndex = images.length - 1; // Переход к последнему изображению
        } else if (currentIndex >= images.length) {
            currentIndex = 0; // Переход к первому изображению
        }
        var modalImg = document.getElementById("img01");
        modalImg.src = images[currentIndex];
    }