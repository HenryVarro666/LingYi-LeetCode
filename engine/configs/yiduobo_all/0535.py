CONFIG = dict(
    num=535, title='TinyURL的加密与解密', difficulty='Medium', category='设计',
    author='yiduobo', technique='62 进制编码 + 随机不重复',
    code='''
class Codec:

    def __init__(self):
        self.key_dict = {}
        self.pos_dict = {}
        self.rest_key = 62 ** 6

    def encode(self, longUrl):
        self.rest_key -= 1
        key_num = random.randint(0, self.rest_key)
        if key_num in self.pos_dict:
            real_key_num = self.pos_dict[key_num]
        else:
            real_key_num = key_num
        
        if self.rest_key in self.pos_dict:
            self.pos_dict[key_num] = self.pos_dict[self.rest_key]
        else:
            self.pos_dict[key_num] = self.rest_key

        self.pos_dict[self.rest_key] = real_key_num
        self.key_dict[real_key_num] = longUrl

        shortUrl = ''
        for index in range(6):
            tmp = real_key_num % 62
            if tmp < 10:
                shortUrl = str(tmp) + shortUrl
            elif tmp < 36:
                shortUrl = chr(int(tmp) + 87) + shortUrl
            else:
                shortUrl = chr(int(tmp) + 29) + shortUrl

            real_key_num //= 62

        return shortUrl

    def decode(self, shortUrl):

        key = 0
        for char in shortUrl:
            if char <= '9':
                tmp = int(char)
            elif char >= 'a':
                tmp = ord(char) - 87
            else:
                tmp = ord(char) - 29
            key = key * 62 + tmp
        return self.key_dict[key]
''',
    setup='import random; random.seed(0)',
    call="""c = Codec()
u1 = c.encode('leetcode.com/p/1')
u2 = c.encode('leetcode.com/p/2')
[u1, c.decode(u1), u2, c.decode(u2)]""",
    expect=['w5r0dL', 'leetcode.com/p/1', '1YfdRz', 'leetcode.com/p/2'],
    views=[
        dict(type='text', h=60, fn=lambda S: f"总空间 `62^6` = =={62**6}== 个短链；还剩 `rest_key` = {S['self'].rest_key}" if 'self' in S else ''),
        dict(type='map', var='self.key_dict', label='key_dict：数字 → 原始 url', h=170, font=22),
        dict(type='map', var='self.pos_dict', label='pos_dict：随机位置 → 实际数字（防重复）', h=170, font=22),
        dict(type='text', h=70, fn=lambda S: f"短链 shortUrl = ==`{S['shortUrl']}`==" if 'shortUrl' in S and S['_line'] else ''),
    ],
    watch=['key_num', 'real_key_num', 'tmp', 'shortUrl', 'key'],
    captions={
        'self.rest_key -= 1': '剩余可用数字少一个：`rest_key` → {self.rest_key}',
        'random.randint': '在 `[0, rest_key]` 里随机一个位置 `key_num` = {key_num}',
        'real_key_num = self.pos_dict[key_num]': '这个位置以前被抽过，它现在实际代表 `{real_key_num}`',
        'real_key_num = key_num': '没抽过，位置就是数字本身：`{real_key_num}`',
        'self.pos_dict[key_num] = self.pos_dict[self.rest_key]': '把末尾位置的真实值换到 key_num，抽过的数字不会再出现',
        'self.pos_dict[key_num] = self.rest_key': '末尾位置 `rest_key` 还没被动过，换到 key_num',
        'self.pos_dict[self.rest_key] = real_key_num': '末尾位置记下刚用掉的数字，和 519 题一样做洗牌',
        'self.key_dict[real_key_num]': '记下映射：数字 `{real_key_num}` → 原始 url',
        'tmp = real_key_num % 62': '取最低一位 62 进制：`tmp` = {tmp}',
        'if tmp < 10': '`tmp = {tmp}` 判断是否数字 0-9',
        'elif tmp < 36': '`tmp = {tmp}` 判断是否小写 a-z',
        'shortUrl = str(tmp)': '0-9 直接用数字，补到最前面 → `{shortUrl}`',
        'shortUrl = chr(int(tmp) + 87)': '10-35 映射为 a-z，补到最前面 → `{shortUrl}`',
        'shortUrl = chr(int(tmp) + 29)': '36-61 映射为 A-Z，补到最前面 → `{shortUrl}`',
        'real_key_num //= 62': '去掉最低位，继续处理下一位：`{real_key_num}`',
        'return shortUrl': '6 位短链生成：`{shortUrl}`',
        'key = 0': '解码：把短链按 62 进制还原成数字',
        'if char <= ': '`{char}` 是数字字符吗',
        'tmp = int(char)': '数字字符：`tmp = {tmp}`',
        'tmp = ord(char) - 87': '小写字母：还原成 10-35，`tmp = {tmp}`',
        'tmp = ord(char) - 29': '大写字母：还原成 36-61，`tmp = {tmp}`',
        'key = key * 62': '`key = key * 62 + tmp` = {key}',
        'return self.key_dict[key]': '用还原出的数字查 key_dict，得到原始 url',
    },
    skip=['for index in range(6)', 'if tmp < 10', 'elif tmp < 36', 'real_key_num //= 62', 'for char in shortUrl', 'if char <=', 'key = 0', 'shortUrl = \'\''],
    max_steps=75,
    cards=dict(
        one_liner='随机数 → 62 进制 6 位串，dict 记映射',
        complexity='每次操作 `O(1)`（6 位），空间 `O(n)`',
        problem=['`encode` 把长链接变成短链接，`decode` 再还原',
                 '算法自由设计，只要两者互逆即可',
                 '本视频：连续编码两个链接，再各自解码'],
        quote='在加密时，随机一个数，将其按照62进制的编码方式变成TinyURL，同时使用一个dict保存这个数到原始url的映射。',
        quote_src='—— yiduobo 题解原文',
        idea=['a-z、A-Z、0-9 共 62 个字符，6 位有 `62^6` 种短链',
              '随机数用 519 题的洗牌法，不会抽到重复数字',
              '解码就是把 6 位字符按 62 进制还原成数，再查 dict'],
        summary=['时间 `O(1)` 每次，空间 `O(n)`',
                 '随机种子在视频里固定为 0，所以短链是固定的',
                 '原文为 Python 2 写法，`real_key_num /= 62` 已改为 `//= 62`，并删去了 `:type` 文档字符串',
                 '易错：不去重会撞车；整数除法在 Python 3 必须用 `//`'],
    ),
)
