import random
from PIL import Image, ImageDraw, ImageFont
import time
import os
import string


# Captcha验证码
class Captcha(object):
    font_path = os.path.join(os.path.dirname(__file__), 'verdana.ttf')
    number = 4   # 验证码位数
    size = (100, 40)   # 验证码图片的宽高
    bgcolor = (0, 0, 0)
    random.seed(int(time.time()))
    fontcolor = (random.randint(200, 255), random.randint(100, 255), random.randint(100, 255))
    fontsize = 20   # 验证码字体大小
    linecolor = (random.randint(0, 250), random.randint(0, 255), random.randint(0, 250))   # 随机干扰线的颜色
    draw_line = True   # 是否加入干扰线
    draw_point = True   # 是否加入噪点
    line_number = 3   # 加入干扰线的条数

    # 验证码包括大小写字母和数字
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 随机生成一个字符串
    # 定义成私有类方法，对象在外部不能直接调用
    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE, cls.number))

    # 绘制干扰线，随机生成一对起点和终点，并连接成线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.linecolor)

    # 绘制干扰点，
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))   # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    # 生成验证码
    @classmethod
    def gene_code(cls):
        width, height = cls.size
        image = Image.new('RGBA', (width, height), cls.bgcolor)   # 创建画板
        font = ImageFont.truetype(cls.font_path, cls.fontsize)
        draw = ImageDraw.Draw(image)   # 创建画笔
        text = cls.gene_text()
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width)/2, (height - font_height)/2), text, font=font, fill=cls.fontcolor)
        if cls.draw_line:
            # 遍历， 即画line_number条线
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)

        return text, image
