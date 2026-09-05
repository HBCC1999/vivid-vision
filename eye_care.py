import time
import subprocess
import json
import os

title = '20-20-20 Rule Reminder'
message = 'Time for a pause, look away from the screen onto an object 20 feet away for 20 seconds.'
time_step = 2  # 20 minutes

def get_install_dir():
    return os.path.join(os.getenv('LOCALAPPDATA'), 'VividVision')

def read_config(path="config.json"):
    """Read user config."""
    
    with open(os.path.join(get_install_dir(),path), "r") as f:
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

    if notification_intensity == "silent":
        while True:
            time.sleep(interval) # --time step
            send_toast(title, message)


    def show_notification():
        from tkinter import Tk, messagebox

        root = Tk()
        root.withdraw()

        messagebox.showerror(title, message)
        root.destroy()

    if notification_intensity == "critical":
        while True:
            time.sleep(interval)
            show_notification()

if __name__ == '__main__':
    try:
        config = read_config()
        intensity = config.get("notification_intensity", "silent")
        interval = config.get("interval", time_step)
    except Exception:
        intensity, interval = "silent", time_step

    run_with_intensity(intensity, interval)
