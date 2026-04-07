'use client';

import { useState, useEffect } from 'react';
import { 
  Scale, 
  FileText, 
  Search, 
  CreditCard, 
  Video, 
  ChevronRight,
  Menu,
  X,
  Phone,
  Mail,
  MapPin,
  ArrowUpRight
} from 'lucide-react';

// Анимированный счётчик
function CountUp({ end, duration = 2000 }: { end: number; duration?: number }) {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    let startTime: number;
    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      setCount(Math.floor(progress * end));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
  }, [end, duration]);
  
  return <span>{count.toLocaleString()}</span>;
}

// Карточка с hover-эффектом
function GlassCard({ 
  children, 
  className = '' 
}: { 
  children: React.ReactNode; 
  className?: string 
}) {
  return (
    <div 
      className={`
        relative overflow-hidden rounded-2xl
        bg-white/80 backdrop-blur-xl
        border border-white/20
        shadow-[0_8px_32px_rgba(31,38,135,0.15)]
        hover:shadow-[0_8px_32px_rgba(31,38,135,0.25)]
        hover:scale-[1.02]
        transition-all duration-500 ease-out
        ${className}
      `}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/40 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-500" />
      {children}
    </div>
  );
}

// Новостная карточка
function NewsCard({ 
  date, 
  title, 
  excerpt 
}: { 
  date: string; 
  title: string; 
  excerpt: string 
}) {
  return (
    <GlassCard className="group cursor-pointer">
      <div className="p-6 relative z-10">
        <span className="inline-block px-3 py-1 text-xs font-medium bg-gradient-to-r from-amber-400 to-amber-500 text-slate-900 rounded-full mb-4">
          {date}
        </span>
        <h3 className="text-lg font-semibold text-slate-800 mb-3 group-hover:text-blue-700 transition-colors line-clamp-2">
          {title}
        </h3>
        <p className="text-slate-600 text-sm line-clamp-3 mb-4">{excerpt}</p>
        <div className="flex items-center text-blue-600 text-sm font-medium group-hover:gap-2 transition-all">
          Читать далее <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </div>
      </div>
    </GlassCard>
  );
}

// Сервис карточка
function ServiceCard({ 
  icon: Icon, 
  title, 
  description 
}: { 
  icon: React.ElementType; 
  title: string; 
  description: string 
}) {
  return (
    <GlassCard className="group cursor-pointer h-full">
      <div className="p-8 relative z-10 h-full flex flex-col">
        <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-500 shadow-lg">
          <Icon className="w-7 h-7 text-white" />
        </div>
        <h3 className="text-xl font-semibold text-slate-800 mb-3">{title}</h3>
        <p className="text-slate-600 flex-grow">{description}</p>
        <div className="mt-6 flex items-center text-blue-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
          Перейти <ArrowUpRight className="w-4 h-4 ml-1" />
        </div>
      </div>
    </GlassCard>
  );
}

// Главная страница
export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'Главная', href: '#' },
    { name: 'О департаменте', href: '#about' },
    { name: 'Новости', href: '#news' },
    { name: 'Документы', href: '#documents' },
    { name: 'Электронное правосудие', href: '#ejustice' },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100">
      {/* Header */}
      <header 
        className={`
          fixed top-0 left-0 right-0 z-50 transition-all duration-500
          ${scrolled 
            ? 'bg-white/90 backdrop-blur-xl shadow-lg py-3' 
            : 'bg-transparent py-5'
          }
        `}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center text-2xl shadow-lg shadow-blue-500/30">
                <Scale className="w-7 h-7 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className={`font-bold transition-colors ${scrolled ? 'text-slate-800' : 'text-slate-800'}`}>
                  Судебный департамент
                </h1>
                <p className={`text-xs transition-colors ${scrolled ? 'text-slate-500' : 'text-slate-500'}`}>
                  при Верховном суде РФ
                </p>
              </div>
            </div>

            {/* Desktop Nav */}
            <nav className="hidden lg:flex items-center space-x-1">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className={`
                    px-4 py-2 rounded-lg text-sm font-medium transition-all
                    ${scrolled 
                      ? 'text-slate-600 hover:text-blue-600 hover:bg-blue-50' 
                      : 'text-slate-700 hover:text-blue-600 hover:bg-white/50'
                    }
                  `}
                >
                  {link.name}
                </a>
              ))}
            </nav>

            {/* CTA Button */}
            <div className="hidden md:flex items-center space-x-4">
              <button className="px-5 py-2.5 bg-gradient-to-r from-amber-400 to-amber-500 text-slate-900 rounded-lg font-semibold text-sm hover:shadow-lg hover:shadow-amber-400/30 hover:scale-105 transition-all">
                Личный кабинет
              </button>
            </div>

            {/* Mobile Menu Button */}
            <button 
              className="lg:hidden p-2 rounded-lg hover:bg-slate-100"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="lg:hidden absolute top-full left-0 right-0 bg-white/95 backdrop-blur-xl shadow-xl border-t border-slate-100">
            <div className="px-4 py-4 space-y-2">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="block px-4 py-3 rounded-lg text-slate-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {link.name}
                </a>
              ))}
              <button className="w-full mt-4 px-5 py-3 bg-gradient-to-r from-amber-400 to-amber-500 text-slate-900 rounded-lg font-semibold">
                Личный кабинет
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-3xl transform translate-x-1/3 -translate-y-1/4" />
          <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-amber-400/10 to-orange-400/10 rounded-full blur-3xl transform -translate-x-1/3 translate-y-1/4" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 text-blue-700 text-sm font-medium mb-8">
              <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
              Официальный портал правосудия
            </div>
            
            <h2 className="text-4xl sm:text-5xl lg:text-7xl font-bold text-slate-800 mb-6 leading-tight">
              Судебный{' '}
              <span className="bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                департамент
              </span>
            </h2>
            
            <p className="text-lg sm:text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
              Организационное обеспечение деятельности судов общей юрисдикции 
              и арбитражных судов Российской Федерации
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="group px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl font-semibold text-lg hover:shadow-xl hover:shadow-blue-500/30 hover:scale-105 transition-all flex items-center justify-center gap-2">
                Электронное правосудие
                <ArrowUpRight className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
              </button>
              <button className="px-8 py-4 bg-white/80 backdrop-blur text-slate-700 border border-slate-200 rounded-xl font-semibold text-lg hover:bg-white hover:border-slate-300 hover:shadow-lg transition-all">
                Подача документов
              </button>
            </div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-slate-400 rounded-full flex justify-center pt-2">
            <div className="w-1.5 h-3 bg-slate-400 rounded-full" />
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { value: 3200, suffix: '+', label: 'Судов в системе', icon: Scale },
              { value: 25000, suffix: '+', label: 'Судей', icon: FileText },
              { value: 15000000, suffix: '+', label: 'Дел в год', icon: Search },
              { value: 5000000, suffix: '+', label: 'Пользователей ГАС', icon: CreditCard },
            ].map((stat, idx) => (
              <GlassCard key={idx} className="text-center p-8">
                <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                  <stat.icon className="w-6 h-6 text-blue-600" />
                </div>
                <div className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent mb-2">
                  <CountUp end={stat.value} />{stat.suffix}
                </div>
                <div className="text-slate-500 text-sm">{stat.label}</div>
              </GlassCard>
            ))}
          </div>
        </div>
      </section>

      {/* E-Justice Services */}
      <section id="ejustice" className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h3 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-4">
              Электронное правосудие
            </h3>
            <p className="text-slate-600 text-lg max-w-2xl mx-auto">
              Современные цифровые сервисы для участников судебного процесса
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <ServiceCard
              icon={FileText}
              title="Подача документов"
              description="Подайте исковое заявление или жалобу онлайн через ГАС «Правосудие» без посещения суда"
            />
            <ServiceCard
              icon={Search}
              title="Проверка статуса"
              description="Отслеживайте ход рассмотрения вашего дела в режиме реального времени"
            />
            <ServiceCard
              icon={CreditCard}
              title="Оплата пошлин"
              description="Оплатите государственную пошлину онлайн без комиссии и очередей"
            />
            <ServiceCard
              icon={Video}
              title="Видеоконференции"
              description="Участвуйте в судебных заседаниях удалённо через безопасное видеосоединение"
            />
            <ServiceCard
              icon={FileText}
              title="Копии документов"
              description="Закажите и получите копии судебных документов в электронном виде"
            />
            <ServiceCard
              icon={Scale}
              title="Мои дела"
              description="Управляйте всеми своими делами в едином личном кабинете"
            />
          </div>
        </div>
      </section>

      {/* News Section */}
      <section id="news" className="py-20 bg-gradient-to-b from-transparent to-slate-100/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-12">
            <div>
              <h3 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-4">
                Новости
              </h3>
              <p className="text-slate-600">
                Актуальная информация о деятельности судебной системы
              </p>
            </div>
            <a 
              href="#" 
              className="mt-4 sm:mt-0 inline-flex items-center text-blue-600 font-medium hover:text-blue-700 group"
            >
              Все новости 
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <NewsCard
              date="15 марта 2024"
              title="Совещание по внедрению цифровых технологий в судебную систему"
              excerpt="Под председательством заместителя Председателя Верховного Суда состоялось рабочее совещание по вопросам цифровизации..."
            />
            <NewsCard
              date="12 марта 2024"
              title="Обновление ГАС «Правосудие»: новые функции для участников процесса"
              excerpt="В системе появились новые возможности для подачи процессуальных документов и взаимодействия с судами..."
            />
            <NewsCard
              date="8 марта 2024"
              title="Судебный департамент подвел итоги работы за 2023 год"
              excerpt="В отчетном периоде значительно увеличилось количество электронных обращений граждан..."
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <GlassCard className="p-8 sm:p-12 text-center bg-gradient-to-br from-blue-600 to-blue-800 text-white">
            <h3 className="text-3xl sm:text-4xl font-bold mb-4">
              Нужна помощь?
            </h3>
            <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto">
              Наши специалисты готовы ответить на ваши вопросы по работе 
              электронных сервисов судебной системы
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-4 bg-white text-blue-700 rounded-xl font-semibold hover:shadow-xl hover:scale-105 transition-all">
                Написать в поддержку
              </button>
              <button className="px-8 py-4 bg-blue-700 text-white border border-blue-500 rounded-xl font-semibold hover:bg-blue-600 transition-all">
                Частые вопросы
              </button>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
            {/* Brand */}
            <div>
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-amber-400 to-amber-500 flex items-center justify-center">
                  <Scale className="w-6 h-6 text-slate-900" />
                </div>
                <div>
                  <h4 className="font-bold text-lg">Судебный департамент</h4>
                  <p className="text-slate-400 text-sm">при Верховном суде РФ</p>
                </div>
              </div>
              <p className="text-slate-400 text-sm leading-relaxed">
                Организационное обеспечение деятельности судов общей 
                юрисдикции и арбитражных судов Российской Федерации
              </p>
            </div>

            {/* Links */}
            <div>
              <h5 className="font-semibold mb-6 text-lg">Разделы</h5>
              <ul className="space-y-3 text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">О департаменте</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Деятельность</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Документы</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Статистика</a></li>
              </ul>
            </div>

            {/* Services */}
            <div>
              <h5 className="font-semibold mb-6 text-lg">Сервисы</h5>
              <ul className="space-y-3 text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">Электронное правосудие</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Картотека дел</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Расписание слушаний</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Видеоконференции</a></li>
              </ul>
            </div>

            {/* Contacts */}
            <div>
              <h5 className="font-semibold mb-6 text-lg">Контакты</h5>
              <ul className="space-y-4 text-slate-400">
                <li className="flex items-start gap-3">
                  <MapPin className="w-5 h-5 text-amber-400 mt-0.5 shrink-0" />
                  <span>121260, Москва, ул. Новый Арбат, 16</span>
                </li>
                <li className="flex items-center gap-3">
                  <Phone className="w-5 h-5 text-amber-400 shrink-0" />
                  <span>+7 (495) 606-16-16</span>
                </li>
                <li className="flex items-center gap-3">
                  <Mail className="w-5 h-5 text-amber-400 shrink-0" />
                  <span>info@court.gov.ru</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom */}
          <div className="border-t border-slate-800 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-slate-500 text-sm">
              © 2024 Судебный департамент при Верховном суде Российской Федерации
            </p>
            <div className="flex gap-6 text-slate-500 text-sm">
              <a href="#" className="hover:text-white transition-colors">Политика конфиденциальности</a>
              <a href="#" className="hover:text-white transition-colors">Карта сайта</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
