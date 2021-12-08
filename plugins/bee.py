import tempfile
import re

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
            return pdf.get_page_text(0)

    response = api.requests.get("https://www.beebar.se/goteborg/mat-dryck/veckolunch")
    pdf_lines = read_first_pdf_page(response.content).splitlines()

    dagens_line = pdf_lines.index(__days[date.isoweekday()-1])
    dagens_end_line = pdf_lines.index(__days[date.isoweekday()])
    dagens_lines = pdf_lines[dagens_line+2:dagens_end_line]

    fish_line = pdf_lines.index(u"VECKANS FISK (FISH OF THE WEEK)")
    veg_line = pdf_lines.index(u"VECKANS VEGETARISKA")
    veg_end_line = pdf_lines.index(u"ALLTID PÅ LUNCHEN")

    fish_lines = pdf_lines[fish_line+3:veg_line]
    veg_lines = pdf_lines[veg_line+3:veg_end_line]

    def get_fish():
        today_fish_text = u"MÅNDAG TILL ONSDAG" if date.isoweekday() < 4 else u"TORSDAG OCH FREDAG"
        today_fish_line = pdf_lines.index(today_fish_text)
        end_fish_line = pdf_lines.index(u"TORSDAG OCH FREDAG") if date.isoweekday() < 4 else veg_line
        fish_lines = pdf_lines[today_fish_line+1:end_fish_line]
        fish_heading = re.sub("\\(([^)]+)\\).*", "\\1", fish_lines[0])
        return api.food(fish_heading, ' '.join(fish_lines))

    dagens = api.food(dagens_lines[0], ' '.join(dagens_lines[1:]))
    fish = get_fish()
    vegetarian = api.food(None, ' '.join(veg_lines))
    return [dagens, fish, vegetarian]

def name():
    return u"Bee Kök & Bar"