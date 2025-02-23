let tg = window.Telegram.WebApp;
tg.expand(); // Разворачиваем WebApp

let selectedRating = 0;
const textarea = document.getElementById("review");
const sendButton = document.getElementById("sendReview");

// Обработчик клика по звёздам
document.querySelectorAll(".star").forEach(star => {
    star.addEventListener("click", function() {
        selectedRating = parseInt(this.getAttribute("data-value"));
        updateStars(selectedRating);
    });
});

// Функция для обновления цвета звёзд
function updateStars(rating) {
    document.querySelectorAll(".star").forEach(star => {
        if (parseInt(star.getAttribute("data-value")) <= rating) {
            star.classList.add("selected");
        } else {
            star.classList.remove("selected");
        }
    });
}

// Обработчик отправки отзыва
sendButton.addEventListener("click", function() {
    let reviewText = textarea.value.trim();

    if (reviewText === "") {
        alert("Пожалуйста, напишите отзыв.");
        resetFocus();
        return;
    }
    if (selectedRating === 0) {
        alert("Выберите количество звёзд.");
        resetFocus();
        return;
    }

    let reviewData = {
        review: reviewText,
        rating: selectedRating
    };

    tg.sendData(JSON.stringify(reviewData)); // Отправляем данные боту
    tg.close(); // Закрываем WebApp
});

// Функция для сброса фокуса и возврата
function resetFocus() {
    sendButton.blur(); // Убираем фокус с кнопки
    setTimeout(() => textarea.focus(), 100); // Через 100 мс возвращаем фокус в текстовое поле
}

// Сброс ошибки при вводе текста
textarea.addEventListener("input", function () {
    textarea.classList.remove("error");
});
