// 可用的字體大小/行高組合（從小到大）
const FONT_SIZE_TABLE = [
  'text-xl/8',
  'text-2xl/9',
  'text-3xl/11', // 預設值
  'text-4xl/13',
  'text-5xl/15',
  'text-6xl/18',
];

// 初始化並綁定按鈕事件
document.addEventListener('DOMContentLoaded', () => {
  const mainEl = document.getElementById('main');
  const incBtn = document.getElementById('increaseFontSizeButton');
  const decBtn = document.getElementById('decreaseFontSizeButton');

  if (!mainEl || !incBtn || !decBtn) return;

  // 套用預設字體大小
  let defaultIndex = FONT_SIZE_TABLE.indexOf('text-3xl/11');
  let currentFontIndex = defaultIndex;
  applyFontSize(defaultIndex);


  function applyFontSize(index) {
    // 移除所有已知的字體 class，然後加上指定的 class
    mainEl.classList.remove(...FONT_SIZE_TABLE);
    mainEl.classList.add(FONT_SIZE_TABLE[index]);
    // 更新按鈕的 disabled 狀態（邊界時禁用）
    incBtn.disabled = index >= FONT_SIZE_TABLE.length - 1;
    decBtn.disabled = index <= 0;
  }

  incBtn.addEventListener('click', () => {
    if (currentFontIndex < FONT_SIZE_TABLE.length - 1) {
      currentFontIndex += 1;
      applyFontSize(currentFontIndex);
    }
  });

  decBtn.addEventListener('click', () => {
    if (currentFontIndex > 0) {
      currentFontIndex -= 1;
      applyFontSize(currentFontIndex);
    }
  });

});


