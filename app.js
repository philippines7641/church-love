const numberInput = document.getElementById("number");
const searchBtn = document.getElementById("searchBtn");
const message = document.getElementById("message");
const songInfo = document.getElementById("songInfo");
const category = document.getElementById("category");
const title = document.getElementById("title");
const playerBox = document.getElementById("playerBox");
const player = document.getElementById("player");
const empty = document.getElementById("empty");

let songs = [];

async function loadSongs() {
  const response = await fetch("songs.json");
  songs = await response.json();
}

function playSong() {
  const number = String(numberInput.value).trim();
  const song = songs.find(item => item.number === number);

  if (!song) {
    message.textContent = "등록된 찬송가가 없습니다.";
    songInfo.classList.add("hidden");
    playerBox.classList.add("hidden");
    empty.classList.remove("hidden");
    return;
  }

  category.textContent = `${song.category} ${song.number}장`;
  title.textContent = song.title;
  songInfo.classList.remove("hidden");
  empty.classList.add("hidden");

  if (song.youtubeId) {
    player.src = `https://www.youtube.com/embed/${song.youtubeId}?autoplay=1&rel=0`;
    playerBox.classList.remove("hidden");
    message.textContent = "영상을 불러왔습니다.";
  } else {
    player.src = "";
    playerBox.classList.add("hidden");
    message.textContent = "이 곡은 아직 재생 영상이 연결되지 않았습니다.";
  }
}

searchBtn.addEventListener("click", playSong);
numberInput.addEventListener("keydown", e => {
  if (e.key === "Enter") playSong();
});

loadSongs().catch(() => {
  message.textContent = "DB 파일을 불러오지 못했습니다.";
});
