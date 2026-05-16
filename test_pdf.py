from utils.pdf_exporter import create_pdf

q = [{'id': 1, 'keyword': 'test', 'question': 'What is test?', 'type': 'Definition', 'difficulty': 'Easy', 'importance': 'High'}]
try:
    b = create_pdf(q)
    print("PDF bytes length:", len(b))
    print("Type:", type(b))
    with open("test.pdf", "wb") as f:
        f.write(b)
    print("Successfully wrote test.pdf")
except Exception as e:
    import traceback
    traceback.print_exc()
