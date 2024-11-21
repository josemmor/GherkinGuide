
class AppManager:
    @staticmethod
    def clear_frame(frame):
        """Limpia todos los widgets de un frame dado."""
        for widget in frame.winfo_children():
            widget.destroy()