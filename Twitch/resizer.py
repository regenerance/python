import sys
import os
from PIL import Image

def resize_image(image_path, output_sizes, compress=False):
    try:
        compressed_img = "comp"
        img = Image.open(image_path)
        file_name, ext = os.path.splitext(image_path)

        if img.format == 'GIF':
            for size in output_sizes:
                img.seek(0)
                frames = []
                try:
                    while True:
                        frame = img.copy()
                        frame = frame.resize((size[0], size[1]), Image.Resampling.LANCZOS)
                        if compress:
                            frame = frame.convert('P', palette=Image.ADAPTIVE)
                        frames.append(frame)
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass

                if compress:
                    new_file_name = f"{file_name}_{compressed_img}_{size[0]}x{size[1]}{ext}"
                else:
                    new_file_name = f"{file_name}_{size[0]}x{size[1]}{ext}"
                frames[0].save(new_file_name, save_all=True, append_images=frames[1:], loop=0)
                print(f"Saved: {new_file_name}")
        else:
            for size in output_sizes:
                resized_img = img.resize((size[0], size[1]), Image.Resampling.LANCZOS)
                if compress:
                    new_file_name = f"{file_name}_{compressed_img}_{size[0]}x{size[1]}{ext}"
                else:
                    new_file_name = f"{file_name}_{size[0]}x{size[1]}{ext}"
                if compress:
                    resized_img.save(new_file_name, optimize=True, quality=85)
                else:
                    resized_img.save(new_file_name)
                print(f"Saved: {new_file_name}")

    except Exception as e:
        print(f"Failed to resize {image_path}. Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Welcome to the Twitch Image Resizer by @mp_rust. Please drag and drop an image file onto the EXE.")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.isfile(image_path):
        print(f"File not found: {image_path}")
        sys.exit(1)

    print("Please type one of the following commands: Avatar, Badges, Banner, or Emotes (you may add 'c' at the end to compress your files). This EXE only supports .jpg, .png, and .gif files.")
    user_input = input().strip().lower().split()

    if len(user_input) == 0:
        print("No input provided. Exiting.")
        sys.exit(1)

    image_type = user_input[0]
    compress = len(user_input) > 1 and user_input[1] == "c"

    if image_type == "avatar":
        output_sizes = [(480, 480), (1000, 1000)]
    elif image_type == "badges":
        output_sizes = [(18, 18), (36, 36), (72, 72)]    
    elif image_type == "banner":
        output_sizes = [(1200, 480)]
    elif image_type == "emotes":
        output_sizes = [(28, 28), (56, 56), (112, 112)]
    else:
        print("Invalid command type... Please type one of the following commands: 'Avatar', 'Badges', 'Banner', or 'Emotes' (you may add 'c' at the end to compress your files). This EXE only supports .jpg, .png, and .gif files.")
        sys.exit(1)

    resize_image(image_path, output_sizes, compress)

if __name__ == "__main__":
    main()