# main.py
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class SleepApp(App):
    def build(self):
        self.sleeping = False
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.label = Label(
            text='📱 Phone is AWAKE\n\nPress button to sleep', 
            font_size=18,
            halign='center'
        )
        self.button = Button(
            text='🌙 SLEEP PHONE',
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 1, 1)
        )
        self.button.bind(on_press=self.toggle)
        
        layout.add_widget(self.label)
        layout.add_widget(self.button)
        return layout
    
    def toggle(self, instance):
        self.sleeping = not self.sleeping
        if self.sleeping:
            self.label.text = '💤 Phone is SLEEPING\n\nPress Volume buttons to wake up'
            self.button.text = '⏰ WAKE UP'
            self.button.background_color = (0.3, 0.8, 0.3, 1)
        else:
            self.label.text = '📱 Phone is AWAKE\n\nPress button to sleep'
            self.button.text = '🌙 SLEEP PHONE'
            self.button.background_color = (0.2, 0.6, 1, 1)

    # These will be called by Android when volume buttons are pressed
    def on_volume_up(self):
        if hasattr(self, 'sleeping') and self.sleeping:
            self.toggle(None)
    
    def on_volume_down(self):
        if hasattr(self, 'sleeping') and self.sleeping:
            self.toggle(None)

SleepApp().run()