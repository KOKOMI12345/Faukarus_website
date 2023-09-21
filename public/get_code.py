import random
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from flask import make_response,session
def get_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


def get_code():
    valid_code = ''
    img = Image.new('RGB',(280,40),get_random_color())
    #写文字
    font = ImageFont.truetype('public/font.ttf', 24)

    draw = ImageDraw.Draw(img)
    #动态生成大写小写数字5个
    for i in range(5):
        num = str(random.randint(0,9))
        up_char = str(chr(random.randint(65,90)))
        lower_cahr = str(chr(random.randint(97,122)))
        ss = random.choice([num,up_char,lower_cahr])
        valid_code += ss
        draw.text((30+i*50,5),ss,font=font)
    #画点和线
    width = 320
    height = 35
    for i in range(5):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        #在图片上画线
        draw.line((x1,y1,x2,y2),fill=get_random_color())
    session['valid_code'] = valid_code
    for i in range(100):
        #画点
        draw.point([random.randint(0,width),random.randint(0,height)],fill=get_random_color())
        x = random.randint(0,width)
        y = random.randint(0,height)
        #画弧形
        draw.arc((x,y,x+4,y+4),0,90,fill=get_random_color())
    f = BytesIO()
    img.save(f,'png')
    #把文件从对象中取出来
    response = make_response(f.getvalue())
    return response