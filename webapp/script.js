let tg = window.Telegram.WebApp;
tg.expand(); // Разворачиваем WebApp

document.getElementById("sendReview").addEventListener("click", function() {
    let reviewText = document.getElementById("review").value.trim();

    if (reviewText === "") {
        alert("Пожалуйста, напишите отзыв.");
        return;
    }

    tg.sendData(JSON.stringify({ review: reviewText })); // Отправка данных в бота
    tg.close(); // Закрываем WebApp
});
