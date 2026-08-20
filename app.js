const PRODUCTS = [
  {
    id: "hoodie",
    name: "Chase Hoodie",
    desc: "Плотный худи, крой oversized, внутренний начёс.",
    price: 8900,
    cat: "одежда",
    emoji: "🖤",
    color: "#1f2933",
    sizes: ["S", "M", "L", "XL"],
  },
  {
    id: "tee",
    name: "Motion Tee",
    desc: "Хлопок 240 г, принт CHASER на груди.",
    price: 3400,
    cat: "одежда",
    emoji: "⚡️",
    color: "#262218",
    sizes: ["S", "M", "L"],
  },
  {
    id: "pants",
    name: "Track Pants",
    desc: "Спортивные штаны с лампасами и карманами на молнии.",
    price: 6700,
    cat: "одежда",
    emoji: "🏃",
    color: "#172018",
    sizes: ["S", "M", "L", "XL"],
  },
  {
    id: "sneakers",
    name: "Velocity",
    desc: "Кроссовки для города и зала, амортизация на каждый день.",
    price: 12400,
    cat: "обувь",
    emoji: "👟",
    color: "#1a2030",
    sizes: ["40", "41", "42", "43", "44"],
  },
  {
    id: "cap",
    name: "Night Cap",
    desc: "Кепка с вышивкой логотипа, регулировка сзади.",
    price: 2900,
    cat: "аксессуары",
    emoji: "🧢",
    color: "#201820",
    sizes: ["one size"],
  },
  {
    id: "bag",
    name: "Chase Pack",
    desc: "Рюкзак 18 л, отделение для ноутбука 14\".",
    price: 5600,
    cat: "аксессуары",
    emoji: "🎒",
    color: "#182018",
    sizes: ["one size"],
  },
];

const tg = window.Telegram?.WebApp;
const storeKey = "chaser-shop-v1";

const state = loadState();
let activeCat = "все";
let query = "";
let selectedProduct = null;
let selectedSize = null;

function loadState() {
  try {
    const raw = JSON.parse(localStorage.getItem(storeKey) || "{}");
    return { cart: raw.cart || [], favs: raw.favs || [] };
  } catch {
    return { cart: [], favs: [] };
  }
}

function saveState() {
  localStorage.setItem(storeKey, JSON.stringify(state));
}

function money(n) {
  return `${n.toLocaleString("ru-RU")} ₽`;
}

function haptic(type = "light") {
  tg?.HapticFeedback?.impactOccurred(type);
}

function user() {
  return tg?.initDataUnsafe?.user || null;
}

function userName() {
  return user()?.first_name || "гостю";
}

function countItems() {
  return state.cart.reduce((sum, item) => sum + item.qty, 0);
}

function cartSum() {
  return state.cart.reduce((sum, item) => sum + item.price * item.qty, 0);
}

function filteredProducts(source = PRODUCTS) {
  return source.filter((p) => {
    const catOk = activeCat === "все" || p.cat === activeCat;
    const q = query.trim().toLowerCase();
    const textOk = !q || `${p.name} ${p.desc} ${p.cat}`.toLowerCase().includes(q);
    return catOk && textOk;
  });
}

function renderCats() {
  const cats = ["все", ...new Set(PRODUCTS.map((p) => p.cat))];
  const nav = document.getElementById("cats");
  nav.innerHTML = "";
  cats.forEach((cat) => {
    const btn = document.createElement("button");
    btn.textContent = cat;
    btn.className = cat === activeCat ? "active" : "";
    btn.onclick = () => {
      activeCat = cat;
      haptic();
      renderCats();
      renderCatalog();
    };
    nav.appendChild(btn);
  });
}

function productCard(product) {
  const btn = document.createElement("button");
  btn.className = "card";
  btn.innerHTML = `
    <div class="visual" style="background:${product.color}">${product.emoji}</div>
    <div class="card-body">
      <h3>${product.name}</h3>
      <p class="muted">${product.cat}</p>
      <p class="price">${money(product.price)}</p>
    </div>
  `;
  btn.onclick = () => openProduct(product);
  return btn;
}

function renderCatalog() {
  const root = document.getElementById("catalog");
  const list = filteredProducts();
  root.innerHTML = "";
  if (!list.length) {
    root.innerHTML = `<p class="empty">Ничего не нашли.</p>`;
    return;
  }
  list.forEach((p) => root.appendChild(productCard(p)));
}

function renderFavs() {
  const root = document.getElementById("favs");
  const list = PRODUCTS.filter((p) => state.favs.includes(p.id));
  root.innerHTML = "";
  if (!list.length) {
    root.innerHTML = `<p class="empty">Пока пусто — нажми ♡ на карточке товара.</p>`;
    return;
  }
  list.forEach((p) => root.appendChild(productCard(p)));
}

function openProduct(product) {
  selectedProduct = product;
  selectedSize = product.sizes[0];
  haptic();
  const visual = document.getElementById("productVisual");
  visual.style.background = product.color;
  visual.textContent = product.emoji;
  document.getElementById("productName").textContent = product.name;
  document.getElementById("productDesc").textContent = product.desc;
  document.getElementById("productPrice").textContent = money(product.price);
  const heart = document.getElementById("favToggle");
  heart.classList.toggle("on", state.favs.includes(product.id));
  heart.textContent = state.favs.includes(product.id) ? "♥" : "♡";
  const sizes = document.getElementById("sizes");
  sizes.innerHTML = "";
  product.sizes.forEach((size) => {
    const btn = document.createElement("button");
    btn.textContent = size;
    btn.className = size === selectedSize ? "active" : "";
    btn.onclick = () => {
      selectedSize = size;
      haptic();
      [...sizes.children].forEach((el) =>
        el.classList.toggle("active", el.textContent === size)
      );
    };
    sizes.appendChild(btn);
  });
  document.getElementById("productSheet").classList.remove("hidden");
  tg?.BackButton?.show();
}

function closeSheets() {
  document.getElementById("productSheet").classList.add("hidden");
  document.getElementById("doneSheet").classList.add("hidden");
  tg?.BackButton?.hide();
}

function toggleFav() {
  if (!selectedProduct) return;
  const i = state.favs.indexOf(selectedProduct.id);
  if (i >= 0) state.favs.splice(i, 1);
  else state.favs.push(selectedProduct.id);
  saveState();
  haptic("medium");
  openProduct(selectedProduct);
  renderFavs();
  renderProfile();
}

function addToCart() {
  if (!selectedProduct || !selectedSize) return;
  const key = `${selectedProduct.id}-${selectedSize}`;
  const existing = state.cart.find((item) => item.key === key);
  if (existing) existing.qty += 1;
  else {
    state.cart.push({
      key,
      id: selectedProduct.id,
      name: selectedProduct.name,
      size: selectedSize,
      price: selectedProduct.price,
      qty: 1,
    });
  }
  saveState();
  haptic("medium");
  renderCart();
  closeSheets();
  showTab("cart");
}

function renderCart() {
  const root = document.getElementById("cartItems");
  document.getElementById("cartTotal").textContent = money(cartSum());
  document.getElementById("tabCart").textContent = String(countItems());
  document.getElementById("checkout").disabled = state.cart.length === 0;
  document.getElementById("statCart").textContent = String(countItems());
  if (!state.cart.length) {
    root.innerHTML = `<p class="empty">Корзина пустая — загляни на витрину.</p>`;
    return;
  }
  root.innerHTML = "";
  state.cart.forEach((item) => {
    const row = document.createElement("div");
    row.className = "cart-line";
    row.innerHTML = `
      <div>
        <strong>${item.name}</strong>
        <p class="muted">${item.size} · ${money(item.price)}</p>
      </div>
      <div class="qty">
        <button type="button" data-act="dec">−</button>
        <span>${item.qty}</span>
        <button type="button" data-act="inc">+</button>
      </div>
    `;
    row.querySelector('[data-act="dec"]').onclick = () => changeQty(item.key, -1);
    row.querySelector('[data-act="inc"]').onclick = () => changeQty(item.key, 1);
    root.appendChild(row);
  });
}

function changeQty(key, delta) {
  const item = state.cart.find((entry) => entry.key === key);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) state.cart = state.cart.filter((entry) => entry.key !== key);
  saveState();
  haptic();
  renderCart();
  renderProfile();
}

function renderProfile() {
  const u = user();
  document.getElementById("greeting").textContent = `Привет, ${userName()}`;
  document.getElementById("profileName").textContent = u
    ? `${u.first_name}${u.last_name ? " " + u.last_name : ""}`
    : "Гость";
  document.getElementById("profileMeta").textContent = u?.username
    ? `@${u.username}`
    : u
      ? `id ${u.id}`
      : "Открой магазин из Telegram, чтобы подтянуть аккаунт";
  document.getElementById("avatar").textContent = (userName()[0] || "C").toUpperCase();
  document.getElementById("statFavs").textContent = String(state.favs.length);
  document.getElementById("statCart").textContent = String(countItems());
}

function showTab(name) {
  document.querySelectorAll(".page").forEach((page) => {
    page.classList.toggle("hidden", page.dataset.page !== name);
  });
  document.querySelectorAll(".tabs button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === name);
  });
  if (name === "cart") renderCart();
  if (name === "favs") renderFavs();
  if (name === "profile") renderProfile();
}

function checkout() {
  if (!state.cart.length) return;
  const payload = {
    shop: "CHASER",
    user: user(),
    note: document.getElementById("note").value.trim(),
    items: state.cart,
    total: cartSum(),
  };
  haptic("heavy");
  const text = `CHASER · ${money(payload.total)} · ${payload.items.length} поз.`;
  document.getElementById("doneText").textContent = text;
  if (tg?.sendData) {
    try {
      tg.sendData(JSON.stringify(payload));
    } catch {
      /* menu button web apps cannot sendData */
    }
  }
  state.cart = [];
  saveState();
  renderCart();
  document.getElementById("doneSheet").classList.remove("hidden");
}

function boot() {
  tg?.ready();
  tg?.expand();
  tg?.enableClosingConfirmation?.();
  tg?.setHeaderColor?.("secondary_bg_color");

  renderCats();
  renderCatalog();
  renderCart();
  renderFavs();
  renderProfile();

  document.getElementById("search").oninput = (e) => {
    query = e.target.value;
    renderCatalog();
  };
  document.getElementById("addToCart").onclick = addToCart;
  document.getElementById("favToggle").onclick = toggleFav;
  document.getElementById("checkout").onclick = checkout;
  document.getElementById("closeProduct").onclick = closeSheets;
  document.getElementById("closeDone").onclick = () => {
    closeSheets();
    showTab("shop");
  };
  document.querySelectorAll(".tabs button").forEach((btn) => {
    btn.onclick = () => {
      haptic();
      showTab(btn.dataset.tab);
    };
  });
  tg?.BackButton?.onClick(closeSheets);
}

boot();
