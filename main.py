import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
from threading import Thread

from xuly import fetch_data, SaveFile

resultLinks = []

def check_link(string):
    if string == "":
        return False
    if string.startswith("https://fb.watch") or string.startswith("https://www.facebook.com/watch") or string.startswith("https://www.facebook.com/reel"):
        return True
    return False

def get_video_info():
    url = url_entry.get()  # Lấy nội dung từ ô nhập liệu
    if check_link(url) == False:
        process_label.grid_remove()
        messagebox.showinfo("", "Vui lòng điền đúng định dạng")
        return

    result = fetch_data(url)
    if result == False:
        process_label.grid_remove()
        messagebox.showinfo("", "URL không hợp lệ hoặc không tồn tại")
        return

    resultLinks.clear()

    for link in result:
        resultLinks.append(link)
    displayThumbnail()
    process_label.grid_remove()

def enterHandle():
    process_label.grid(row=0, column=0, padx=10, pady=5)
    root.update()
    get_video_info()

def on_enter_pressed(event):
    process_label.grid(row=0, column=0, padx=10, pady=5)
    root.update()
    get_video_info()

def SaveVideoAsSD():
    if len(resultLinks) == 0:
        return
    process_label.grid(row=0, column=0, padx=10, pady=5)
    root.update()
    SaveFile(resultLinks[0], process_label)

def SaveVideoAsHD():
    if len(resultLinks) == 0:
        return
    process_label.grid(row=0, column=0, padx=10, pady=5)
    root.update()
    SaveFile(resultLinks[1], process_label)

def displayThumbnail():
    new_url = resultLinks[2]
    response = requests.get(new_url)
    image_data = response.content
    thumbnail_image = Image.open(BytesIO(image_data))
    thumbnail_image.thumbnail((130, 130))
    thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
    thumbnail_display.configure(image=thumbnail_photo)
    thumbnail_display.image = thumbnail_photo
    thumbnail_display.grid(row=1, column=0, padx=10, pady=10)


root = tk.Tk()
root.title("Facebook Video Downloader")

window_width = 800
window_height = 500
root.geometry(f"{window_width}x{window_height}")

# Frame for URL input
url_frame = tk.Frame(root)
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="Enter Facebook Video URL:", font=30)
url_label.pack(side=tk.LEFT)

url_entry = tk.Entry(url_frame, width=40, font=50)
url_entry.pack(side=tk.LEFT)

# Button for Enter key
url_entry.bind("<Return>", on_enter_pressed)

enter_button = tk.Button(url_frame, text="Enter", font=18, command=enterHandle, width=8, height=1, bg="#28B76B", fg="white")
enter_button.pack(side=tk.LEFT, padx=10)

# Frame for video info display
info_frame = tk.Frame(root)
info_frame.pack(pady=10)

process_label = tk.Label(info_frame, text="Đang xử lý...")
# process_label.grid_remove()

# # Tải ảnh từ URL
# image_url = "https://scontent-ams2-1.xx.fbcdn.net/v/t15.5256-10/435515795_1764476014042265_3338390410188886237_n.jpg?stp=dst-jpg_p526x296&_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=thVWHpzra6QAb6yLnNl&_nc_ht=scontent-ams2-1.xx&edm=AGo2L-IEAAAA&oh=00_AfAAPpqfuFclIOzw4BHWH-DWa8m5hnbYaCWfGRawT0pGYw&oe=6634F2BA"
# response = requests.get(image_url)
# image_data = response.content

# Mở ảnh từ dữ liệu nhận được
thumbnail_image = Image.open("Thumbnail.png")
thumbnail_image.thumbnail((150, 150))  # Resize the image

thumbnail_photo = ImageTk.PhotoImage(thumbnail_image)
thumbnail_display = tk.Label(info_frame, image=thumbnail_photo)
thumbnail_display.image = thumbnail_photo
thumbnail_display.grid(row=1, column=0, padx=10, pady=10)

# Frame for download buttons
download_frame = tk.Frame(root)
download_frame.pack(pady=10)

download_sd_button = tk.Button(download_frame, text="Download SD - 360p", font=18, command=SaveVideoAsSD, bg="#0099FF", fg="white")
download_sd_button.grid(row=0, column=0, padx=30)

download_hd_button = tk.Button(download_frame, text="Download HD - 720p", font=18, command=SaveVideoAsHD, bg="#FF6600", fg="white")
download_hd_button.grid(row=0, column=1, padx=50)

root.mainloop()
