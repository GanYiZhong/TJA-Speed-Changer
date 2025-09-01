#!/usr/bin/env python3
"""
Create ZhongTaiko Logo
Creates the LOGO_BLACK_TRANS.png file if PIL is available
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("PIL not available. Please install Pillow: pip install Pillow")
    exit(1)

def create_logo():
    """Create a simple ZhongTaiko logo"""
    # Create a new image with transparency
    width, height = 300, 180
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    black = (0, 0, 0, 255)
    
    # Draw controller outline (simplified gamepad shape)
    controller_width = 200
    controller_height = 80
    controller_x = (width - controller_width) // 2
    controller_y = 20
    
    # Main controller body
    draw.rounded_rectangle(
        [controller_x, controller_y, controller_x + controller_width, controller_y + controller_height],
        radius=20,
        outline=black,
        width=4
    )
    
    # D-pad (left side)
    dpad_x = controller_x + 30
    dpad_y = controller_y + 25
    dpad_size = 25
    
    # D-pad horizontal bar
    draw.rectangle(
        [dpad_x - 10, dpad_y + 7, dpad_x + dpad_size + 10, dpad_y + 17],
        outline=black,
        width=3
    )
    
    # D-pad vertical bar
    draw.rectangle(
        [dpad_x + 7, dpad_y - 10, dpad_x + 17, dpad_y + dpad_size + 10],
        outline=black,
        width=3
    )
    
    # Center button
    center_x = controller_x + controller_width // 2
    center_y = controller_y + controller_height // 2
    draw.rounded_rectangle(
        [center_x - 12, center_y - 12, center_x + 12, center_y + 12],
        radius=3,
        outline=black,
        width=3
    )
    
    # Center dot
    draw.ellipse(
        [center_x - 3, center_y - 3, center_x + 3, center_y + 3],
        fill=black
    )
    
    # Action buttons (right side)
    button_x = controller_x + controller_width - 60
    button_y = controller_y + 25
    
    # Four action buttons
    button_positions = [
        (button_x, button_y - 5),      # Top
        (button_x + 20, button_y + 10), # Right
        (button_x, button_y + 25),      # Bottom
        (button_x - 20, button_y + 10)  # Left
    ]
    
    for bx, by in button_positions:
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], outline=black, width=3)
    
    # Shoulder buttons
    # Left shoulder
    draw.arc(
        [controller_x - 10, controller_y - 15, controller_x + 40, controller_y + 15],
        start=90, end=270, fill=black, width=4
    )
    
    # Right shoulder  
    draw.arc(
        [controller_x + controller_width - 40, controller_y - 15, 
         controller_x + controller_width + 10, controller_y + 15],
        start=270, end=90, fill=black, width=4
    )
    
    # Stand/base
    base_y = controller_y + controller_height + 10
    draw.rectangle(
        [controller_x + 40, base_y, controller_x + controller_width - 40, base_y + 15],
        outline=black,
        width=4
    )
    
    # Stand legs
    draw.rectangle(
        [controller_x + 60, base_y + 15, controller_x + 80, base_y + 25],
        outline=black,
        width=3
    )
    draw.rectangle(
        [controller_x + controller_width - 80, base_y + 15, 
         controller_x + controller_width - 60, base_y + 25],
        outline=black,
        width=3
    )
    
    # Text
    try:
        # Try to use a bold font if available
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # ZhongTaiko text
    text1 = "ZhongTaiko"
    text_bbox = draw.textbbox((0, 0), text1, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = height - 50
    draw.text((text_x, text_y), text1, fill=black, font=font_large)
    
    # THE CONTROLLER text
    text2 = "THE CONTROLLER."
    text_bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    text_width2 = text_bbox2[2] - text_bbox2[0]
    text_x2 = (width - text_width2) // 2
    text_y2 = height - 25
    draw.text((text_x2, text_y2), text2, fill=black, font=font_small)
    
    # Save the image
    img.save("LOGO_BLACK_TRANS.png", "PNG")
    print("Logo created: LOGO_BLACK_TRANS.png")

if __name__ == "__main__":
    if HAS_PIL:
        create_logo()
    else:
        print("Cannot create logo without PIL/Pillow")