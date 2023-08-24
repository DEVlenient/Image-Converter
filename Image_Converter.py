import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class DragDropWidget(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self, text='選擇文件', command=self.select_file)
        self.select_button.pack(pady=20)

        self.format_var = tk.StringVar(value='.jpg')
        self.format_label = tk.Label(self, text='轉換格式：')
        self.format_label.pack()
        self.format_optionmenu = tk.OptionMenu(self, self.format_var, '.jpg', '.png', '.jpeg', '.webp')
        self.format_optionmenu.pack()

        self.browse_button = tk.Button(self, text='選擇位置', command=self.browse_save_path)
        self.browse_button.pack(pady=10)

        self.save_path_label = tk.Label(self, text='儲存路徑')
        self.save_path_label.pack()
        self.save_path_entry = tk.Entry(self)
        self.save_path_entry.pack()

        self.convert_button = tk.Button(self, text='開始轉換', command=self.convert_images)
        self.convert_button.pack(pady=10)

        self.preview_label = tk.Label(self)
        self.preview_label.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Images', '*.jpg *.jpeg *.png *.webp')])
        if file_path:
            self.file_paths = [file_path]
            self.show_preview()

    def show_preview(self):
        if not self.file_paths:
            self.preview_label.configure(image=None)
            return

        image_path = self.file_paths[0]
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo

    def browse_save_path(self):
        save_path = filedialog.askdirectory()
        if save_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, save_path)

    def convert_images(self):
        if not self.file_paths:
            messagebox.showwarning('錯誤', '請先選擇文件！')
            return

        output_format = self.format_var.get()
        output_dir = self.save_path_entry.get()

        for file_path in self.file_paths:
            if os.path.isfile(file_path):
                convert_image(file_path, output_dir, output_format)

        messagebox.showinfo('轉換完成', '圖片轉換完成！')
        self.show_preview()

def convert_image(image_path, output_dir, output_format):
    output_filename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}{output_format}")

    image = Image.open(image_path)
    image = image.convert("RGB")  # 將影像轉換成RGB模式
    image.save(output_path)

root = tk.Tk()
root.geometry("450x500")
root.title('圖片格式轉換工具')

app = DragDropWidget(root)
app.pack()

root.mainloop()
