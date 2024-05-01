import tkinter as tk
from tkinter import messagebox, filedialog
import re
from bs4 import BeautifulSoup
import requests
import json
from threading import Thread

def clean_str(str):
    return str.replace("\\", "").replace("u0025", "%")

def get_thumbnail(html_content):
    matches = re.findall(r'preferred_thumbnail":{"image":{"uri":"[^"]*', html_content)
    splitchuoi = matches[0].split(':"')
    return clean_str(splitchuoi[1])

def get_sd_link(html_content):
    matches = re.findall(r'browser_native_sd_url":"https:[^"]*', html_content)
    splitchuoi = matches[0].split(':"')
    return clean_str(splitchuoi[1])

def get_hd_link(html_content):
    matches = re.findall(r'browser_native_hd_url":"https:[^"]*', html_content)
    splitchuoi = matches[0].split(':"')
    return clean_str(splitchuoi[1])

def fetch_data(url):
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return False

        html_content = response.text

        thumbnail = get_thumbnail(html_content)
        sd_link = get_sd_link(html_content)
        hd_link = get_hd_link(html_content)

        return [
            sd_link,
            hd_link,
            thumbnail
        ]
    except:
        return False


def SaveFile(url, process_label):
    filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    if filename == "":            # Nếu người dùng "Cancel"
        return

    response = requests.get(url)
    if response.status_code == 200:
        OpenFileToWrite = open(filename, 'wb')
        try:
            OpenFileToWrite.write(response.content)
            process_label.grid_remove()
            messagebox.showinfo("", "Video đã được tải xuống thành công!")
        except:
            process_label.grid_remove()
            messagebox.showinfo("", "Lỗi khi lưu video")
        OpenFileToWrite.close()
    else:
        process_label.grid_remove()
        messagebox.showinfo("", "Lỗi khi lưu video")


