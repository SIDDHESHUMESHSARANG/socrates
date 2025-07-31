from models import searchData
from models import createPPT
prompt = input('Enter the topic of presentation: ')
slideCount = int(input('How many slides long ppt do you want? : '))
response = searchData.getPPTData(prompt, slideCount)

sanitizedPrompt = prompt.replace(' ',"_")
createPPT.createPresentation(response, output_filename=f"{sanitizedPrompt}.pptx")