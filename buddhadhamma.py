from pypdf import PdfWriter, PdfReader
from pypdf.annotations import Link, Rectangle, FreeText
import re

page_no = 0
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

def vfn_toc(text, cm, tm, font_dict, font_size):
    (x,y) = (tm[4], tm[5])
    if x > 400:
      m = re.search("^([๐-๙]+)", text) 
      if m:
        pg = thai_to_arabic(m.group(1))
        dest = pg+offset
        rect = [12,y-2,x+12*len(text), y+10]
        # w.add_annotation(page_no, Rectangle(rect=rect))
        w.add_annotation(page_no, Link(target_page_index=dest, rect=rect))
  

def main():
  global page_no
  w.add_outline_item('toc',9)
  w.add_outline_item('index', 1258)

  for page_no in range(0, len(r.pages)):
  # for page_no in range(0, 200):
    p = r.pages[page_no]
    w.add_page(p)
    print(page_no)
    if page_no in range(9,31):
       p.extract_text(visitor_text=vfn_toc)
    if page_no > 1257:
        p.extract_text(visitor_text=vfn_index)

  w.write("out.pdf")

main()
