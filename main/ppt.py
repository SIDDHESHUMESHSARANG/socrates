from models import searchData
from models import createPPT

def getPPT(prompt, slideCount, style="Geometric"):
    response = searchData.getPPTData(prompt, slideCount)
    sanitizedPrompt = prompt.replace(' ', "_")
    ppt = createPPT.createPresentation(response, output_filename=f"{sanitizedPrompt}.pptx", style=style)
    return ppt