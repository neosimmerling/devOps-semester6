const API = '/api';
let activeListId = null;
let lists = [];

async function apiFetch(path, opts = {}) {
  const res = await fetch( API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...opts
  });
  if (res.status === 204) return null;
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function loadLists() {
  lists = await apiFetch(`/lists/`);
  renderLists();
}

function renderLists() {
  const container = document.getElementById('lists-container');
  if (!lists.length) {
    container.innerHTML = '<div class="empty-state"><p>Keine Listen vorhanden</p></div>';
    return;
  }
  container.innerHTML = lists.map(l => {
    const total = l.items.length;
    const done = l.items.filter(i => i.is_checked).length;
    const active = l.id === activeListId ? 'active' : '';
    return `
    <div class="list-item ${active}" onclick="selectList(${l.id})">
      <div class="list-item-info">
        <div class="list-item-name">${esc(l.name)}</div>
        <div class="list-item-count">${done}/${total} erledigt</div>
      </div>
      <button class="btn btn-danger" onclick="event.stopPropagation(); deleteList(${l.id})" title="Löschen">✕</button>
    </div>`;
  }).join('');
}

async function  selectList(id) {
  activeListId = id;
  renderLists();
  const lst = lists.find(l => l.id === id);
  renderMain(lst);  
}

function renderMain(lst) {
  const main = document.getElementById('main-panel');
  const total = lst.items.length;
  const done = lst.items.filter(i => i.is_checked).length;
  const pct = total > 0 ? Math.round(done / total * 100) : 0;

  main.innerHTML = `
    <div class="main-header">
      <h2 id="list-title">${esc(lst.name)}</h2>
      <span class="badge">${pct}%</span>
    </div>
    <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
    <div class="add-item-bar">
      <input type="text" id="item-name" placeholder="Artikel hinzufügen…" onkeydown="if(event.key==='Enter') addItem()" />
      <input type="number" id="item-qty" class="qty-input" placeholder="Anz." value="1" min="1" />
      <select id="item-unit" class="unit-input">
        <option value="Stück">Stück</option>
        <option value="kg">kg</option>
        <option value="g">g</option>
        <option value="l">l</option>
        <option value="ml">ml</option>
        <option value="Packung">Packung</option>
        <option value="Flasche">Flasche</option>
        <option value="Dose">Dose</option>
      </select>
      <button class="btn btn-primary" onclick="addItem()">Hinzufügen</button>
    </div>
    <div class="items-container" id="items-container">
      ${renderItems(lst.items)}
    </div>`;
}

function renderItems(items) {
  if (!items.length) return `<div class="empty-state"><div class="icon">📋</div><p>Noch keine Artikel in dieser Liste.</p></div>`;
  return items.map(item =>  `
    <div class="item-row ${item.is_checked ? 'checked' : ''}" id="item-${item.id}">
      <input type="checkbox" class="item-checkbox" ${item.is_checked ? 'checked' : ''}
        onchange="toggleItem(${item.id}, this.checked)" />
      <span class="item-name">${esc(item.name)}</span>
      <span class="item-qty">${item.quantity} ${esc(item.unit)}</span>
      <button class="btn btn-icon" onclick="startEditItem(${item.id})" title="Bearbeiten">✏️</button>
      <button class="btn btn-danger" onclick="deleteItem(${item.id})" title="Löschen">✕</button>
    </div>`).join('');
}

async function createList() {
  const input = document.getElementById('new-list-input');
  const name = input.value.trim();
  if (!name) return;
  await apiFetch(`/lists/`, {method: 'POST', body: JSON.stringify({ name })});
  input.value = '';
  await loadLists();
}

async function deleteList(id) {
  if (!confirm('Liste wirklich löschen?')) return;
  await apiFetch(`/lists/${id}`, { method: 'DELETE'});
  if (activeListId === id) {
    activeListId = null;
    document.getElementById('main-panel').innerHTML = 
    '<div class="empty-state" style="margin:auto;"><div class="icon">👈</div><p>Wähle eine Liste aus.</p></div>';
  }
  await loadLists();
}

async function addItem() {
  const name = document.getElementById('item-name').value.trim();
  const quantity = parseInt(document.getElementById('item-qty').value) || 1;
  const unit = document.getElementById('item-unit').value;
  if (!name) return;
  await apiFetch(`/items/`, {method: 'POST', body: JSON.stringify({ list_id: activeListId, name, quantity, unit }) });
  document.getElementById('item-name').value = '';
  await refreshActive();
}

async function toggleItem(id, checked) {
  await apiFetch(`/items/${id}`, { method: 'PUT', body: JSON.stringify({ is_checked: checked}) });
  await refreshActive();
}

async function deleteItem(id) {
  await apiFetch(`/items/${id}`, { method: 'DELETE'});
  await refreshActive();
}

function startEditItem(id) {
  const lst = lists.find(l => l.id === activeListId);
  const item = lst.items.find(i => i.id === id);
  const row = document.getElementById(`item-${id}`);
  row.innerHTML = `
    <div class="item-edit-form">
      <input id="edit-name-${id}" value="${esc(item.name)}" style="flex:1" />
      <input id="edit-qty-${id}" type="number" value="${item.quantity}" style="width:60px" />
      <select id="edit-unit-${id}" style="width:90px">
        <option value="Stück" ${item.unit === 'Stück' ? 'selected': ''}>Stück</option>
        <option value="kg" ${item.unit === 'kg' ? 'selected': ''}>kg</option>
        <option value="g" ${item.unit === 'g' ? 'selected': ''}>g</option>
        <option value="l" ${item.unit === 'l' ? 'selected': ''}>l</option>
        <option value="ml" ${item.unit === 'ml' ? 'selected': ''}>ml</option>
        <option value="Packung" ${item.unit === 'Packung' ? 'selected': ''}>Packung</option>
        <option value="Flasche" ${item.unit === 'Flasche' ? 'selected': ''}>Flasche</option>
        <option value="Dose" ${item.unit === 'Dose' ? 'selected': ''}>Dose</option>
      </select>
      <button class="btn btn-primary" onclick="saveEditItem(${id})">Speichern</button>
      <button class="btn btn-icon" onclick="renderMain(lists.find(l=>l.id===activeListId))">✕</button>
    </div>`;
}

async function saveEditItem(id) {
  const name = document.getElementById(`edit-name-${id}`).value.trim();
  const quantity = parseInt(document.getElementById(`edit-qty-${id}`).value) || 1;
  const unit = document.getElementById(`edit-unit-${id}`).value.trim();
  if (!name) return;
  await apiFetch(`/items/${id}`, { method: 'PUT', body: JSON.stringify({name, quantity, unit}) });
  await refreshActive();
}

async function refreshActive() {
  await loadLists();
  const lst = lists.find(l => l.id === activeListId);
  if (lst) renderMain(lst);  
}

function esc(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

document.getElementById('new-list-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') createList();
});

loadLists();