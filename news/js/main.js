// 全球新闻日报 - 交互脚本

// 移动端菜单切换
function toggleMenu() {
  const nav = document.querySelector(".main-nav");
  if (nav) { nav.classList.toggle("open"); }
}

// 分类筛选
document.addEventListener("DOMContentLoaded", function () {
  const filterBtns = document.querySelectorAll(".filter-btn");
  const catSections = document.querySelectorAll(".cat-section");
  const topStories = document.querySelector(".top-stories");

  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cat = this.getAttribute("data-cat");

      // 更新按钮状态
      filterBtns.forEach(function (b) { b.classList.remove("active"); });
      this.classList.add("active");

      // 显示/隐藏分类
      if (cat === "all") {
        catSections.forEach(function (s) { s.style.display = ""; });
        if (topStories) topStories.style.display = "";
      } else {
        catSections.forEach(function (s) {
          s.style.display = s.getAttribute("data-category") === cat ? "" : "none";
        });
        if (topStories) topStories.style.display = "none";
      }
    });
  });

  // 键盘导航
  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      var arrows = document.querySelectorAll(".nav-arrow");
      var idx = e.key === "ArrowLeft" ? 0 : (arrows.length > 1 ? 1 : 0);
      if (arrows[idx]) { window.location.href = arrows[idx].getAttribute("href"); }
    }
  });
});
