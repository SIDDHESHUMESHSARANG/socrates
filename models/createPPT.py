import re
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.dml.color import RGBColor

def createPresentation(groq_content, output_filename):
    prs = Presentation()
    blank_layout = prs.slide_layouts[6]
    sections = re.split(r"(?=\*\*.*?\*\*)", groq_content.strip())

    def set_font(run, size, bold=False, color=None):
        run.font.size = Pt(size)
        run.font.bold = bold
        if color:
            run.font.color.rgb = RGBColor(*color)

    def add_slide(content, center_text=False):
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

        
        body_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.6), Inches(8), Inches(4.5))
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

    
    if sections:
        add_slide(sections.pop(0), center_text=True)

    
    for section in sections:
        add_slide(section)

    prs.save(output_filename)
    print(f"✨ Presentation '{output_filename}' created successfully!")