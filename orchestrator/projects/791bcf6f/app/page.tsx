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
  ArrowUpRight,
  Building2,
  Users,
  Gavel,
  BookOpen,
  BarChart3,
  ExternalLink,
  Calendar
} from 'lucide-react';

// Анимированный счётчик
function CountUp({ end, duration = 2000, suffix = '' }: { end: number; duration?: number; suffix?: string }) {
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
  
  return <span>{count.toLocaleString()}{suffix}</span>;
}

// Карточка с hover-эффектом
function GlassCard({ children, className = '', hover = true }: { children: React.ReactNode; className?: string; hover?: boolean }) {
  return (
    <div className={`
      relative overflow-hidden rounded-2xl
      bg-white/80 backdrop-blur-xl
      border border-white/20
      shadow-[0_8px_32px_rgba(31,38,135,0.15)]
      ${hover ? 'hover:shadow-[0_8px_32px_rgba(31,38,135,0.25)] hover:scale-[1.02] transition-all duration-500' : ''}
      ${className}
    `}>
      <div className="absolute inset-0 bg-gradient-to-br from-white/40 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-500" />
      {children}
    </div>
  );
}

// Новостная карточка
function NewsCard({ date, title, href = '#' }: { date: string; title: string; href?: string }) {
  return (
    <a href={href} className="block group">
      <GlassCard className="h-full">
        <div className="p-6 relative z-10 h-full flex flex-col">
          <div className="flex items-center gap-2 text-sm text-slate-500 mb-3">
            <Calendar className="w-4 h-4" />
            {date}
          </div>
          <h3 className="text-lg font-semibold text-slate-800 group-hover:text-blue-700 transition-colors line-clamp-3 flex-grow">
            {title}
          </h3>
          <div className="mt-4 flex items-center text-blue-600 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
            Подробнее <ChevronRight className="w-4 h-4 ml-1" />
          </div>
        </div>
      </GlassCard>
    </a>
  );
}

// Сервис карточка
function ServiceCard({ icon: Icon, title, description, href = '#' }: { icon: React.ElementType; title: string; description: string; href?: string }) {
  return (
    <a href={href} className="block group h-full">
      <GlassCard className="h-full">
        <div className="p-8 relative z-10 h-full flex flex-col">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-500 shadow-lg shadow-blue-500/30">
            <Icon className="w-7 h-7 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-slate-800 mb-3">{title}</h3>
          <p className="text-slate-600 flex-grow">{description}</p>
          <div className="mt-6 flex items-center text-blue-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
            Перейти <ArrowUpRight className="w-4 h-4 ml-1" />
          </div>
        </div>
      </GlassCard>
    </a>
  );
}

// Ссылка на внешний ресурс
function ExternalLinkCard({ title, href, description }: { title: string; href: string; description: string }) {
  return (
    <a href={href} target="_blank" rel="noopener noreferrer" className="block group">
      <div className="p-4 rounded-xl bg-white/50 hover:bg-white/80 transition-all border border-slate-200 hover:border-blue-300">
        <div className="flex items-start gap-3">
          <ExternalLink className="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
          <div>
            <h4 className="font-semibold text-slate-800 group-hover:text-blue-700 transition-colors">{title}</h4>
            <p className="text-sm text-slate-500">{description}</p>
          </div>
        </div>
      </div>
    </a>
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

  // РЕАЛЬНЫЕ НОВОСТИ с cdep.ru
  const news = [
    { date: '01.04.2026', title: 'Проведены занятия по вопросам противодействия коррупции' },
    { date: '31.03.2026', title: 'Генеральный директор Судебного департамента принял участие в заседании Совета судей Российской Федерации' },
    { date: '30.03.2026', title: 'Состоялась встреча с заместителями председателей судов, прошедшими повышение квалификации в РГУП' },
    { date: '27.03.2026', title: 'Назначен начальник регионального управления Судебного департамента' },
    { date: '27.03.2026', title: 'В Судебном департаменте обсудили реализацию проектов капитального строительства' },
    { date: '26.03.2026', title: 'На Госуслугах появилась возможность подавать в суд документы в рамках уголовного судопроизводства' },
  ];

  // РЕАЛЬНАЯ НАВИГАЦИЯ с cdep.ru
  const navLinks = [
    { name: 'О СУДЕБНОМ ДЕПАРТАМЕНТЕ', href: '#about' },
    { name: 'ОРГАНИЗАЦИЯ ДЕЯТЕЛЬНОСТИ', href: '#organization' },
    { name: 'НАПРАВЛЕНИЯ ДЕЯТЕЛЬНОСТИ', href: '#activities' },
    { name: 'ГОСУДАРСТВЕННАЯ СЛУЖБА', href: '#service' },
    { name: 'ПРОТИВОДЕЙСТВИЕ КОРРУПЦИИ', href: '#anticorruption' },
    { name: 'ОБРАЩЕНИЯ ГРАЖДАН', href: '#appeals' },
    { name: 'ОТКРЫТЫЕ ДАННЫЕ', href: '#opendata' },
    { name: 'ПРЕСС-СЛУЖБА', href: '#press' },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100">
      {/* Top Bar */}
      <div className="bg-[#1a365d] text-white text-sm py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <span className="text-amber-400 font-semibold">07.04.2026</span>
            <span className="hidden sm:inline text-slate-300">|</span>
            <span className="hidden sm:inline text-slate-300">Официальный портал</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-amber-400 transition-colors">ENG</a>
            <a href="#" className="hover:text-amber-400 transition-colors">Версия для слабовидящих</a>
          </div>
        </div>
      </div>

      {/* Header */}
      <header className={`sticky top-0 z-50 transition-all duration-500 ${scrolled ? 'bg-white/95 backdrop-blur-xl shadow-lg' : 'bg-white'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            {/* Logo */}
            <a href="/" className="flex items-center space-x-4 group">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-700 to-blue-900 flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow">
                <Scale className="w-8 h-8 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="font-bold text-slate-800 leading-tight">СУДЕБНЫЙ ДЕПАРТАМЕНТ</h1>
                <p className="text-xs text-slate-500">при Верховном Суде Российской Федерации</p>
              </div>
            </a>

            {/* Mobile Menu Button */}
            <button className="lg:hidden p-2 rounded-lg hover:bg-slate-100" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Navigation */}
        <nav className={`border-t border-slate-200 ${isMenuOpen ? 'block' : 'hidden'} lg:block`}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col lg:flex-row lg:items-center py-2 lg:py-0 overflow-x-auto">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="px-4 py-3 lg:py-4 text-sm font-medium text-slate-700 hover:text-blue-700 hover:bg-blue-50 whitespace-nowrap transition-colors"
                >
                  {link.name}
                </a>
              ))}
            </div>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 lg:py-28 overflow-hidden">
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
            
            <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-800 mb-6 leading-tight">
              Судебный департамент
              <span className="block text-2xl sm:text-3xl lg:text-4xl mt-2 text-slate-600">
                при Верховном Суде Российской Федерации
              </span>
            </h2>
            
            <p className="text-lg sm:text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
              Организационное обеспечение деятельности судов общей юрисдикции 
              и арбитражных судов Российской Федерации
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="#ejustice" className="group px-8 py-4 bg-gradient-to-r from-blue-700 to-blue-800 text-white rounded-xl font-semibold text-lg hover:shadow-xl hover:shadow-blue-500/30 hover:scale-105 transition-all flex items-center justify-center gap-2">
                Электронное правосудие
                <ArrowUpRight className="w-5 h-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
              </a>
              <a href="#appeals" className="px-8 py-4 bg-white text-slate-700 border-2 border-slate-300 rounded-xl font-semibold text-lg hover:bg-slate-50 hover:border-slate-400 transition-all">
                Обращения граждан
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { value: 3200, suffix: '+', label: 'Судов в системе РФ', icon: Building2 },
              { value: 25000, suffix: '+', label: 'Судей', icon: Gavel },
              { value: 15000000, suffix: '+', label: 'Дел в год', icon: FileText },
              { value: 85, suffix: '', label: 'Субъектов РФ', icon: MapPin },
            ].map((stat, idx) => (
              <GlassCard key={idx} className="text-center p-8" hover={true}>
                <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                  <stat.icon className="w-6 h-6 text-blue-700" />
                </div>
                <div className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent mb-2">
                  <CountUp end={stat.value} suffix={stat.suffix} />
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
              Современные цифровые сервисы для участников судебного процесса в Российской Федерации
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <ServiceCard
              icon={FileText}
              title="Подача документов"
              description="Подайте исковое заявление или жалобу онлайн через ГАС «Правосудие» без посещения суда"
              href="https://sudrf.ru"
            />
            <ServiceCard
              icon={Search}
              title="Картотека дел"
              description="Найдите информацию о судебном деле по номеру или участнику процесса"
              href="https://sudrf.ru/index.php?id=300"
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
              icon={Calendar}
              title="Расписание слушаний"
              description="Узнайте дату и время судебного заседания в режиме онлайн"
            />
            <ServiceCard
              icon={BookOpen}
              title="Образцы документов"
              description="Скачайте шаблоны исковых заявлений и других процессуальных документов"
            />
          </div>
        </div>
      </section>

      {/* News Section */}
      <section id="press" className="py-20 bg-gradient-to-b from-transparent to-slate-100/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-12">
            <div>
              <h3 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-4">
                Новости
              </h3>
              <p className="text-slate-600">
                Актуальная информация о деятельности Судебного департамента при Верховном Суде Российской Федерации
              </p>
            </div>
            <a href="#" className="mt-4 sm:mt-0 inline-flex items-center text-blue-700 font-medium hover:text-blue-800 group">
              Все новости <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {news.map((item, idx) => (
              <NewsCard key={idx} date={item.date} title={item.title} />
            ))}
          </div>
        </div>
      </section>

      {/* Important Links */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-8 text-center">
            Важные ссылки
          </h3>
          <p className="text-slate-600 text-center mb-12 max-w-2xl mx-auto">
            Организации судебной системы Российской Федерации
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ExternalLinkCard 
              title="Верховный Суд Российской Федерации"
              href="http://www.vsrf.ru/"
              description="Высший судебный орган РФ"
            />
            <ExternalLinkCard 
              title="Совет судей Российской Федерации"
              href="http://www.ssrf.ru/"
              description="Объединение судей РФ"
            />
            <ExternalLinkCard 
              title="Высшая квалификационная коллегия судей"
              href="http://www.vkks.ru/"
              description="Квалификационные требования к судьям"
            />
            <ExternalLinkCard 
              title="Интернет-портал ГАС «Правосудие»"
              href="https://sudrf.ru/"
              description="Государственная автоматизированная система"
            />
            <ExternalLinkCard 
              title="Федеральные суды общей юрисдикции"
              href="https://sudrf.ru/index.php?id=300"
              description="Суды по гражданским и уголовным делам"
            />
            <ExternalLinkCard 
              title="Федеральные арбитражные суды"
              href="https://www.arbitr.ru/"
              description="Суды по экономическим спорам"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="appeals" className="py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <GlassCard className="p-8 sm:p-12 text-center bg-gradient-to-br from-blue-700 to-blue-900 text-white" hover={false}>
            <h3 className="text-3xl sm:text-4xl font-bold mb-4">
              Обращения граждан
            </h3>
            <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto">
              Вы можете обратиться в Судебный департамент при Верховном Суде Российской Федерации 
              по вопросам организации деятельности судов
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="mailto:info@cdep.ru" className="px-8 py-4 bg-white text-blue-700 rounded-xl font-semibold hover:shadow-xl hover:scale-105 transition-all">
                Написать обращение
              </a>
              <a href="#" className="px-8 py-4 bg-blue-800 text-white border border-blue-600 rounded-xl font-semibold hover:bg-blue-700 transition-all">
                Порядок обращения
              </a>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#0f172a] text-white pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
            {/* Brand */}
            <div>
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-amber-500 flex items-center justify-center">
                  <Scale className="w-7 h-7 text-slate-900" />
                </div>
                <div>
                  <h4 className="font-bold text-lg leading-tight">Судебный департамент</h4>
                  <p className="text-slate-400 text-sm">при Верховном Суде РФ</p>
                </div>
              </div>
              <p className="text-slate-400 text-sm leading-relaxed">
                Организационное обеспечение деятельности судов общей 
                юрисдикции и арбитражных судов Российской Федерации
              </p>
            </div>

            {/* Navigation */}
            <div>
              <h5 className="font-semibold mb-6 text-lg">Разделы</h5>
              <ul className="space-y-3 text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">О Судебном департаменте</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Организация деятельности</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Направления деятельности</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Государственная служба</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Противодействие коррупции</a></li>
              </ul>
            </div>

            {/* Services */}
            <div>
              <h5 className="font-semibold mb-6 text-lg">Сервисы</h5>
              <ul className="space-y-3 text-slate-400">
                <li><a href="#" className="hover:text-white transition-colors">Электронное правосудие</a></li>
                <li><a href="#" className="hover:text-white transition-colors">ГАС «Правосудие»</a></li>
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
                  <span>121260, г. Москва, ул. Новый Арбат, д. 16</span>
                </li>
                <li className="flex items-center gap-3">
                  <Phone className="w-5 h-5 text-amber-400 shrink-0" />
                  <span>+7 (495) 606-16-16</span>
                </li>
                <li className="flex items-center gap-3">
                  <Mail className="w-5 h-5 text-amber-400 shrink-0" />
                  <a href="mailto:info@cdep.ru" className="hover:text-white transition-colors">info@cdep.ru</a>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-800 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-slate-500 text-sm">
              2009-2026 © Судебный департамент при Верховном Суде Российской Федерации
            </p>
            <div className="flex gap-6 text-slate-500 text-sm">
              <a href="#" className="hover:text-white transition-colors">Карта сайта</a>
              <a href="#" className="hover:text-white transition-colors">Техподдержка</a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
