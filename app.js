const tg = window.Telegram?.WebApp;

// 1. Данные товаров
const products = [
    {
        id: 1,
        name: "Chaser Mint",
        price: 60,
        volume: "30ml",
        img: "images/mint.jpg",
        description: "Освежающий, чистый и бодрящий вкус перечной мяты. Идеальная прохлада для ежедневного парения."
    },
    {
        id: 2,
        name: "Chaser Grape Plus",
        price: 60,
        volume: "30ml",
        img: "images/grape_plus.jpg",
        description: "Насыщенный вкус сочного тёмного винограда с усиленной ароматикой. Настоящая ягодная феерия."
    },
    {
        id: 3,
        name: "Chaser Pineapple",
        price: 60,
        volume: "30ml",
        img: "images/pineapple.jpg",
        description: "Яркий и сладкий тропический ананас с лёгкой приятной кислинкой сочной мякоти."
    },
    {
        id: 4,
        name: "Chaser Energy Cherry",
        price: 60,
        volume: "30ml",
        img: "images/energy_cherry.jpg",
        description: "Мощный тонизирующий микс бодрящего энергетика и спелой вишни."
    },
    {
        id: 5,
        name: "Chaser Lux Tropic Punch",
        price: 60,
        volume: "30ml",
        img: "images/tropic_punch.jpg",
        description: "Экзотический тропический пунш из линейки Lux Balance — гармоничное сочетание сочного манго и спелых цитрусов."
    },
    {
        id: 6,
        name: "Chaser Lux Blueberry Mint",
        price: 60,
        volume: "30ml",
        img: "images/blueberry_mint.jpg",
        description: "Премиальный микс спелой лесной черники и прохладных листочков свежей мяты."
    },
    {
        id: 7,
        name: "Chaser Triple Raspberry",
        price: 60,
        volume: "30ml",
        img: "images/triple_raspberry.jpg",
        description: "Уникальное сочетание трёх сортов малины: красной, жёлтой и синей (голубичной)."
    },
    {
        id: 8,
        name: "Chaser Pink Lemonade",
        price: 60,
        volume: "30ml",
        img: "images/pink_lemonade.jpg",
        description: "Классический розовый лимонад из сладкой малины и освежающего лимона с легким кубиком льда."
    }
];

// Корзина
let cart = [];

// 2. Отображение каталога
function renderProducts() {
    const container = document.getElementById('products-container') || document.body;
    container.innerHTML = '';

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.img}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p class="desc">${product.description}</p>
            <p class="price">${product.price} грн (${product.volume})</p>
            <button onclick="addToCart(${product.id})">Добавить в корзину</button>
        `;
        container.appendChild(card);
    });
}

// 3. Добавление в корзину
function addToCart(productId) {
    const item = products.find(p => p.id === productId);
    if (item) {
        cart.push(item);
        updateTelegramMainButton();
    }
}

// 4. Обновление Главной кнопки Telegram
function updateTelegramMainButton() {
    if (!tg) return;

    if (cart.length > 0) {
        const total = cart.reduce((sum, item) => sum + item.price, 0);
        tg.MainButton.text = `Оформить заказ (${total} грн)`;
        tg.MainButton.show();
    } else {
        tg.MainButton.hide();
    }
}

// 5. Инициализация и отправка заказа в бота
document.addEventListener('DOMContentLoaded', () => {
    if (tg) {
        tg.ready();
        tg.expand();
        
        Telegram.WebApp.onEvent('mainButtonClicked', () => {
            tg.sendData(JSON.stringify(cart));
        });
    }
    renderProducts();
});
