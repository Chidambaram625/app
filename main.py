# main.py - Desktop version (no Android dependencies needed)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import datetime

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_messages = []
        self.is_sleeping = False
        self.sleep_clock_event = None
    
    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Title
        title = Label(
            text='Advanced Kivy App with Sleep Mode', 
            font_size=18,
            size_hint=(1, 0.1),
            color=(0.2, 0.6, 1, 1)
        )
        
        # Widgets
        self.status_label = Label(
            text='Ready! Enter your name below.', 
            font_size=16,
            size_hint=(1, 0.15),
            color=(0.1, 0.8, 0.1, 1)
        )
        
        self.text_input = TextInput(
            hint_text='Type your name here...',
            size_hint=(1, 0.15),
            font_size=14
        )
        
        # Buttons layout
        button_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint=(1, 0.15))
        
        submit_button = Button(
            text='Submit',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        
        self.sleep_button = Button(
            text='Sleep Mode',
            background_color=(0.8, 0.6, 0.2, 1)
        )
        
        # Bind events
        submit_button.bind(on_press=self.on_submit_click)
        self.sleep_button.bind(on_press=self.on_sleep_click)
        
        button_layout.add_widget(submit_button)
        button_layout.add_widget(self.sleep_button)
        
        # Result display
        self.result_label = Label(
            text='Your greeting will appear here...', 
            font_size=16,
            size_hint=(1, 0.15),
            color=(0.9, 0.3, 0.3, 1)
        )
        
        # Log section title
        log_title = Label(
            text='Application Logs:', 
            font_size=14,
            size_hint=(1, 0.05),
            color=(0.5, 0.5, 0.5, 1)
        )
        
        # Log display area with scroll
        self.log_layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 0.3))
        scroll.add_widget(self.log_layout)
        
        self.log_message("App started successfully")
        
        # Add all widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.result_label)
        main_layout.add_widget(log_title)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def on_submit_click(self, instance):
        try:
            name = self.text_input.text.strip()
            if name:
                greeting = f"Hello {name}! Nice to meet you!"
                self.result_label.text = greeting
                self.result_label.color = (0.2, 0.7, 0.2, 1)
                self.status_label.text = "Success! Greeting generated."
                self.status_label.color = (0.1, 0.8, 0.1, 1)
                self.log_message(f"Greeting generated for: {name}")
            else:
                raise ValueError("Empty name provided")
        except Exception as e:
            error_msg = f"Error: Please enter a valid name!"
            self.result_label.text = error_msg
            self.result_label.color = (0.9, 0.2, 0.2, 1)
            self.status_label.text = "Input Error!"
            self.status_label.color = (0.9, 0.1, 0.1, 1)
            self.log_message(f"Submission error: {str(e)}")
    
    def on_sleep_click(self, instance):
        if not self.is_sleeping:
            self.enter_sleep_mode()
        else:
            self.wake_up()
    
    def enter_sleep_mode(self):
        try:
            self.is_sleeping = True
            self.sleep_button.text = "Wake Up"
            self.sleep_button.background_color = (0.2, 0.8, 0.2, 1)
            
            # Hide main UI elements
            self.status_label.text = "💤 SLEEP MODE ACTIVE 💤"
            self.status_label.color = (0.5, 0.5, 0.8, 1)
            self.result_label.text = "App is in sleep mode. Press Wake Up button to wake up."
            self.result_label.color = (0.5, 0.5, 0.5, 1)
            
            # Disable input
            self.text_input.disabled = True
            
            self.log_message("Entered sleep mode")
            
        except Exception as e:
            self.log_message(f"Sleep mode error: {str(e)}")
    
    def wake_up(self):
        try:
            self.is_sleeping = False
            
            self.sleep_button.text = "Sleep Mode"
            self.sleep_button.background_color = (0.8, 0.6, 0.2, 1)
            
            # Restore UI
            self.status_label.text = "Awake! Ready for input."
            self.status_label.color = (0.1, 0.8, 0.1, 1)
            self.result_label.text = "App is now awake. Enter your name above."
            self.result_label.color = (0.2, 0.6, 1, 1)
            
            # Enable input
            self.text_input.disabled = False
            
            self.log_message("Woke up from sleep mode")
            
        except Exception as e:
            self.log_message(f"Wake up error: {str(e)}")
    
    def log_message(self, message):
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            
            self.log_messages.append(log_entry)
            
            # Create label for log entry
            log_label = Label(
                text=log_entry,
                font_size=11,
                text_size=(self.root.width - 30 if self.root else 300, None),
                halign='left',
                valign='middle',
                size_hint_y=None,
                height=30
            )
            log_label.bind(texture_size=log_label.setter('size'))
            
            # Add to log layout at the top
            self.log_layout.add_widget(log_label, index=0)
            
            # Keep only last 50 log entries
            if len(self.log_messages) > 50:
                self.log_messages.pop(0)
                if len(self.log_layout.children) > 50:
                    self.log_layout.remove_widget(self.log_layout.children[-1])
                    
        except Exception as e:
            print(f"Logging error: {str(e)}")  # Fallback print
    
    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        self.log_message("App paused")
        return True
    
    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        self.log_message("App resumed")
        return True
    
    def on_stop(self):
        """Handle app stop"""
        self.log_message("App stopped")

if __name__ == '__main__':
    MyApp().run()