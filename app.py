from models import searchData
from models import createPPT
from models import fetchImages

prompt = input('Enter the topic of presentation: ')
slideCount = int(input('How many slides long ppt do you want? : '))
response = searchData.getPPTData(prompt, slideCount)
responseKeywords = fetchImages.topicKeywords(response)
images = fetchImages.getPPTImages(responseKeywords,slideCount)

sanitizedPrompt = prompt.replace(' ',"_")
createPPT.createPresentation(response, images, output_filename=f"{sanitizedPrompt}.pptx")