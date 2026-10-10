/* WordHunter - офлайн-оболонка.
   Цей файл між версіями НЕ змінюється: інакше браузер сам поставить новий
   service worker і гра оновиться без дозволу. Нову версію ставить сама гра
   після «🔄 Оновити»: чистить кеш, знімає service worker і перезавантажується. */
const CACHE = "wordhunter";
const APP_FILES = ["./", "./index.html", "./manifest.json", "./icon-192.png", "./icon-512.png"];
const fresh = u => new Request(u, { cache: "reload" });

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(APP_FILES.map(u => c.add(fresh(u)).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;            // перекладач, озвучка - як є
  if (url.pathname.endsWith("/version.json") || url.searchParams.has("t")) return;   // перевірка оновлень - лише мережа
  // спершу збережене (так нова версія не підміняє стару сама), інакше мережа
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(req, { ignoreSearch: true }) || (req.mode === "navigate" ? await c.match("./index.html") : null);
    if (hit) return hit;
    try { const res = await fetch(req); if (res && res.ok) c.put(req, res.clone()); return res; }
    catch (err) { return new Response("", { status: 504, statusText: "offline" }); }
  }));
});
