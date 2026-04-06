#!/usr/bin/env python3
"""
🪟 WPF-Agent
Windows Presentation Foundation Specialist

Десктопные приложения для Windows на C# и XAML.
"""

import argparse
from pathlib import Path
from typing import Dict


class WPFAgent:
    """
    🪟 WPF-Agent
    
    Специализация: Windows Desktop (C#, XAML)
    Задачи: Modern Windows apps, MVVM, Data binding
    """
    
    NAME = "🪟 WPF-Agent"
    ROLE = "WPF Desktop Developer"
    EXPERTISE = ["C#", "WPF", "XAML", "MVVM", ".NET"]
    
    def process_request(self, request: str) -> Dict[str, str]:
        return {
            "App.xaml": self._generate_app_xaml(),
            "MainWindow.xaml": self._generate_main_window(),
            "MainWindow.xaml.cs": self._generate_main_window_cs(),
            "ViewModel.cs": self._generate_viewmodel(),
            "Project.csproj": self._generate_csproj()
        }
    
    def _generate_app_xaml(self) -> str:
        return '''<Application x:Class="MyWPFApp.App"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             StartupUri="MainWindow.xaml">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <ResourceDictionary Source="Styles/Colors.xaml"/>
                <ResourceDictionary Source="Styles/Controls.xaml"/>
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Application.Resources>
</Application>
'''
    
    def _generate_main_window(self) -> str:
        return '''<Window x:Class="MyWPFApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d"
        Title="My WPF Application" Height="600" Width="900"
        WindowStartupLocation="CenterScreen">
    
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        
        <!-- Header -->
        <Border Grid.Row="0" Background="#007ACC" Padding="20,15">
            <TextBlock Text="{Binding Title}" 
                     Foreground="White" 
                     FontSize="24" 
                     FontWeight="Bold"/>
        </Border>
        
        <!-- Content -->
        <Grid Grid.Row="1" Margin="20">
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="250"/>
                <ColumnDefinition Width="*"/>
            </Grid.ColumnDefinitions>
            
            <!-- Sidebar -->
            <StackPanel Grid.Column="0" Margin="0,0,20,0">
                <Button Content="Dashboard" 
                        Command="{Binding NavigateCommand}"
                        CommandParameter="Dashboard"
                        Margin="0,5"
                        Padding="15,10"/>
                
                <Button Content="Settings" 
                        Command="{Binding NavigateCommand}"
                        CommandParameter="Settings"
                        Margin="0,5"
                        Padding="15,10"/>
            </StackPanel>
            
            <!-- Main Content -->
            <ContentControl Grid.Column="1" 
                           Content="{Binding CurrentView}"/>
        </Grid>
        
        <!-- Status Bar -->
        <StatusBar Grid.Row="2">
            <StatusBarItem>
                <TextBlock Text="{Binding StatusMessage}"/>
            </StatusBarItem>
            <StatusBarItem HorizontalAlignment="Right">
                <TextBlock Text="{Binding CurrentTime}"/>
            </StatusBarItem>
        </StatusBar>
    </Grid>
</Window>
'''
    
    def _generate_main_window_cs(self) -> str:
        return '''using System.Windows;

namespace MyWPFApp
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new MainViewModel();
        }
    }
}
'''
    
    def _generate_viewmodel(self) -> str:
        return '''using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

namespace MyWPFApp
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private string _title = "My WPF Application";
        private string _statusMessage = "Ready";
        private object _currentView;

        public string Title
        {
            get => _title;
            set { _title = value; OnPropertyChanged(); }
        }

        public string StatusMessage
        {
            get => _statusMessage;
            set { _statusMessage = value; OnPropertyChanged(); }
        }

        public object CurrentView
        {
            get => _currentView;
            set { _currentView = value; OnPropertyChanged(); }
        }

        public string CurrentTime => DateTime.Now.ToString("HH:mm:ss");

        public ICommand NavigateCommand { get; }

        public MainViewModel()
        {
            NavigateCommand = new RelayCommand(Navigate);
        }

        private void Navigate(object parameter)
        {
            StatusMessage = $"Navigating to {parameter}...";
            // Navigation logic here
        }

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class RelayCommand : ICommand
    {
        private readonly Action<object> _execute;
        private readonly Predicate<object> _canExecute;

        public RelayCommand(Action<object> execute, Predicate<object> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public bool CanExecute(object parameter) => _canExecute?.Invoke(parameter) ?? true;

        public void Execute(object parameter) => _execute(parameter);

        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }
    }
}
'''
    
    def _generate_csproj(self) -> str:
        return '''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net8.0-windows</TargetFramework>
    <UseWPF>true</UseWPF>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="CommunityToolkit.Mvvm" Version="8.2.2" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
  </ItemGroup>

</Project>
'''


def main():
    parser = argparse.ArgumentParser(description="🪟 WPF-Agent")
    parser.add_argument("--output", "-o", help="Папка для сохранения")
    args = parser.parse_args()
    
    agent = WPFAgent()
    files = agent.process_request("setup")
    
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            (output_dir / filename).write_text(content, encoding="utf-8")
            print(f"✅ {filename}")
    else:
        print(f"🪟 {agent.NAME}")
        for filename in files.keys():
            print(f"  📄 {filename}")


if __name__ == "__main__":
    main()
