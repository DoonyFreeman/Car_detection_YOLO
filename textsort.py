def char_to_int(text):
    text = text.replace('O','0').replace('I','1').replace('J','3').replace('A','4').replace('G','6').replace('B','8').replace('S','5')
    return text

def int_to_char(text):
    text = text.replace('0','O').replace('1','I').replace('3','J').replace('4','A').replace('6','G').replace('8','B').replace('5','S')
    return text

def eng_to_ru(text):
    text = text.replace('A','А').replace('B','В').replace('E','Е').replace('K','К').replace('M','М').replace('H','Н').replace('O','О').replace('P','Р').replace('C','С').replace('T','Т').replace('Y','У').replace('X','Х')
    return text

def plate_format(text):
    if (8 > len(text)) or (len(text) > 9):
        return False
    else:
        text_full = ''
        text_full = text_full + int_to_char(text[0])
        text_full = text_full + char_to_int(text[1])
        text_full = text_full + char_to_int(text[2])
        text_full = text_full + char_to_int(text[3])
        text_full = text_full + int_to_char(text[4])
        text_full = text_full + int_to_char(text[5])
        text_full = text_full + char_to_int(text[6])
        text_full = text_full + char_to_int(text[7])
        if len(text) == 9:
            text_full = text_full + char_to_int(text[8])
        return text_full

def text_filter(text):
    if plate_format(text) == False:
        return ''
    else:
        text = plate_format(text)
        text = eng_to_ru(text)
    return text

