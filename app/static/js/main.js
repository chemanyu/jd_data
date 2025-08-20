// 主要JavaScript功能

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 为所有卡片添加动画类
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('card-animate');
        }, index * 100);
    });
    
    // 自动隐藏警告消息
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }
        }, 5000);
    });
    
    // 工具提示初始化
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// 格式化数字显示
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// 计算百分比
function calculatePercentage(part, total) {
    if (total === 0) return 0;
    return ((part / total) * 100).toFixed(1);
}

// 显示加载状态
function showLoading(buttonElement, text = '加载中...') {
    if (buttonElement) {
        buttonElement.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${text}`;
        buttonElement.disabled = true;
    }
}

// 隐藏加载状态
function hideLoading(buttonElement, originalText) {
    if (buttonElement) {
        buttonElement.innerHTML = originalText;
        buttonElement.disabled = false;
    }
}

// 复制文本到剪贴板
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('已复制到剪贴板', 'success');
    } catch (err) {
        console.error('复制失败: ', err);
        showToast('复制失败', 'error');
    }
}

// 显示提示消息
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // 自动移除
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// 创建Toast容器
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// 表格排序功能
function sortTable(table, column, type = 'string') {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.cells[column].textContent.trim();
        const bValue = b.cells[column].textContent.trim();
        
        if (type === 'number') {
            return parseFloat(aValue) - parseFloat(bValue);
        } else {
            return aValue.localeCompare(bValue);
        }
    });
    
    // 清空tbody并重新添加排序后的行
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

// 数据导出功能
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    const csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cells = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cells.length; j++) {
            row.push('"' + cells[j].textContent.trim().replace(/"/g, '""') + '"');
        }
        
        csv.push(row.join(','));
    }
    
    const csvString = csv.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// 全局错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript错误:', e.error);
});

// API请求封装
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API请求失败:', error);
        throw error;
    }
}
