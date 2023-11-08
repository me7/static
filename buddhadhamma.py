from pypdf import PdfWriter, PdfReader
from pypdf.annotations import Link, Rectangle, FreeText
import re

start_page = 300
page_no = 0
parts = []
offset = 31 # how many page before start page 1
r = PdfReader("b.pdf")
w = PdfWriter()
thai_to_arabic_digits = {
    "๐": 0,
    "๑": 1,
    "๒": 2,
    "๓": 3,
    "๔": 4,
    "๕": 5,
    "๖": 6,
    "๗": 7,
    "๘": 8,
    "๙": 9,
}

thai_to_arabic_digit_str = {
    ".":"",
    "๐": "0",
    "๑": "1",
    "๒": "2",
    "๓": "3",
    "๔": "4",
    "๕": "5",
    "๖": "6",
    "๗": "7",
    "๘": "8",
    "๙": "9",
    "/":"/"
}

def create_link(x,y,size,text):
      offset = 31 # how many page before start page 1
      pg = thai_to_arabic(text)
      dest = pg+offset
      rect = [x-2,y-2,x+size*len(text)-2, y+size-2]
      # w.add_annotation(page_no, Rectangle(rect=rect))
      w.add_annotation(page_no, Link(target_page_index=dest, rect=rect))

def toc_link(): # gen link in table of content
  pass

def thai_to_arabic(thai_number):
  """Converts a Thai number to an Arabic number.

  Args:
    thai_number: A string representing a Thai number.

  Returns:
    An integer representing the Arabic equivalent of the Thai number.
  """
  arabic_number = 0
  for i in range(len(thai_number)):
    arabic_number += thai_to_arabic_digits[thai_number[i]] * 10**(len(thai_number) - i - 1)
  return arabic_number


def vfn_index(text, cm, tm, font_dict, font_size):
    (x,y) = (tm[4], tm[5])
    if x > 0:
      m = re.search("([๐-๙]+)", text) 
      if m:
        pg = thai_to_arabic(m.group(1))
        dest = pg+offset
        rect = [x-2,y-2,x+8*len(text)-2, y+8-2]
        # w.add_annotation(page_no, Rectangle(rect=rect))
        w.add_annotation(page_no, Link(target_page_index=dest, rect=rect))

# def check_footnote(text):
#    m = re.search("\.([๐-๙]+/[๐-๙]+/[๐-๙]+)", text)
#    if m:
#       res = ""
#       print(m.group(1), text)
#       for c in m.group(1):
#          res += thai_to_arabic_digit_str[c]
#       return res

def thai_to_arabic_str(text):
  res = []
  for c in text:
    res.append(thai_to_arabic_digit_str[c])
  return "".join(res)

def check_footnote(text):
   res = re.findall("\.([๐-๙]+/[๐-๙]+/)", text)
   print(res)
   return res

def vfn_foot(text, cm, tm, font_dict, font_size):
    global parts
    (x,y) = (tm[4], tm[5])
    if y < 200:
      line = 0
      if text == '\n':
        line += 1
        match = check_footnote("".join(parts))
        print("match: ", match)
        start_x = 10
        start_y = 10
        for n, m in enumerate(match):
          end_x += 5*len(m)
          end_y += 15*line
          bookArabic = thai_to_arabic_str(m)
          url = "https://84000.org/tipitaka/read/?"+ bookArabic
          print(url)
          rect = [start_x, end_x , start_y, end_y]
          w.add_annotation(page_no - start_page - 1, FreeText(text=bookArabic, rect=rect))
          w.add_annotation(page_no - start_page - 1, Link(url=url, rect=rect))           
          start_x = end_x
          start_y = end_y
        parts = []
      else:
        parts.append(text)
  

def main():
  global page_no, parts
  for i in range(1,20):
    page_no = start_page + i
    p = r.pages[page_no]
    w.add_page(p)
    parts = []
    print("page: ",page_no+1)
    p.extract_text(visitor_text=vfn_foot)
    # check_footnote("".join(parts))
    w.write("out.pdf")

main()