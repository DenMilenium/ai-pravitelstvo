'use client';

import { useState } from 'react';
import { Send, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { useAppeal } from '@/lib/api';

export default function AppealForm() {
  const { submitAppeal, submitting, success, error } = useAppeal();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const errors: Record<string, string> = {};
    
    if (!formData.full_name.trim() || formData.full_name.length < 2) {
      errors.full_name = 'Введите полное имя (минимум 2 символа)';
    }
    
    if (!formData.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Введите корректный email';
    }
    
    if (!formData.subject.trim() || formData.subject.length < 5) {
      errors.subject = 'Введите тему (минимум 5 символов)';
    }
    
    if (!formData.message.trim() || formData.message.length < 20) {
      errors.message = 'Введите сообщение (минимум 20 символов)';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    try {
      await submitAppeal(formData);
      setFormData({ full_name: '', email: '', phone: '', subject: '', message: '' });
    } catch {
      // Error handled in hook
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  if (success) {
    return (
      <div className="max-w-2xl mx-auto p-8 bg-green-50 rounded-2xl border border-green-200 text-center">
        <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
        <h3 className="text-2xl font-bold text-green-800 mb-2">Обращение отправлено!</h3>
        <p className="text-green-700 mb-6">
          Спасибо за обращение. Мы рассмотрим его в ближайшее время и ответим на указанный email.
        </p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors"
        >
          Отправить ещё одно обращение
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-6">
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 shrink-0" />
          <div>
            <p className="font-medium text-red-800">Ошибка отправки</p>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="full_name" className="block text-sm font-medium text-slate-700 mb-2">
            ФИО *
          </label>
          <input
            type="text"
            id="full_name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            className={`w-full px-4 py-3 rounded-xl border ${formErrors.full_name ? 'border-red-300 bg-red-50' : 'border-slate-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all`}
            placeholder="Иванов Иван Иванович"
          />
          {formErrors.full_name && <p className="mt-1 text-sm text-red-600">{formErrors.full_name}</p>}
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
            Email *
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={`w-full px-4 py-3 rounded-xl border ${formErrors.email ? 'border-red-300 bg-red-50' : 'border-slate-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all`}
            placeholder="ivan@example.com"
          />
          {formErrors.email && <p className="mt-1 text-sm text-red-600">{formErrors.email}</p>}
        </div>
      </div>

      <div>
        <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-2">
          Телефон
        </label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          placeholder="+7 (999) 123-45-67"
        />
      </div>

      <div>
        <label htmlFor="subject" className="block text-sm font-medium text-slate-700 mb-2">
          Тема обращения *
        </label>
        <input
          type="text"
          id="subject"
          name="subject"
          value={formData.subject}
          onChange={handleChange}
          className={`w-full px-4 py-3 rounded-xl border ${formErrors.subject ? 'border-red-300 bg-red-50' : 'border-slate-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all`}
          placeholder="Укажите тему вашего обращения"
        />
        {formErrors.subject && <p className="mt-1 text-sm text-red-600">{formErrors.subject}</p>}
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-slate-700 mb-2">
          Сообщение *
        </label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          rows={6}
          className={`w-full px-4 py-3 rounded-xl border ${formErrors.message ? 'border-red-300 bg-red-50' : 'border-slate-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none`}
          placeholder="Опишите ваш вопрос или проблему подробно..."
        />
        {formErrors.message && <p className="mt-1 text-sm text-red-600">{formErrors.message}</p>}
        <p className="mt-1 text-sm text-slate-500">Минимум 20 символов</p>
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="w-full py-4 bg-gradient-to-r from-blue-700 to-blue-800 text-white rounded-xl font-semibold text-lg hover:shadow-xl hover:shadow-blue-500/30 hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
      >
        {submitting ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Отправка...
          </>
        ) : (
          <>
            <Send className="w-5 h-5" />
            Отправить обращение
          </>
        )}
      </button>

      <p className="text-sm text-slate-500 text-center">
        Нажимая кнопку, вы соглашаетесь с{' '}
        <a href="#" className="text-blue-600 hover:underline">политикой конфиденциальности</a>
      </p>
    </form>
  );
}
