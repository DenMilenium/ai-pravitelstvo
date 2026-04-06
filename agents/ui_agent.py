#!/usr/bin/env python3
"""
🎨 UI-Agent
Агент-дизайнер интерфейсов

Создаёт:
- UI-компоненты
- CSS стили
- Цветовые палитры
- Типографику
"""

import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class DesignSystem:
    name: str
    colors: Dict[str, str]
    typography: Dict[str, str]
    spacing: Dict[str, str]
    radius: Dict[str, str]
    shadows: Dict[str, str]


class UIAgent:
    """
    🎨 UI-Agent
    
    Специализация: Визуальный дизайн интерфейсов
    Инструменты: CSS, Tailwind, Figma-подобные системы
    """
    
    NAME = "🎨 UI-Agent"
    ROLE = "UI Дизайнер"
    EXPERTISE = ["UI Design", "CSS", "Design Systems", "Color Theory", "Typography"]
    
    def __init__(self):
        self.design_systems = {
            "modern": self._create_modern_design(),
            "glassmorphism": self._create_glass_design(),
            "neumorphism": self._create_neu_design(),
            "minimal": self._create_minimal_design(),
            "cyberpunk": self._create_cyber_design(),
        }
    
    def _create_modern_design(self) -> DesignSystem:
        return DesignSystem(
            name="Modern",
            colors={
                "primary": "#3B82F6",
                "secondary": "#8B5CF6",
                "success": "#10B981",
                "warning": "#F59E0B",
                "danger": "#EF4444",
                "background": "#0F172A",
                "surface": "#1E293B",
                "text": "#F8FAFC",
                "textMuted": "#94A3B8",
            },
            typography={
                "fontFamily": "'Inter', -apple-system, sans-serif",
                "heading": "font-weight: 700; letter-spacing: -0.025em;",
                "body": "font-weight: 400; line-height: 1.6;",
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "2xl": "48px",
            },
            radius={
                "sm": "4px",
                "md": "8px",
                "lg": "12px",
                "xl": "16px",
                "full": "9999px",
            },
            shadows={
                "sm": "0 1px 2px rgba(0,0,0,0.1)",
                "md": "0 4px 6px -1px rgba(0,0,0,0.1)",
                "lg": "0 10px 15px -3px rgba(0,0,0,0.1)",
                "glow": "0 0 20px rgba(59,130,246,0.5)",
            }
        )
    
    def _create_glass_design(self) -> DesignSystem:
        return DesignSystem(
            name="Glassmorphism",
            colors={
                "primary": "rgba(255,255,255,0.2)",
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "surface": "rgba(255,255,255,0.1)",
                "text": "#FFFFFF",
            },
            typography={"fontFamily": "'Segoe UI', sans-serif"},
            spacing={"md": "16px"},
            radius={"lg": "16px"},
            shadows={"glass": "0 8px 32px rgba(0,0,0,0.1), inset 0 0 0 1px rgba(255,255,255,0.1)"}
        )
    
    def _create_neu_design(self) -> DesignSystem:
        return DesignSystem(
            name="Neumorphism",
            colors={
                "background": "#E0E5EC",
                "text": "#4A5568",
                "primary": "#6B46C1",
            },
            typography={"fontFamily": "'Nunito', sans-serif"},
            spacing={"md": "20px"},
            radius={"lg": "20px"},
            shadows={
                "raised": "9px 9px 16px rgb(163,177,198,0.6), -9px -9px 16px rgba(255,255,255, 0.5)",
                "pressed": "inset 6px 6px 10px 0 rgba(163,177,198, 0.7), inset -6px -6px 10px 0 rgba(255,255,255, 0.8)"
            }
        )
    
    def _create_minimal_design(self) -> DesignSystem:
        return DesignSystem(
            name="Minimal",
            colors={
                "background": "#FFFFFF",
                "text": "#000000",
                "primary": "#000000",
                "border": "#E5E5E5",
            },
            typography={"fontFamily": "'Helvetica Neue', sans-serif"},
            spacing={"md": "24px"},
            radius={"md": "0px"},
            shadows={"none": "none"}
        )
    
    def _create_cyber_design(self) -> DesignSystem:
        return DesignSystem(
            name="Cyberpunk",
            colors={
                "background": "#0a0a0f",
                "primary": "#00ff41",
                "secondary": "#ff0080",
                "accent": "#00ffff",
                "text": "#e0e0e0",
            },
            typography={"fontFamily": "'Courier New', monospace"},
            spacing={"md": "16px"},
            radius={"md": "4px"},
            shadows={"neon": "0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41"}
        )
    
    def process_request(self, request: str, style: str = "modern") -> Dict[str, str]:
        """Обработка запроса на дизайн"""
        request_lower = request.lower()
        files = {}
        
        design = self.design_systems.get(style, self.design_systems["modern"])
        
        if "кнопка" in request_lower or "button" in request_lower:
            files = self._design_buttons(design)
        elif "форма" in request_lower or "form" in request_lower:
            files = self._design_form(design)
        elif "карточка" in request_lower or "card" in request_lower:
            files = self._design_card(design)
        elif "модал" in request_lower or "modal" in request_lower:
            files = self._design_modal(design)
        elif "навигация" in request_lower or "nav" in request_lower:
            files = self._design_navigation(design)
        elif "система" in request_lower or "design system" in request_lower:
            files = self._design_system(design)
        else:
            files = self._design_component(request, design)
        
        return files
    
    def _design_buttons(self, design: DesignSystem) -> Dict[str, str]:
        """Дизайн кнопок"""
        files = {}
        
        files["buttons.css"] = f"""/* 🎨 Кнопки от UI-Agent */
/* Design System: {{design.name}} */

.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  font-family: {design.typography['fontFamily']};
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: {design.radius['md']};
  cursor: pointer;
  transition: all 0.2s ease;
}}

/* Primary Button */
.btn-primary {{
  background: {design.colors['primary']};
  color: white;
  box-shadow: {design.shadows.get('md', '0 4px 6px rgba(0,0,0,0.1)')};
}}

.btn-primary:hover {{
  transform: translateY(-2px);
  box-shadow: {design.shadows.get('lg', '0 10px 15px rgba(0,0,0,0.1)')};
}}

.btn-primary:active {{
  transform: translateY(0);
}}

/* Secondary Button */
.btn-secondary {{
  background: transparent;
  color: {design.colors['primary']};
  border: 2px solid {design.colors['primary']};
}}

.btn-secondary:hover {{
  background: {design.colors['primary']};
  color: white;
}}

/* Danger Button */
.btn-danger {{
  background: {design.colors.get('danger', '#EF4444')};
  color: white;
}}

/* Ghost Button */
.btn-ghost {{
  background: transparent;
  color: {design.colors.get('textMuted', '#94A3B8')};
}}

.btn-ghost:hover {{
  background: rgba(255,255,255,0.1);
  color: {design.colors.get('text', '#F8FAFC')};
}}

/* Sizes */
.btn-sm {{ padding: 8px 16px; font-size: 12px; }}
.btn-lg {{ padding: 16px 32px; font-size: 16px; }}

/* With Icon */
.btn-icon svg {{
  width: 18px;
  height: 18px;
}}

/* Disabled */
.btn:disabled {{
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}}
"""
        return files
    
    def _design_form(self, design: DesignSystem) -> Dict[str, str]:
        """Дизайн форм"""
        files = {}
        
        files["forms.css"] = f"""/* 🎨 Формы от UI-Agent */

.form-group {{
  margin-bottom: {design.spacing.get('lg', '24px')};
}}

.form-label {{
  display: block;
  margin-bottom: {design.spacing.get('sm', '8px')};
  font-family: {design.typography['fontFamily']};
  font-size: 14px;
  font-weight: 500;
  color: {design.colors.get('text', '#F8FAFC')};
}}

.form-input {{
  width: 100%;
  padding: 12px 16px;
  font-family: {design.typography['fontFamily']};
  font-size: 14px;
  color: {design.colors.get('text', '#F8FAFC')};
  background: {design.colors.get('surface', '#1E293B')};
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: {design.radius.get('md', '8px')};
  transition: all 0.2s ease;
}}

.form-input:focus {{
  outline: none;
  border-color: {design.colors['primary']};
  box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}}

.form-input::placeholder {{
  color: {design.colors.get('textMuted', '#94A3B8')};
}}

.form-input.error {{
  border-color: {design.colors.get('danger', '#EF4444')};
}}

.form-error {{
  margin-top: {design.spacing.get('xs', '4px')};
  font-size: 12px;
  color: {design.colors.get('danger', '#EF4444')};
}}

/* Textarea */
textarea.form-input {{
  min-height: 120px;
  resize: vertical;
}}

/* Select */
select.form-input {{
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px;
}}

/* Checkbox & Radio */
.form-check {{
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}}

.form-check input {{
  width: 18px;
  height: 18px;
  accent-color: {design.colors['primary']};
}}
"""
        return files
    
    def _design_card(self, design: DesignSystem) -> Dict[str, str]:
        """Дизайн карточек"""
        files = {}
        
        files["cards.css"] = f"""/* 🎨 Карточки от UI-Agent */

.card {{
  background: {design.colors.get('surface', '#1E293B')};
  border-radius: {design.radius.get('lg', '12px')};
  padding: {design.spacing.get('lg', '24px')};
  box-shadow: {design.shadows.get('md', '0 4px 6px rgba(0,0,0,0.1)')};
  transition: all 0.3s ease;
}}

.card:hover {{
  transform: translateY(-4px);
  box-shadow: {design.shadows.get('lg', '0 10px 15px rgba(0,0,0,0.1)')};
}}

.card-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: {design.spacing.get('md', '16px')};
}}

.card-title {{
  font-family: {design.typography['fontFamily']};
  font-size: 18px;
  font-weight: 600;
  color: {design.colors.get('text', '#F8FAFC')};
  margin: 0;
}}

.card-subtitle {{
  font-size: 14px;
  color: {design.colors.get('textMuted', '#94A3B8')};
  margin-top: 4px;
}}

.card-body {{
  color: {design.colors.get('textMuted', '#94A3B8')};
  line-height: 1.6;
}}

.card-footer {{
  display: flex;
  align-items: center;
  gap: {design.spacing.get('sm', '8px')};
  margin-top: {design.spacing.get('lg', '24px')};
  padding-top: {design.spacing.get('md', '16px')};
  border-top: 1px solid rgba(255,255,255,0.1);
}}

/* Card Variants */
.card-border {{
  border: 1px solid rgba(255,255,255,0.1);
}}

.card-gradient {{
  background: linear-gradient(135deg, {design.colors.get('surface', '#1E293B')} 0%, rgba(59,130,246,0.1) 100%);
}}
"""
        return files
    
    def _design_system(self, design: DesignSystem) -> Dict[str, str]:
        """Полная дизайн-система"""
        files = {}
        
        files["design-system.css"] = f"""/* 🎨 Design System: {design.name} */
/* Создано UI-Agent */

:root {{
  /* Colors */
  --color-primary: {design.colors['primary']};
  --color-secondary: {design.colors.get('secondary', design.colors['primary'])};
  --color-success: {design.colors.get('success', '#10B981')};
  --color-warning: {design.colors.get('warning', '#F59E0B')};
  --color-danger: {design.colors.get('danger', '#EF4444')};
  --color-background: {design.colors.get('background', '#0F172A')};
  --color-surface: {design.colors.get('surface', '#1E293B')};
  --color-text: {design.colors.get('text', '#F8FAFC')};
  --color-text-muted: {design.colors.get('textMuted', '#94A3B8')};
  
  /* Typography */
  --font-family: {design.typography['fontFamily']};
  
  /* Spacing */
  --space-xs: {design.spacing.get('xs', '4px')};
  --space-sm: {design.spacing.get('sm', '8px')};
  --space-md: {design.spacing.get('md', '16px')};
  --space-lg: {design.spacing.get('lg', '24px')};
  --space-xl: {design.spacing.get('xl', '32px')};
  
  /* Radius */
  --radius-sm: {design.radius.get('sm', '4px')};
  --radius-md: {design.radius.get('md', '8px')};
  --radius-lg: {design.radius.get('lg', '12px')};
  
  /* Shadows */
  --shadow-sm: {design.shadows.get('sm', '0 1px 2px rgba(0,0,0,0.1)')};
  --shadow-md: {design.shadows.get('md', '0 4px 6px rgba(0,0,0,0.1)')};
  --shadow-lg: {design.shadows.get('lg', '0 10px 15px rgba(0,0,0,0.1)')};
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: var(--font-family);
  background: var(--color-background);
  color: var(--color-text);
  line-height: 1.6;
}}
"""
        
        files.update(self._design_buttons(design))
        files.update(self._design_form(design))
        files.update(self._design_card(design))
        
        return files
    
    def _design_component(self, request: str, design: DesignSystem) -> Dict[str, str]:
        """Произвольный компонент"""
        files = {}
        files[f"component.css"] = f"""/* 🎨 Компонент: {{request}} */
/* Design System: {design.name} */

.component {{
  background: {design.colors.get('surface', '#1E293B')};
  padding: {design.spacing.get('md', '16px')};
  border-radius: {design.radius.get('md', '8px')};
}}
"""
        return files


def main():
    parser = argparse.ArgumentParser(description="🎨 UI-Agent — Дизайнер интерфейсов")
    parser.add_argument("request", nargs="?", help="Описание дизайна")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    parser.add_argument("--style", "-s", default="modern",
                       choices=["modern", "glassmorphism", "neumorphism", "minimal", "cyberpunk"],
                       help="Стиль дизайна")
    
    args = parser.parse_args()
    
    agent = UIAgent()
    
    if args.request:
        print(f"🎨 {agent.NAME} создаёт: {args.request}")
        print(f"Стиль: {args.style}")
        print("-" * 50)
        
        files = agent.process_request(args.request, args.style)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename, content in files.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding="utf-8")
                print(f"✅ {filename}")
            
            print(f"\n📁 Сохранено в: {output_dir}")
        else:
            for filename, content in files.items():
                print(f"\n{'='*50}")
                print(f"📄 {filename}")
                print('='*50)
                print(content[:1000] + "..." if len(content) > 1000 else content)
    else:
        print(f"🎨 {agent.NAME}")
        print(f"Роль: {agent.ROLE}")
        print(f"Экспертиза: {', '.join(agent.EXPERTISE)}")
        print("\nПримеры:")
        print('  python ui_agent.py "Кнопки" -s modern')
        print('  python ui_agent.py "Форма входа" -s glassmorphism')
        print('  python ui_agent.py "Design System" -o design-system')


if __name__ == "__main__":
    main()
