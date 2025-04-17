document.addEventListener('DOMContentLoaded', function() {
    const popUp = document.createElement('img');
    popUp.src = "/static/blog/decor_images/pop-up.png"; // Путь к изображению
    popUp.className = 'pop-up';

    const title = document.querySelector('.site-title'); // Элемент с заголовком

    const text = title.textContent;
    const lastSIndex = text.lastIndexOf('S'); // Поиск последней буквы "S"

    if (lastSIndex !== -1) {
        // Создаём временный span для точного позиционирования
        const tempSpan = document.createElement('span');
        tempSpan.textContent = text.substring(0, lastSIndex + 1);
        tempSpan.style.visibility = 'hidden';
        tempSpan.style.position = 'absolute';
        tempSpan.style.fontFamily = getComputedStyle(title).fontFamily;
        tempSpan.style.fontSize = getComputedStyle(title).fontSize;
        tempSpan.style.fontWeight = getComputedStyle(title).fontWeight;
        tempSpan.style.letterSpacing = getComputedStyle(title).letterSpacing;

        title.parentNode.insertBefore(tempSpan, title.nextSibling);

        const rect = tempSpan.getBoundingClientRect(); // Позиция временного элемента
        const titleRect = title.getBoundingClientRect(); // Позиция заголовка

        popUp.style.left = `${rect.right - titleRect.left - 20}px`; // Настраиваем положение по горизонтали
        popUp.style.top = `${rect.top - titleRect.top - 16}px`; // Настраиваем положение по вертикали

        tempSpan.remove(); // Удаляем временный span
    } else {
        // Если "S" не найдено, позиционируем букет по умолчанию
        popUp.style.left = 'calc(100% - 60px)';
        popUp.style.top = '-16px';
    }

    title.parentNode.appendChild(popUp);

    // Добавляем класс для анимации
    setTimeout(() => {
        popUp.classList.add('show');
    }, 500);
});
