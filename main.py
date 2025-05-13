from tkinter import filedialog

import ttkbootstrap as ttb
from PIL import Image, ImageDraw, ImageFont

image_filetypes = [
    ("All Supported Images", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
    ("PNG", "*.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("BMP", "*.bmp"),
    ("GIF", "*.gif"),
    ("TIFF", "*.tiff"),
    ("WEBP", "*.webp"),
]


def add_tk_str(root: ttb.Frame, text: str, var: ttb.StringVar):
    """Create label/Entry Text input

    Args:
        root (Frame): main root containing frame
        text (str): Text inside the Label
        var (StringVar): Linked Variable inside the class

    Returns:
        Entry: Frame with Label/Entry/Label
    """
    frame = ttb_frame(root)
    entry = ttb_entry(frame, var)
    ttb_name(frame, text)
    return entry


def ttb_name(root: ttb.Frame, text: str):
    """Create name label of entry item

    Args:
        root (Frame): main root containing frame
        text (str): text inside the label created
    """
    name = ttb.Label(root, text=f"{text}: ")
    name.grid(row=0, column=0, sticky="w", padx=10)


def ttb_entry(root: ttb.Frame, var) -> ttb.Entry:
    """Creare entry widget

    Args:
        root (Frame): main root containing frame
        var (tkinter variable): Type of Variables in tkinter

    Returns:
        Entry: Created entry
    """
    entry = ttb.Entry(root, textvariable=var, width=20)
    entry.grid(row=0, column=1, sticky="e", padx=5)
    return entry


def ttb_frame(root: ttb.Frame) -> ttb.Frame:
    """Create container frame of entry item

    Args:
        root (Frame): main root containing frame

    Returns:
        Frame: Created Frame
    """
    frame = ttb.Frame(root)
    frame.grid(sticky="nsew", pady=2)
    frame.grid_columnconfigure(1, weight=1)
    return frame


def open_file(watermark_var):
    file_path = filedialog.askopenfilename(
        filetypes=image_filetypes, title="Select an image file"
    )
    if not file_path:
        return  # User cancelled

    im = Image.open(file_path).convert("RGBA")
    watermark_text = watermark_var.get()

    # Create watermark
    watermark = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # Load font (default if no TTF available)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = im.width - text_width - 10
    y = im.height - text_height - 10

    draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)

    watermarked = Image.alpha_composite(im, watermark)

    # Ask user where to save (default to same format as opened image)
    default_ext = f".{im.format.lower()}" if im.format else ".png"

    save_path = filedialog.asksaveasfilename(
        defaultextension=default_ext,
        filetypes=image_filetypes,
        title="Save watermarked image",
    )
    if save_path:
        # Convert to RGB if saving to non-alpha format like JPEG
        output_image = (
            watermarked.convert("RGB")
            if save_path.lower().endswith((".jpg", ".jpeg"))
            else watermarked
        )
        output_image.save(save_path)
        print(f"Saved to {save_path}")

        watermark_var.set("")


def main():
    root = ttb.Window()
    main_frame = ttb.Frame(root, padding=10)
    main_frame.grid(sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)

    watermark = ttb.StringVar(value="")
    add_tk_str(main_frame, "Watermark", watermark)
    open_file_bt = ttb.Button(
        main_frame, text="Open File", command=lambda: open_file(watermark)
    )
    open_file_bt.grid(sticky="nsew")

    root.mainloop()


if __name__ == "__main__":
    main()
