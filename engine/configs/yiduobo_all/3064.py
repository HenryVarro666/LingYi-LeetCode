CONFIG = dict(
    num=3064, title='使用按位查询猜测数字 I', difficulty='Medium', category='位运算',
    author='yiduobo', technique='逐位询问 2 的幂', tags=['位运算', '贪心与思维'],
    code='''
class Solution(object):
    def findNumber(self):
        
        res = 0
        v = 1
        for index in range(30):
            if commonSetBits(v):
                res += v
            v += v
        
        return res
''',
    setup='''
_secret = 13
def commonSetBits(num):
    return bin(_secret & num).count('1')
''',
    call='Solution().findNumber()',
    expect=13,
    views=[
        dict(type='text', fn=lambda S: (f"隐藏的 n = `{bin(13)[2:]}`（二进制）　已猜出 res = `{bin(S['res'])[2:]}` = =={S['res']}==" if 'res' in S else ''), h=70),
        dict(type='text', fn=lambda S: (f"当前询问 v = `2^{S['index']}` = =={S['v']}==，commonSetBits(v) 返回 ==" + str(bin(13 & S['v']).count('1')) + '==' if 'index' in S and 'v' in S and S['v'] < 2 ** 31 else ''), h=70),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 用来拼出 n，初始 0',
        'v = 1': '`v` 是当前位的值，从 `2^0 = 1` 开始',
        'for index in range(30)': '题目保证 n 最多 30 位：逐位询问，当前第 `{index}` 位',
        'if commonSetBits(v)': lambda S, B, r: (f'`commonSetBits({S.v})` 返回 `{bin(13 & S.v).count("1")}`：' + ('n 在这一位是 1' if 13 & S.v else 'n 在这一位是 0')),
        'res += v': 'n 的这一位是 1 → 把 `2^{index}` 加进答案：`res` = =={res}==',
        'v += v': '`v` 翻倍，换到下一位：`v` = {v}',
        'return res': '30 位问完，`res = {res}` 就是 n',
    },
    cards=dict(
        one_liner='问 2 的幂：返回 1 说明 n 这一位是 1',
        complexity='时间 `O(30)` 次询问，空间 `O(1)`',
        problem=['有一个隐藏整数 n（最多 30 位），只能调用 `commonSetBits(num)`',
                 '它返回 n 与 num 二进制中同为 1 的位数',
                 '用它猜出 n。本例隐藏 `n = 13`'],
        quote='如果输入的num是2的幂次，就可以通过这个函数值是否为1来确定n在这一位上是否为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num = 2^k` 只有一个 1，返回值只能是 0 或 1',
              '返回 1 → n 的第 k 位是 1，把 `2^k` 加进 `res`',
              '从低位到高位问 30 次，n 就被完整还原'],
        summary=['询问 30 次，时间 `O(30)`，空间 `O(1)`',
                 '`v += v` 就是左移一位',
                 '题目的 `commonSetBits` 是交互接口，视频里在 `setup` 中用隐藏的 n=13 模拟',
                 '要点：用 2 的幂当探针，一次只探一位'],
    ),
)
