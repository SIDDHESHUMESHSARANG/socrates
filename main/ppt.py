from models import searchData
from models import createPPT

def getPPT(prompt, slideCount) :
    response = searchData.getPPTData(prompt, slideCount)
    from models import fetchImages
    keywords = fetchImages.topicKeywords(prompt)
    images = fetchImages.getPPTImages(keywords, slideCount)

    sanitizedPrompt = prompt.replace(' ',"_")
    ppt = createPPT.createPresentation(response, output_filename=f"{sanitizedPrompt}.pptx", images=images)
    return ppt