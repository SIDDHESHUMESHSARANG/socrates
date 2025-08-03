from models import searchData
from models import createPPT
from models import fetchImages

def getPPT(prompt, slideCount) :
    response = searchData.getPPTData(prompt, slideCount)
    responseKeywords = fetchImages.topicKeywords(response)
    images = fetchImages.getPPTImages(responseKeywords,slideCount)

    sanitizedPrompt = prompt.replace(' ',"_")
    ppt = createPPT.createPresentation(response, images, output_filename=f"{sanitizedPrompt}.pptx")
    return ppt