CONFIG = dict(
    num=3602, title='十六进制和三十六进制转化', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 b 除以 b · 手写进制转换',
    tags=[],
    code='''
class Solution(object):
    def concatHex36(self, n):
        
        def trans(x, base):
            res = []
            while x:
                res.append(x % base)
                x //= base
            
            res.reverse()
            return [str(v) if 0 <= v <= 9 else chr(v + 55) for v in res]
        
        return ''.join(trans(n * n, 16) + trans(n * n * n, 36))
''',
    call='Solution().concatHex36(13)',
    expect='A91P1',
    views=[
        dict(type='text', size=30, h=110, fn=lambda S: (
            f"把 `x = {S['x']}` 转成 `{S['base']}` 进制" if 'base' in S and 'x' in S else '`n = 13`：`n² = 169` 转 16 进制，`n³ = 2197` 转 36 进制')),
        dict(type='array', var='res', label='res（先存数位，低位在前，最后反转）', cell=90, h=200,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 and S['_line'] in (8, 9) else None),
        dict(type='text', size=28, h=110, fn=lambda S: (
            f"数位 >= 10 用字母：`chr(v + 55)`，例如 `10 → 'A'`，`25 → 'P'`" if S.get('_line') == 12 else '')),
    ],
    watch=[('x', 'x', 'blue'), ('base', 'base', 'pink'), ('n', 'n')],
    captions={
        'res = []': '`res` 存各个数位，先得到的是==最低位==',
        'while x': lambda S, B, r: (f'`x = {S.x}` 不为 0，继续取数位' if S.x else '`x = 0`：所有数位都取完了'),
        'res.append(x % base)': '最低位 `x % base = {res[-1]}`（`x` 除以 `{base}` 的余数）',
        'x //= base': '去掉最低位：`x //= {base}` → {x}',
        'res.reverse()': '先取出的是低位，反转后高位在前：`{res}`',
        'return [str(v)': lambda S, B, r: f'数位 0~9 直接转成字符，≥ 10 用 `chr(v + 55)` 转成 `A`~`Z`（`chr(65)` = `A`）→ `{r}`',
        "return ''.join": lambda S, B, r: f'把两段数位拼接：`{r}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='模 b 取最低位，除以 b 去掉它，反转就是 b 进制',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['返回 `n²` 的==十六进制==（`A~F` 表示 10~15）与 `n³` 的==三十六进制==（`A~Z` 表示 10~35）拼接成的字符串',
                 '本视频：`n = 13` → `169 = "A9"`，`2197 = "1P1"` → `"A91P1"`'],
        quote='常规的进制转化问题，直接使用模b除以b的方法计算转换后的数位，反转后即为对应的b进制数。需要注意要将大于等于10的数位转换为字母。',
        quote_src='—— yiduobo 题解原文',
        idea=['`x % base` 是最低位，`x //= base` 去掉最低位，循环到 `x = 0`',
              '得到的数位低位在前，`reverse()` 后才是 b 进制写法',
              '数位 ≥ 10 要换成字母：`chr(v + 55)`，因为 `chr(65) = "A"` 对应 10',
              '写成函数 `trans(x, base)`，十六进制和三十六进制各调用一次'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '易错：转字母时偏移是 55（`65 - 10`），不是 65',
                 '`n ≥ 1` 所以 `x` 不会是 0；若 `x = 0`，循环不执行，会得到空串',
                 '原文已是 Python 3 可运行写法，`x //= base` 本来就是整除，没有修改',
                 '对比灵神：灵神直接用 `np.base_repr` 库函数，一行完成'],
    ),
)
