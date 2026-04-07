export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-[#1a365d] text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-[#d4af37] rounded-full flex items-center justify-center text-2xl">
                ⚖️
              </div>
              <div>
                <h1 className="text-xl font-bold">Судебный департамент</h1>
                <p className="text-sm text-gray-300">при Верховном суде Российской Федерации</p>
              </div>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-white hover:text-[#d4af37] transition">Главная</a>
              <a href="#about" className="text-gray-300 hover:text-white transition">О департаменте</a>
              <a href="#news" className="text-gray-300 hover:text-white transition">Новости</a>
              <a href="#documents" className="text-gray-300 hover:text-white transition">Документы</a>
              <a href="#ejustice" className="text-gray-300 hover:text-white transition">Электронное правосудие</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-b from-[#1a365d] to-[#2c5282] text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-6xl font-bold mb-6">
            Судебный департамент
          </h2>
          <p className="text-xl md:text-2xl text-gray-200 mb-8 max-w-3xl mx-auto">
            Организационное обеспечение деятельности судов общей юрисдикции и арбитражных судов Российской Федерации
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-[#d4af37] text-[#1a365d] px-8 py-4 rounded-lg font-semibold hover:bg-[#b8962f] transition">
              Электронное правосудие
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-[#1a365d] transition">
              Подача документов
            </button>
          </div>
        </div>
      </section>

      {/* Statistics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-[#1a365d]">3,200+</div>
              <div className="text-gray-600 mt-2">Судов в системе</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-[#1a365d]">25,000+</div>
              <div className="text-gray-600 mt-2">Судей</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-[#1a365d]">15M+</div>
              <div className="text-gray-600 mt-2">Дел в год</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-[#1a365d]">5M+</div>
              <div className="text-gray-600 mt-2">Пользователей ГАС</div>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="py-16 bg-gray-100" id="ejustice">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl font-bold text-[#1a365d] text-center mb-12">Электронное правосудие</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition border-t-4 border-[#d4af37]">
              <div className="text-4xl mb-4">📄</div>
              <h4 className="text-xl font-semibold text-[#1a365d] mb-2">Подача документов</h4>
              <p className="text-gray-600">Подайте исковое заявление или жалобу онлайн через ГАС «Правосудие»</p>
            </div>
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition border-t-4 border-[#d4af37]">
              <div className="text-4xl mb-4">🔍</div>
              <h4 className="text-xl font-semibold text-[#1a365d] mb-2">Проверка статуса</h4>
              <p className="text-gray-600">Отслеживайте ход рассмотрения вашего дела в режиме реального времени</p>
            </div>
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition border-t-4 border-[#d4af37]">
              <div className="text-4xl mb-4">💳</div>
              <h4 className="text-xl font-semibold text-[#1a365d] mb-2">Оплата пошлин</h4>
              <p className="text-gray-600">Оплатите государственную пошлину онлайн без посещения банка</p>
            </div>
          </div>
        </div>
      </section>

      {/* News Section */}
      <section className="py-16 bg-white" id="news">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl font-bold text-[#1a365d] mb-8">Новости</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <article className="border rounded-xl overflow-hidden hover:shadow-lg transition">
              <div className="p-6">
                <span className="text-sm text-[#d4af37] font-semibold">15 марта 2024</span>
                <h4 className="text-lg font-semibold text-[#1a365d] mt-2 mb-3">
                  Совещание по внедрению цифровых технологий в судебную систему
                </h4>
                <p className="text-gray-600 text-sm">
                  Под председательством заместителя Председателя Верховного Суда состоялось совещание...
                </p>
              </div>
            </article>
            <article className="border rounded-xl overflow-hidden hover:shadow-lg transition">
              <div className="p-6">
                <span className="text-sm text-[#d4af37] font-semibold">12 марта 2024</span>
                <h4 className="text-lg font-semibold text-[#1a365d] mt-2 mb-3">
                  Обновление ГАС «Правосудие»: новые функции для участников процесса
                </h4>
                <p className="text-gray-600 text-sm">
                  В системе появились новые возможности для подачи процессуальных документов...
                </p>
              </div>
            </article>
            <article className="border rounded-xl overflow-hidden hover:shadow-lg transition">
              <div className="p-6">
                <span className="text-sm text-[#d4af37] font-semibold">8 марта 2024</span>
                <h4 className="text-lg font-semibold text-[#1a365d] mt-2 mb-3">
                  Судебный департамент подвел итоги работы за 2023 год
                </h4>
                <p className="text-gray-600 text-sm">
                  В отчетном периоде значительно увеличилось количество электронных обращений...
                </p>
              </div>
            </article>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#1a365d] text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-[#d4af37] rounded-full flex items-center justify-center">⚖️</div>
                <span className="font-bold">Судебный департамент</span>
              </div>
              <p className="text-gray-400 text-sm">
                Организационное обеспечение деятельности судов Российской Федерации
              </p>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Разделы</h5>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">О департаменте</a></li>
                <li><a href="#" className="hover:text-white">Деятельность</a></li>
                <li><a href="#" className="hover:text-white">Документы</a></li>
                <li><a href="#" className="hover:text-white">Статистика</a></li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Сервисы</h5>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">Электронное правосудие</a></li>
                <li><a href="#" className="hover:text-white">Картотека дел</a></li>
                <li><a href="#" className="hover:text-white">Расписание слушаний</a></li>
                <li><a href="#" className="hover:text-white">Видеоконференции</a></li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Контакты</h5>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>📍 121260, Москва, ул. Новый Арбат, 16</li>
                <li>📞 +7 (495) 606-16-16</li>
                <li>✉️ info@court.gov.ru</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400 text-sm">
            <p>© 2024 Судебный департамент при Верховном суде Российской Федерации</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
