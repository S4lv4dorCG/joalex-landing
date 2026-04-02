from PIL import Image

def process_logo(input_path, output_path, target_rgb):
    try:
        img = Image.open(input_path).convert('RGBA')
        data = img.getdata()
        
        new_data = []
        for r, g, b, a in data:
            # Calculate luminance (0 to 255)
            # Assuming logo is bright graphics on dark background OR dark on light.
            luminance = (0.299 * r + 0.587 * g + 0.114 * b)
            
            # For a typical JPEG logo with a dark background, the graphics are bright.
            # We will use luminance as the alpha channel!
            # High luminance = opaque graphic, Low luminance = transparent background.
            # Then we color the opaque parts with target_rgb.
            
            # If the background is actually white, luminance will be high for bg and low for graphic.
            # We can check the first pixel (usually background).
            bg_luminance = 0.299*data[0][0] + 0.587*data[0][1] + 0.114*data[0][2]
            
            if bg_luminance > 128:
                # White background -> invert alpha mapping
                alpha = int(255 - luminance)
            else:
                # Black background -> direct alpha mapping
                alpha = int(luminance)
                
            # Enhance alpha to make graphics punchy and background vanished
            alpha = max(0, min(255, int((alpha - 20) * 1.5)))
            
            new_data.append((target_rgb[0], target_rgb[1], target_rgb[2], alpha))
            
        img.putdata(new_data)
        img.save(output_path, "PNG")
        print(f"Success! Saved as {output_path}")
    except Exception as e:
        print(f"Error: {e}")

process_logo("Logo.jpeg", "Logo_copper.png", (188, 139, 93))
