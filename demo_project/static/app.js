/**
 * JavaScript модуль для демонстрационного приложения.
 * 
 * Содержит функции для интерактивности, валидации форм
 * и работы с API.
 */

// Основной объект приложения
const DemoApp = {
    // Конфигурация
    config: {
        apiUrl: '/api',
        timeout: 5000,
        debug: false
    },
    
    // Инициализация
    init() {
        console.log('Инициализация демонстрационного приложения...');
        this.setupEventListeners();
        this.loadConfiguration();
        this.initializeComponents();
    },
    
    // Настройка обработчиков событий
    setupEventListeners() {
        // Обработчик для кнопок
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn')) {
                this.handleButtonClick(e.target);
            }
        });
        
        // Обработчик для форм
        document.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit(e.target);
        });
        
        // Обработчик для полей ввода
        document.addEventListener('input', (e) => {
            if (e.target.matches('.form-control')) {
                this.handleInputChange(e.target);
            }
        });
    },
    
    // Загрузка конфигурации
    loadConfiguration() {
        try {
            const config = localStorage.getItem('demoAppConfig');
            if (config) {
                this.config = { ...this.config, ...JSON.parse(config) };
            }
        } catch (error) {
            console.warn('Ошибка загрузки конфигурации:', error);
        }
    },
    
    // Сохранение конфигурации
    saveConfiguration() {
        try {
            localStorage.setItem('demoAppConfig', JSON.stringify(this.config));
        } catch (error) {
            console.warn('Ошибка сохранения конфигурации:', error);
        }
    },
    
    // Инициализация компонентов
    initializeComponents() {
        this.initializeTooltips();
        this.initializeModals();
        this.initializeTabs();
    },
    
    // Инициализация подсказок
    initializeTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip);
            element.addEventListener('mouseleave', this.hideTooltip);
        });
    },
    
    // Инициализация модальных окон
    initializeModals() {
        const modalTriggers = document.querySelectorAll('[data-modal]');
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', this.openModal);
        });
        
        const modalCloses = document.querySelectorAll('.modal-close');
        modalCloses.forEach(close => {
            close.addEventListener('click', this.closeModal);
        });
    },
    
    // Инициализация вкладок
    initializeTabs() {
        const tabTriggers = document.querySelectorAll('[data-tab]');
        tabTriggers.forEach(trigger => {
            trigger.addEventListener('click', this.switchTab);
        });
    },
    
    // Обработка клика по кнопке
    handleButtonClick(button) {
        const action = button.dataset.action;
        
        switch (action) {
            case 'save':
                this.saveData();
                break;
            case 'load':
                this.loadData();
                break;
            case 'reset':
                this.resetForm();
                break;
            case 'validate':
                this.validateForm();
                break;
            default:
                console.log('Неизвестное действие:', action);
        }
    },
    
    // Обработка отправки формы
    handleFormSubmit(form) {
        if (this.validateForm(form)) {
            this.submitForm(form);
        }
    },
    
    // Обработка изменения поля ввода
    handleInputChange(input) {
        this.validateField(input);
        this.updateFormState();
    },
    
    // Валидация формы
    validateForm(form = null) {
        const targetForm = form || document.querySelector('form');
        if (!targetForm) return false;
        
        const fields = targetForm.querySelectorAll('.form-control[required]');
        let isValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    },
    
    // Валидация поля
    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const required = field.hasAttribute('required');
        
        // Очистка предыдущих ошибок
        this.clearFieldError(field);
        
        // Проверка обязательности
        if (required && !value) {
            this.showFieldError(field, 'Это поле обязательно для заполнения');
            return false;
        }
        
        // Проверка типа
        if (value) {
            switch (type) {
                case 'email':
                    if (!this.isValidEmail(value)) {
                        this.showFieldError(field, 'Введите корректный email');
                        return false;
                    }
                    break;
                case 'url':
                    if (!this.isValidUrl(value)) {
                        this.showFieldError(field, 'Введите корректный URL');
                        return false;
                    }
                    break;
                case 'number':
                    if (isNaN(value)) {
                        this.showFieldError(field, 'Введите корректное число');
                        return false;
                    }
                    break;
            }
        }
        
        return true;
    },
    
    // Проверка email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    // Проверка URL
    isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    },
    
    // Показать ошибку поля
    showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        const errorElement = document.createElement('div');
        errorElement.className = 'invalid-feedback';
        errorElement.textContent = message;
        
        field.parentNode.appendChild(errorElement);
    },
    
    // Очистить ошибку поля
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    },
    
    // Обновить состояние формы
    updateFormState() {
        const form = document.querySelector('form');
        if (!form) return;
        
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            const isValid = this.validateForm(form);
            submitButton.disabled = !isValid;
        }
    },
    
    // Отправить форму
    submitForm(form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        console.log('Отправка данных:', data);
        
        // Показать индикатор загрузки
        this.showLoading();
        
        // Имитация отправки
        setTimeout(() => {
            this.hideLoading();
            this.showAlert('Данные успешно отправлены!', 'success');
            form.reset();
        }, 1000);
    },
    
    // Сохранить данные
    saveData() {
        const data = this.collectFormData();
        localStorage.setItem('demoAppData', JSON.stringify(data));
        this.showAlert('Данные сохранены!', 'success');
    },
    
    // Загрузить данные
    loadData() {
        try {
            const data = localStorage.getItem('demoAppData');
            if (data) {
                const parsedData = JSON.parse(data);
                this.populateForm(parsedData);
                this.showAlert('Данные загружены!', 'info');
            } else {
                this.showAlert('Нет сохраненных данных', 'warning');
            }
        } catch (error) {
            this.showAlert('Ошибка загрузки данных', 'danger');
        }
    },
    
    // Сбросить форму
    resetForm() {
        const form = document.querySelector('form');
        if (form) {
            form.reset();
            this.clearAllErrors();
            this.showAlert('Форма сброшена', 'info');
        }
    },
    
    // Собрать данные формы
    collectFormData() {
        const form = document.querySelector('form');
        if (!form) return {};
        
        const formData = new FormData(form);
        return Object.fromEntries(formData.entries());
    },
    
    // Заполнить форму данными
    populateForm(data) {
        Object.entries(data).forEach(([key, value]) => {
            const field = document.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = value;
            }
        });
    },
    
    // Очистить все ошибки
    clearAllErrors() {
        const errorElements = document.querySelectorAll('.invalid-feedback');
        errorElements.forEach(element => element.remove());
        
        const invalidFields = document.querySelectorAll('.is-invalid');
        invalidFields.forEach(field => field.classList.remove('is-invalid'));
    },
    
    // Показать подсказку
    showTooltip(event) {
        const element = event.target;
        const text = element.dataset.tooltip;
        
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            pointer-events: none;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        
        element._tooltip = tooltip;
    },
    
    // Скрыть подсказку
    hideTooltip(event) {
        const element = event.target;
        if (element._tooltip) {
            element._tooltip.remove();
            delete element._tooltip;
        }
    },
    
    // Открыть модальное окно
    openModal(event) {
        const modalId = event.target.dataset.modal;
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            modal.classList.add('show');
        }
    },
    
    // Закрыть модальное окно
    closeModal(event) {
        const modal = event.target.closest('.modal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
    },
    
    // Переключить вкладку
    switchTab(event) {
        const tabId = event.target.dataset.tab;
        
        // Скрыть все вкладки
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Убрать активность с всех кнопок
        document.querySelectorAll('[data-tab]').forEach(button => {
            button.classList.remove('active');
        });
        
        // Показать выбранную вкладку
        const tabContent = document.getElementById(tabId);
        if (tabContent) {
            tabContent.classList.add('active');
            event.target.classList.add('active');
        }
    },
    
    // Показать индикатор загрузки
    showLoading() {
        const loading = document.createElement('div');
        loading.id = 'loading';
        loading.innerHTML = '<div class="spinner"></div>';
        loading.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        
        document.body.appendChild(loading);
    },
    
    // Скрыть индикатор загрузки
    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.remove();
        }
    },
    
    // Показать уведомление
    showAlert(message, type = 'info') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.textContent = message;
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            min-width: 300px;
        `;
        
        document.body.appendChild(alert);
        
        // Автоматически скрыть через 3 секунды
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    DemoApp.init();
});

// Экспорт для использования в других модулях
window.DemoApp = DemoApp;
