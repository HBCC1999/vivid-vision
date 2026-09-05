import time
import subprocess
import json

title = '20-20-20 Rule Reminder'
message = 'Time for a pause, look away from the screen onto an object 20 feet away for 20 seconds.'
time_step = 20*60  # 20 minutes

def read_config(path="config.json"):
    """Read user config."""
    with open(path, "r") as f:
        config = json.load(f)

    return config

def run_with_intensity(notification_intensity="silent", interval=time_step): # "silent" or "critical"
    def send_toast(title, message):
        ps_script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $textNodes = $template.GetElementsByTagName("text")
        $textNodes.Item(0).AppendChild($template.CreateTextNode("{title}")) | Out-Null
        $textNodes.Item(1).AppendChild($template.CreateTextNode("{message}")) | Out-Null
        $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("HBCC1999")
        $notification = [Windows.UI.Notifications.ToastNotification]::new($template)
        $notifier.Show($notification)
        '''

        subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", ps_script], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
    def run_silent():
        while True:
            time.sleep(interval) # --time step
            send_toast(title, message)
    run_silent() if notification_intensity == "silent" else None

    from tkinter import Tk, messagebox

    root = Tk()
    root.withdraw()  # Hide the main window

    def show_notification():
        messagebox.showerror(title, message)

    def run_critical():
        while True:
            time.sleep(interval)
            show_notification()

    run_critical() if notification_intensity == "critical" else None

if __name__ == '__main__':
    config = read_config()
    intensity = config.get("notification_intensity")
    interval = config.get("interval")
    run_with_intensity(intensity, interval) 
