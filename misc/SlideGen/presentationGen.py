from presentationTools import *

def parse_input(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
        data = [x.strip() for x in data]
        
    
    sections = {}
    curr_list = []
    first_item = True
    for line in data:
        if len(line) > 0:
            # if the first item of a series of lines, create a new section
            if first_item:
                sections[line] = curr_list
                first_item = False
            else:
                curr_list.append(line)
        else:
            if len(curr_list) > 0:
                curr_list = []
                first_item = True
                
    return sections
    
            
filename = 'gen_meeting_22_07_05.txt'            
out = parse_input(filename)
basic_slide_names = []
# collect all names into one list
for key in out:
    basic_slide_names.extend(out[key])
num_basic_slides = len(basic_slide_names)

creds = get_creds()

slides_service = build('slides', 'v1', credentials=creds)
presentation_id = '13cxiZ0WeY9aQAWkU5W3q41GdxI-cw4cjIVTICmCqlCg'

p1 = Presentation(slides_service, presentation_id)

title, section_slide, basic_slide = p1.slides[:3]

# duplicate the basic slide template for each topic slide to be created
for i in range(num_basic_slides):
    new_id = f"basicSlide_{i+1}"
    p1.add_edit(basic_slide.duplicate(new_id))
    # don't have slide objects for the newly duplicated slides since they haven't been created

p1.send_edits()

# unskip topic slides, & set title appropriately
for i, slide in enumerate(p1.slides[3:]):
      p1.add_edit(slide.unskip())
      # for now all slides are only slide objects in presentation
      t_slide = TextSlide(slide.raw, slide.pres)
      t_slide.set_title(basic_slide_names[i])
# 
p1.send_edits()
