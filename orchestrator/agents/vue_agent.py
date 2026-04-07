"""
⚡ Vue Agent
Создаёт Vue.js приложения с Composition API
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class VueAgentExecutor(BaseAgentExecutor):
    """
    ⚡ Vue.js Developer Agent
    
    Генерирует:
    - Vue 3 приложения с Composition API
    - Vue Router конфигурацию
    - Pinia store
    - Vue components
    """
    
    AGENT_TYPE = 'vue'
    NAME = 'Vue Agent'
    EMOJI = '⚡'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['vue', 'vuejs', 'frontend']
    
    def execute(self, task: Task) -> Dict:
        title = task.title.lower()
        
        if 'dashboard' in title:
            return self._create_dashboard(task)
        elif 'shop' in title or 'store' in title or 'магазин' in title:
            return self._create_shop(task)
        else:
            return self._create_default_app(task)
    
    def _create_dashboard(self, task: Task) -> Dict:
        app_vue = '''<template>
  <div class="dashboard">
    <aside class="sidebar">
      <div class="logo">⚡ Vue Dashboard</div>
      <nav>
        <router-link to="/" class="nav-item">📊 Overview</router-link>
        <router-link to="/users" class="nav-item">👥 Users</router-link>
        <router-link to="/settings" class="nav-item">⚙️ Settings</router-link>
      </nav>
    </aside>
    
    <main class="main-content">
      <header class="header">
        <h1>{{ $route.meta.title || 'Dashboard' }}</h1>
        <div class="user-menu">👤 Admin</div>
      </header>
      
      <div class="content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard {
  display: flex;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.sidebar {
  width: 260px;
  background: #1a1a2e;
  color: white;
  padding: 20px 0;
}

.logo {
  padding: 0 20px 30px;
  font-size: 20px;
  font-weight: 700;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.nav-item {
  display: block;
  padding: 15px 20px;
  color: rgba(255,255,255,0.7);
  text-decoration: none;
  transition: all 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: rgba(233, 69, 96, 0.2);
  color: #e94560;
}

.main-content {
  flex: 1;
  background: #f5f7fa;
}

.header {
  background: white;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.header h1 {
  font-size: 24px;
  color: #1a1a2e;
}

.content {
  padding: 30px;
}
</style>
'''

        overview_vue = '''<template>
  <div class="overview">
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-icon">{{ stat.icon }}</div>
        <div class="stat-info">
          <h3>{{ stat.label }}</h3>
          <p class="stat-value">{{ stat.value }}</p>
        </div>
      </div>
    </div>
    
    <div class="recent-activity">
      <h2>Недавняя активность</h2>
      <ul>
        <li v-for="(item, index) in activity" :key="index">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const stats = ref([
  { icon: '👥', label: 'Пользователи', value: '1,234' },
  { icon: '💰', label: 'Доход', value: '$45,600' },
  { icon: '📦', label: 'Заказы', value: '89' },
  { icon: '📈', label: 'Рост', value: '+23%' }
])

const activity = ref([
  '🎉 Новый пользователь зарегистрировался',
  '💳 Оплата получена - $299',
  '🚀 Проект "AI App" завершён',
  '⭐ Новый отзыв 5 звёзд'
])
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  background: #f8f9fa;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info h3 {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}

.recent-activity {
  background: white;
  border-radius: 16px;
  padding: 24px;
}

.recent-activity h2 {
  font-size: 18px;
  margin-bottom: 16px;
}

.recent-activity ul {
  list-style: none;
  padding: 0;
}

.recent-activity li {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}
</style>
'''

        main_js = '''import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
'''

        router_js = '''import { createRouter, createWebHistory } from 'vue-router'
import Overview from './views/Overview.vue'

const routes = [
  {
    path: '/',
    name: 'Overview',
    component: Overview,
    meta: { title: 'Overview' }
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('./views/Users.vue'),
    meta: { title: 'Users' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('./views/Settings.vue'),
    meta: { title: 'Settings' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
'''

        package_json = '''{
  "name": "vue-dashboard",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
'''

        vite_config = '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()]
})
'''

        return {
            'success': True,
            'message': f'✅ Vue 3 Dashboard создан!',
            'artifacts': {
                'src/App.vue': app_vue,
                'src/views/Overview.vue': overview_vue,
                'src/main.js': main_js,
                'src/router.js': router_js,
                'package.json': package_json,
                'vite.config.js': vite_config
            }
        }
    
    def _create_shop(self, task: Task) -> Dict:
        """Создаёт Vue магазин"""
        
        store_js = '''import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  
  const totalItems = computed(() => 
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )
  
  const totalPrice = computed(() =>
    items.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  )
  
  function addItem(product) {
    const existing = items.value.find(i => i.id === product.id)
    if (existing) {
      existing.quantity++
    } else {
      items.value.push({ ...product, quantity: 1 })
    }
  }
  
  function removeItem(id) {
    items.value = items.value.filter(i => i.id !== id)
  }
  
  return { items, totalItems, totalPrice, addItem, removeItem }
})
'''

        return {
            'success': True,
            'message': f'✅ Vue Shop создан!',
            'artifacts': {
                'src/stores/cart.js': store_js,
                'package.json': '{"dependencies":{"vue":"^3.4","pinia":"^2.1"}}'
            }
        }
    
    def _create_default_app(self, task: Task) -> Dict:
        return {
            'success': True,
            'message': f'✅ Базовое Vue приложение создано!',
            'artifacts': {
                'src/App.vue': '<template><h1>⚡ Hello Vue 3!</h1></template>',
                'src/main.js': "import { createApp } from 'vue'; import App from './App.vue'; createApp(App).mount('#app');"
            }
        }
