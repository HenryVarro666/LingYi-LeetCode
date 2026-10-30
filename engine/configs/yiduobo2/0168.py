N = 1354


def _eq(S, B):
    ln = S.get('_line')
    if ln == 5 and 'tmp' in S:
        return f'`{B["n"]}` = {B["n"] // 26} × 26 + =={S["tmp"]}=='
    if ln in (6, 7, 8, 9) and 'tmp' in S:
        return f'余数 `tmp = {S["tmp"]}`，商 `n = {S["n"]}`'
    if ln == 10:
        return f"`chr({S['tmp']} + 64)` = `'{chr(S['tmp'] + 64)}'`（`A` 的 ASCII 是 65）"
    return f'`n = {S.get("n")}`'


def _res_cells(S):
    r = S.get('res')
    return list(r) if r is not None else None


def _cap_while(S, B, ret):
    if B['n']:
        return f'`n = {B["n"]}` 还没除完 → 取下一位（从==最低位==开始）'
    return '`n = 0`：所有位都取完了'


def _cap_mod(S, B, ret):
    if S.tmp:
        return f'`{B.n} % 26 = {S.tmp}` → 这一位是第 `{S.tmp}` 个字母 `{chr(S.tmp + 64)}`'
    return f'`{B.n} % 26 = 0`：但 A~Z 对应 ==1~26==，没有 0 → 这一位其实是 `Z`，要特判'


def _cap_div(S, B, ret):
    return f'整除去掉最低位：`n = {B.n} // 26 = {S.n}`'


def _cap_if(S, B, ret):
    if not S.tmp:
        return '余数为 0 → 进入特判'
    return f'余数 `{S.tmp}` 不为 0，正常转换'


CONFIG = dict(
    num=168, title='Excel表列名称', difficulty='Easy', category='数学',
    author='yiduobo', technique='26 进制转换 · 特判余数 0',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def convertToTitle(self, n):
        res = ''
        while n:
            tmp = n % 26
            n //= 26
            if not tmp:
                n -= 1
                tmp = 26
            res = chr(tmp + 64) + res

        return res
''',
    call=f'Solution().convertToTitle({N})',
    expect='AZB',
    views=[
        dict(type='text', fn=lambda S: '`A`~`Z` ↔ `1`~`26`：本质是==26 进制==，但每一位的范围是 1~26 而不是 0~25', size=26, h=70),
        dict(type='text', fn=_eq, h=80),
        dict(type='string', var=_res_cells, label='res（新的一位拼在最前面）', cell=96, h=230,
             color=lambda S, i, v: 'green' if S.get('_line') == 10 and i == 0 else None),
        dict(type='text', fn=lambda S: ('验算：`AZB` = 1×26² + 26×26 + 2 = 676 + 676 + 2 = ==1354==' if S.get('res') == 'AZB' else ''),
             h=70),
    ],
    watch=[('n', 'n', 'blue'), ('tmp', 'tmp', 'orange'), ('res', 'res', 'green')],
    captions={
        "res = ''": '`res` 从空串开始，==从低位到高位==逐位往前拼',
        'while n:': _cap_while,
        'tmp = n % 26': _cap_mod,
        'n //= 26': _cap_div,
        'if not tmp': _cap_if,
        'n -= 1': '这一位用 `Z`（26）表示 = 从高位==借 1==：`n` 减 1 → `{n}`',
        'tmp = 26': '`tmp = 26`，对应 `Z`',
        'res = chr(': "`chr({tmp} + 64) = '{res[0]}'`，拼到最前面 → `res = '{res}'`",
        'return res': "返回 =={ret}==",
    },
    max_steps=40,
    cards=dict(
        one_liner='26 进制，但每一位是 1~26：余数为 0 时借一位当 Z',
        complexity='时间 `O(log₂₆ n)`，空间 `O(1)`（不计答案）',
        problem=['给整数 `columnNumber`，返回它在 Excel 表中对应的列名称',
                 '`1 → A`，`2 → B`，…，`26 → Z`，`27 → AA`，`28 → AB`，…',
                 '示例：`28 → "AB"`，`701 → "ZY"`',
                 '本视频：`1354 → "AZB"`（中间那位余数为 0）'],
        quote='其实本质上就是==整数的二十六进制表示==。这里需要注意的一点是，列A到列Z是取1到26，但是正常的二十六进制是0到25，所以在转换时需要特别判断==模26等于0==的情况。',
        quote_src='—— yiduobo 知乎题解',
        idea=['每次 `n % 26` 取最低位，`n //= 26` 去掉最低位，新字母拼在最前面',
              '余数为 0 时，这一位应是 `Z`（26），相当于从商里==借 1==：`n -= 1`',
              '`chr(余数 + 64)` 把 1~26 映射到 `A`~`Z`'],
        summary=['时间 `O(log₂₆ n)`：每轮去掉一位',
                 '原文为 Python 2 写法：`n /= 26` 是整除，已改为 `n //= 26`；另删去类型说明文档字符串',
                 '易错：忘记特判余数 0，`26` 会被转成 `A@`',
                 '另一种写法：先 `n -= 1` 再 `n % 26`，余数就落在 0~25，无需特判',
                 '反过来的题：171 Excel 表列序号'],
    ),
)
