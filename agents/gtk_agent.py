#!/usr/bin/env python3
"""
🐧 GTK-Agent
Linux Desktop App Specialist

Приложения для Linux на GTK и Vala/C.
"""

import argparse
from pathlib import Path
from typing import Dict


class GTKAgent:
    """
    🐧 GTK-Agent
    
    Специализация: Linux Desktop (GTK, GNOME)
    Задачи: GTK4, Libadwaita, Linux apps
    """
    
    NAME = "🐧 GTK-Agent"
    ROLE = "Linux Desktop Developer"
    EXPERTISE = ["GTK", "C", "Vala", "Linux", "GNOME"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "main.c": self._generate_main_c(),
            "window.c": self._generate_window_c(),
            "window.h": self._generate_window_h(),
            "meson.build": self._generate_meson(),
            "style.css": self._generate_css()
        }
    
    def _generate_main_c(self) -> str:
        return '''#include "window.h"
#include <gtk/gtk.h>

static void
on_activate (GtkApplication *app)
{
    GtkWidget *window = my_application_window_new (app);
    gtk_window_present (GTK_WINDOW (window));
}

int
main (int argc, char **argv)
{
    g_autoptr(GtkApplication) app = NULL;
    int status;

    app = gtk_application_new ("com.example.MyApp", G_APPLICATION_FLAGS_NONE);
    g_signal_connect (app, "activate", G_CALLBACK (on_activate), NULL);
    
    status = g_application_run (G_APPLICATION (app), argc, argv);
    
    return status;
}
'''
    
    def _generate_window_c(self) -> str:
        return '''#include "window.h"

struct _MyApplicationWindow
{
    GtkApplicationWindow parent_instance;
    
    GtkWidget *header_bar;
    GtkWidget *search_entry;
    GtkWidget *list_box;
    GtkWidget *status_label;
};

G_DEFINE_TYPE (MyApplicationWindow, my_application_window, GTK_TYPE_APPLICATION_WINDOW)

static void
on_search_changed (GtkSearchEntry *entry, MyApplicationWindow *self)
{
    const char *text = gtk_editable_get_text (GTK_EDITABLE (entry));
    gtk_label_set_text (GTK_LABEL (self->status_label), text);
}

static void
my_application_window_init (MyApplicationWindow *self)
{
    gtk_widget_init_template (GTK_WIDGET (self));
    
    g_signal_connect (self->search_entry, "search-changed",
                      G_CALLBACK (on_search_changed), self);
}

static void
my_application_window_dispose (GObject *object)
{
    MyApplicationWindow *self = MY_APPLICATION_WINDOW (object);
    
    gtk_widget_dispose_template (GTK_WIDGET (self), MY_TYPE_APPLICATION_WINDOW);
    
    G_OBJECT_CLASS (my_application_window_parent_class)->dispose (object);
}

static void
my_application_window_class_init (MyApplicationWindowClass *klass)
{
    GObjectClass *object_class = G_OBJECT_CLASS (klass);
    GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);
    
    object_class->dispose = my_application_window_dispose;
    
    gtk_widget_class_set_template_from_resource (widget_class, "/com/example/MyApp/window.ui");
    gtk_widget_class_bind_template_child (widget_class, MyApplicationWindow, header_bar);
    gtk_widget_class_bind_template_child (widget_class, MyApplicationWindow, search_entry);
    gtk_widget_class_bind_template_child (widget_class, MyApplicationWindow, list_box);
    gtk_widget_class_bind_template_child (widget_class, MyApplicationWindow, status_label);
}

MyApplicationWindow *
my_application_window_new (GtkApplication *app)
{
    return g_object_new (MY_TYPE_APPLICATION_WINDOW,
                         "application", app,
                         NULL);
}
'''
    
    def _generate_window_h(self) -> str:
        return '''#pragma once

#include <gtk/gtk.h>

G_BEGIN_DECLS

#define MY_TYPE_APPLICATION_WINDOW (my_application_window_get_type())

G_DECLARE_FINAL_TYPE (MyApplicationWindow, my_application_window, 
                      MY, APPLICATION_WINDOW, GtkApplicationWindow)

MyApplicationWindow *my_application_window_new (GtkApplication *app);

G_END_DECLS
'''
    
    def _generate_meson(self) -> str:
        return '''project('myapp', 'c',
  version : '0.1.0',
  meson_version: '>=0.59.0',
  default_options : ['warning_level=2',
                     'werror=false',
                     'c_std=gnu11'])

# Dependencies
gtk_dep = dependency('gtk4', version: '>=4.6.0')
adwaita_dep = dependency('libadwaita-1', version: '>=1.2.0')

deps = [gtk_dep, adwaita_dep]

# Include directories
inc = include_directories('.')

# Sources
sources = files(
  'main.c',
  'window.c',
)

# Resources
resources = gnome.compile_resources('resources',
  'resources.gresource.xml',
  c_name: 'my_app'
)

# Executable
executable('myapp',
  sources + resources,
  dependencies: deps,
  include_directories: inc,
  install: true,
)

# Desktop file
install_data('com.example.MyApp.desktop',
  install_dir: get_option('datadir') / 'applications'
)

# App icon
install_data('com.example.MyApp.svg',
  install_dir: get_option('datadir') / 'icons' / 'hicolor' / 'scalable' / 'apps'
)
'''
    
    def _generate_css(self) -> str:
        return '''/* GTK4 Styles */

window {
    background-color: @window_bg_color;
}

headerbar {
    background-color: @headerbar_bg_color;
    color: @headerbar_fg_color;
}

.search-entry {
    border-radius: 999px;
    padding: 8px 16px;
}

.list-row {
    padding: 12px;
    border-radius: 8px;
    margin: 4px 8px;
}

.list-row:hover {
    background-color: alpha(@accent_color, 0.1);
}

.list-row:selected {
    background-color: @accent_color;
    color: @accent_fg_color;
}

.button-primary {
    background-color: @accent_color;
    color: @accent_fg_color;
    padding: 8px 16px;
    border-radius: 8px;
}

.status-label {
    font-size: 0.9em;
    color: @dim_label_color;
}
'''


def main():
    parser = argparse.ArgumentParser(description="🐧 GTK-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = GTKAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🐧 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
