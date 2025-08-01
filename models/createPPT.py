import re
from pptx import Presentation # type: ignore
from pptx.util import Pt, Inches # type: ignore
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN # type: ignore
from pptx.dml.color import RGBColor # type: ignore
import requests # type: ignore
from io import BytesIO
from PIL import Image  # type: ignore

def createPresentation(groq_content, image_data_list, output_filename): 
    prs = Presentation()
    blank_layout = prs.slide_layouts[6]
    sections = re.split(r"(?=\*\*.*?\*\*)", groq_content.strip())

    
    
    image_urls = image_data_list

    image_counter = 0

    def set_font(run, size, bold=False, color=None):
        run.font.size = Pt(size)
        run.font.bold = bold
        if color:
            run.font.color.rgb = RGBColor(*color)

    def add_slide(content, slide_index, center_text=False): 
        nonlocal image_counter 

        slide = prs.slides.add_slide(blank_layout)

        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(235, 240, 255)

        match = re.match(r"\*\*(.*?)\*\*\s*(.*)", content.strip(), re.DOTALL)
        if match:
            title = match.group(1).strip()
            body_text = match.group(2).strip()
        else:
            print(f"Skipping malformed section: {content[:50]}...")
            return

        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(8), Inches(1))
        title_tf = title_box.text_frame
        p = title_tf.paragraphs[0]
        run = p.add_run()
        run.text = title
        set_font(run, 36, bold=True, color=(40, 0, 100))
        p.alignment = PP_ALIGN.CENTER
        title_tf.word_wrap = True

        image_on_left = (slide_index % 2 == 0) 
        
        content_width = Inches(8.6)
        text_width = Inches(4.5)  
        image_width = Inches(4.0) 

        if image_on_left:
            image_left = Inches(0.5)
            text_left = Inches(5.0) 
        else:
            text_left = Inches(0.5)
            image_left = Inches(5.0) 

        
        body_box = slide.shapes.add_textbox(text_left, Inches(1.6), text_width, Inches(4.5))
        body_tf = body_box.text_frame
        body_tf.word_wrap = True
        body_tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

        paragraphs = [para.strip() for para in body_text.split("•") if para.strip()]
        for para_text in paragraphs:
            p = body_tf.add_paragraph()
            run = p.add_run()
            run.text = f"• {para_text}"
            set_font(run, 22, color=(50, 50, 50))
            p.alignment = PP_ALIGN.CENTER if center_text else PP_ALIGN.LEFT

        
        if image_urls and image_counter < len(image_urls):
            img_url = image_urls[image_counter]
            print(f"Slide {slide_index}: Attempting to download image from: {img_url}") 
            try:
                
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
                
                response = requests.get(img_url, headers=headers, timeout=30) 
                response.raise_for_status() 
                
                image_data = BytesIO(response.content)
                
                
                if len(image_data.getvalue()) == 0:
                    print(f"Slide {slide_index}: Warning: Downloaded image data for {img_url} is empty.")
                    
                    image_counter += 1
                    return 
                
                
                try:
                    Image.open(image_data).verify() 
                    image_data.seek(0) 
                except Exception as img_exc:
                    print(f"Slide {slide_index}: Warning: Image verification failed for {img_url}: {img_exc}")
                    image_counter += 1 
                    return


                pic = slide.shapes.add_picture(image_data, image_left, Inches(1.6), width=image_width) 
                
                image_counter += 1
                print(f"Slide {slide_index}: Successfully added image from: {img_url}") 

            except requests.exceptions.RequestException as e:
                print(f"Slide {slide_index}: Error fetching image from {img_url}: {e}")
            except Exception as e:
                print(f"Slide {slide_index}: General error adding image: {e}")
        else:
            print(f"Slide {slide_index}: No image available or counter out of bounds for this slide.") 

    for i, section in enumerate(sections):
        add_slide(section, i) 

    prs.save(output_filename)
