let database = { songs: [] };

const input = document.getElementById('searchInput');
const button = document.getElementById('searchBtn');
const results = document.getElementById('results');
const player = document.getElementById('player');
const songTitle = document.getElementById('songTitle');
const videoArea = document.getElementById('videoArea');

fetch('songs.json')
  .then(r => r.json())
  .then(data => { database = data; })
  .catch(() => { results.innerHTML = '<div class="notice">찬송가 자료를 불러오지 못했습니다.</div>'; });

function searchSongs() {
  const q = input.value.trim();
  if (!q) {
    results.innerHTML = '<div class="notice">찬송가 제목 또는 번호를 입력해 주세요.</div>';
    return;
  }

  const isNumber = /^\d+$/.test(q);
  const found = database.songs.filter(song => {
    if (isNumber) return String(song.number) === q;
    return String(song.title || '').toLowerCase().includes(q.toLowerCase());
  });

  if (!found.length) {
    results.innerHTML = '<div class="notice">검색 결과가 없습니다.</div>';
    player.hidden = true;
    return;
  }

  results.innerHTML = found.map((song, i) => `
    <div class="result-item" data-index="${i}">
      <span class="number">${song.number}</span>${escapeHtml(song.title)}
      <span class="category">${escapeHtml(song.category || '')}</span>
    </div>`).join('');

  results.querySelectorAll('.result-item').forEach(el => {
    el.addEventListener('click', () => playSong(found[Number(el.dataset.index)]));
  });
}

function playSong(song) {
  player.hidden = false;
  songTitle.textContent = `${song.number}. ${song.title}`;
  if (song.verified === true && song.vocal === 'none' && song.lyrics === 'embedded' && song.embeddable === true && song.videoUrl) {
    const id = getYoutubeId(song.videoUrl);
    if (id) {
      videoArea.innerHTML = `<div class="video-wrap"><iframe src="https://www.youtube.com/embed/${id}" title="${escapeHtml(song.title)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
      return;
    }
  }
  videoArea.innerHTML = '<div class="notice">영상 준비중</div>';
}

function getYoutubeId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes('youtu.be')) return u.pathname.slice(1);
    if (u.hostname.includes('youtube.com')) return u.searchParams.get('v') || (u.pathname.match(/\/embed\/([^/]+)/) || [])[1];
  } catch (_) {}
  return null;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

button.addEventListener('click', searchSongs);
input.addEventListener('keydown', e => { if (e.key === 'Enter') searchSongs(); });
