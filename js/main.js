// ===== 字體大小配置 =====
// 可用的字體大小類別陣列（從小到大）
const AVAILABLE_FONT_SIZES = [
  // 'text-xs',      // 12px
  // 'text-sm',      // 14px
  // 'text-base',    // 16px
  // 'text-lg',      // 18px
  'text-xl',      // 20px
  'text-2xl',     // 24px
  'text-3xl',     // 30px
  'text-4xl',     // 36px (預設)
  'text-5xl',     // 48px
  'text-6xl',     // 60px
  // 'text-7xl',     // 72px
  // 'text-8xl',     // 96px
  // 'text-9xl'      // 128px
];

// ===== 狀態管理 =====
const DEFAULT_FONT_SIZE = 'text-4xl';

// ===== DOM 元素 =====
const mainElement = document.getElementById('main');
const fontIncreaseButton = document.getElementById('increaseFontSizeButton');
const fontDecreaseButton = document.getElementById('decreaseFontSizeButton');

// 從頁面實際字體大小初始化索引，如果找不到則使用預設值
function getCurrentFontSizeIndex() {
  // 檢查 main 元素當前使用的字體大小類別
  for (let i = 0; i < AVAILABLE_FONT_SIZES.length; i++) {
    if (mainElement.classList.contains(AVAILABLE_FONT_SIZES[i])) {
      return i;
    }
  }
  // 如果找不到，返回預設字體大小的索引
  return AVAILABLE_FONT_SIZES.indexOf(DEFAULT_FONT_SIZE);
}

let currentFontSizeIndex = getCurrentFontSizeIndex();

// ===== 字體大小控制函數 =====

/**
 * 更新頁面字體大小
 * 移除所有字體大小類別，然後添加當前選中的類別
 */
function applyFontSizeToPage() {
  // 移除所有字體大小類別
  mainElement.classList.remove(...AVAILABLE_FONT_SIZES);
  // 添加當前選中的字體大小類別
  mainElement.classList.add(AVAILABLE_FONT_SIZES[currentFontSizeIndex]);
}

/**
 * 增加字體大小
 * 檢查是否已達到最大字體大小限制
 */
function increaseFontSize() {
  if (currentFontSizeIndex < AVAILABLE_FONT_SIZES.length - 1) {
    currentFontSizeIndex++;
    applyFontSizeToPage();
  }
}

/**
 * 減少字體大小
 * 檢查是否已達到最小字體大小限制
 */
function decreaseFontSize() {
  const minFontSizeIndex = 0;
  
  if (currentFontSizeIndex > minFontSizeIndex) {
    currentFontSizeIndex--;
    applyFontSizeToPage();
  }
}

// ===== 事件監聽器設置 =====
fontIncreaseButton.addEventListener('click', increaseFontSize);
fontDecreaseButton.addEventListener('click', decreaseFontSize);
