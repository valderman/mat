import tempfile

__days = [
    u"MÅNDAG",
    u"TISDAG",
    u"ONSDAG",
    u"TORSDAG",
    u"FREDAG",
    u"VECKANS FÅNGST (FISH OF THE"
]

def food(api, date):
    if not api.is_current_week(date):
        return []
    if not api.is_weekday(date):
        return []
    if not api.pdf:
        raise EnvironmentError("PDF is not supported on this machine")

    def read_first_pdf_page(raw_pdf):
        with tempfile.NamedTemporaryFile() as pdf_file:
            pdf_file.write(raw_pdf)
            pdf = api.pdf.open(pdf_file.name)
            return pdf.load_page(0).get_text()

    response = api.requests.get("https://www.beebar.se/goteborg/mat-dryck/veckolunch")
    pdf_lines = read_first_pdf_page(response.content).splitlines()

    dagens_line = pdf_lines.index(__days[date.isoweekday()-1])
    dagens_end_line = pdf_lines.index(__days[date.isoweekday()])
    dagens_lines = pdf_lines[dagens_line+2:dagens_end_line]

    fish_line = pdf_lines.index(u"VECKANS FÅNGST (FISH OF THE")
    veg_line = pdf_lines.index(u"VECKANS VEGETARISKA")
    veg_end_line = pdf_lines.index(u"ALLTID PÅ LUNCHEN")

    fish_lines = pdf_lines[fish_line+3:veg_line]
    veg_lines = pdf_lines[veg_line+3:veg_end_line]

    dagens = api.food(dagens_lines[0], ' '.join(dagens_lines[1:]))
    fish = api.food(fish_lines[0], ' '.join(fish_lines[1:]))
    vegetarian = api.food(veg_lines[0], ' '.join(veg_lines[1:]))
    return [dagens, fish, vegetarian]

def name():
    return u"Bee Kök & Bar"