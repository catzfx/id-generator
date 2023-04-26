from PIL import Image, ImageDraw, ImageFont

def generate_id(data: dict, template_path = 'template.png'):
    def draw_text_psd_style(draw, xy, text, font, tracking=0, leading=None, **kwargs):
        """
        usage: draw_text_psd_style(draw, (0, 0), "Test", 
                    tracking=-0.1, leading=32, fill="Blue")

        Leading is measured from the baseline of one line of text to the
        baseline of the line above it. Baseline is the invisible line on which most
        letters—that is, those without descenders—sit. The default auto-leading
        option sets the leading at 120% of the type size (for example, 12‑point
        leading for 10‑point type).

        Tracking is measured in 1/1000 em, a unit of measure that is relative to 
        the current type size. In a 6 point font, 1 em equals 6 points; 
        in a 10 point font, 1 em equals 10 points. Tracking
        is strictly proportional to the current type size.
        """
        def stutter_chunk(lst, size, overlap=0, default=None):
            for i in range(0, len(lst), size - overlap):
                r = list(lst[i:i + size])
                while len(r) < size:
                    r.append(default)
                yield r
        x, y = xy
        font_size = font.size
        lines = text.splitlines()
        if leading is None:
            leading = font.size * 1.2
        for line in lines:
            for a, b in stutter_chunk(line, 2, 1, ' '):
                w = font.getlength(a + b) - font.getlength(b)
                # dprint("[debug] kwargs")
                # print("[debug] kwargs:{}".format(kwargs))
                    
                draw.text((x, y), a, font=font, **kwargs)
                x += w + (tracking / 1000) * font_size
            y += leading
            x = xy[0]

    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    bottom_font = ImageFont.truetype('OCRB REGULAR.ttf', 57)
    main_font = ImageFont.truetype('OCR-B.ttf', 34)
    br_left = 100
    mr_left = 480
    cnp_left = 550
    cnp_top = 228
    series_left = 930
    series_top = 185
    series_left2 = series_left + 140

    # rid dict key strings of incompatible characters
    for key in data:
        if type(data[key]) is str:
            data[key] = data[key].replace('ș', 's').replace('ț', 't')


    # draw bottom row
    draw_text_psd_style(draw, (br_left, 900), ''.join(data['mrz'][0]), bottom_font, 90, fill='Black')
    draw_text_psd_style(draw, (br_left, 970), ''.join(data['mrz'][1]), bottom_font, 90, fill='Black')
    
    # draw main row
    draw_text_psd_style(draw, (mr_left, 325), data['surname'], main_font, -160, fill='Black')
    draw_text_psd_style(draw, (mr_left, 405), data['name'], main_font, -160, fill='Black')
    draw_text_psd_style(draw, (mr_left, 490), 'Română / ROU', main_font, -150, fill='Black')
    draw_text_psd_style(draw, (mr_left, 570), f'Jud.{data["area_id"]} {data["locality"]}', main_font, -150, fill='Black')
    draw_text_psd_style(draw, (mr_left, 650), f'Jud.{data["area_id"]} {data["locality"]}\n{data["address"]}', main_font, -150, fill='Black', leading=50)

    #   remove prefix from locality
    i = data['locality'].find('.')
    if i != -1:
        data['locality'] = data['locality'][i + 1:]
        
    #   draw locality
    draw_text_psd_style(draw, (mr_left, 800), f'SPCLEP {data["locality"]}', main_font, -150, fill='Black')

    # draw cnp
    draw_text_psd_style(draw, (cnp_left, cnp_top), f'{data["cnp"][0]}', main_font, -150, fill='Red')
    draw_text_psd_style(draw, (cnp_left + main_font.getlength('1') - 6, cnp_top), ''.join(data["cnp"][1:7]), main_font, -150, fill='Black')
    draw_text_psd_style(draw, (cnp_left + main_font.getlength('123456') - 8, cnp_top), ''.join(data["cnp"][7:]), main_font, -150, fill='Red')
    
    # draw series
    draw_text_psd_style(draw, (series_left, series_top), data['series'], main_font, -150, fill='Black')
    draw_text_psd_style(draw, (series_left2, series_top), ''.join(data['series_number']), main_font, -150, fill='Black')

    # draw sex
    draw_text_psd_style(draw, (1420, 490), data['sex'], main_font, -150, fill='Black')

    # draw expiry date
    draw_text_psd_style(draw, (1150, 800), f'{"0" * (2 - len(str(data["emission_date"].day))) + str(data["emission_date"].day)}.{"0" * (2 - len(str(data["emission_date"].month))) + str(data["emission_date"].month)}.{str(data["emission_date"].year)[2:]}-{"0" * (2 - len(str(data["expiry_date"].day))) + str(data["expiry_date"].day)}.{"0" * (2 - len(str(data["expiry_date"].month))) + str(data["expiry_date"].month)}.{str(data["expiry_date"].year)[2:]}', main_font, -150, fill='Black')

    # draw person picture
    picture = Image.open('picture.png').resize((430, 570)) # 620 x 720 resolution
    img_final = img.copy()
    img_final.paste(picture, (40, 150))

    img_final.show()
    img_final.save('result.png')


if __name__ == '__main__':
    generate_id({})