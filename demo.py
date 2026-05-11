import main.ppt as ppt

inp = input("Enter the topic: ")
sc = int(input("Enter the number of slides: "))
print("\nAvailable styles: Geometric, PlainText")
style = input("Enter the style (default: Geometric): ").strip() or "Geometric"

ppt.getPPT(inp, sc, style)