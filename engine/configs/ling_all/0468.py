CONFIG = dict(
    num=468, title='验证IP地址', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='标准库解析 + 特判前导零（Go 原文转写）',
    tags=[],
    setup='''
import re
import types
import ipaddress


class _IP:
    def __init__(self, v4):
        self.v4 = v4

    def To4(self):
        return self if self.v4 else None


def _parse_ip(s):
    # 等价于 Go 的 net.ParseIP：合法返回 IP 对象，否则 None；IPv4 允许前导零
    m = re.fullmatch(r'(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})', s)
    if m:
        return _IP(True) if all(int(g) <= 255 for g in m.groups()) else None
    try:
        a = ipaddress.IPv6Address(s)
    except ValueError:
        return None
    return _IP(a.ipv4_mapped is not None)


net = types.SimpleNamespace(ParseIP=_parse_ip)
''',
    code='''
class Solution:
    def validIPAddress(self, queryIP: str) -> str:
        ip = net.ParseIP(queryIP)
        if ip is None:
            return "Neither"
        if ip.To4() is not None:
            for s in queryIP.split("."):
                if len(s) > 1 and s[0] == '0':
                    return "Neither"
            return "IPv4"
        for s in queryIP.split(":"):
            if len(s) > 4 or s == "":
                return "Neither"
        return "IPv6"
''',
    call='Solution().validIPAddress("192.168.01.1")',
    expect='Neither',
    views=[
        dict(type='text', fn=lambda S: '`queryIP = "%s"`' % S['queryIP'] if 'queryIP' in S else '', size=36, h=70),
        dict(type='text', fn=lambda S: ('`net.ParseIP` ==%s==' % ('失败，不是合法 IP' if S['ip'] is None else ('成功：IPv4 地址' if S['ip'].To4() is not None else '成功：IPv6 地址'))) if 'ip' in S else '', size=34, h=70),
        dict(type='array', var=lambda S: S['queryIP'].split('.' if S['ip'] is not None and S['ip'].To4() is not None else ':') if 'ip' in S and S['ip'] is not None else [],
             label='按分隔符切开的每一段 s', h=170,
             color=lambda S, i, v: (None if v != S.get('s') else 'red' if ((len(v) > 1 and v[0] == '0') or len(v) > 4 or v == '') else 'blue')),
    ],
    watch=[('s', 's', 'blue'), ('len(s)', 'len(s)', 'pink')],
    captions={
        'ip = net.ParseIP': lambda S, B, r: ('`net.ParseIP` 解析失败 → 肯定不是 IP' if S.ip is None else '`net.ParseIP` 解析成功，但它允许 IPv4 里的前导零，所以后面还要自己检查'),
        'if ip is None': lambda S, B, r: ('解析失败，直接 `Neither`' if S.ip is None else '解析成功，继续判断是 IPv4 还是 IPv6'),
        'ip.To4()': lambda S, B, r: ('能转成 4 字节 → 是 ==IPv4==，按 `.` 切开逐段检查前导零' if S.ip.To4() is not None else '转不成 4 字节 → 是 ==IPv6==，按 `:` 切开逐段检查'),
        'for s in queryIP.split(".")': '取出一段 `s = "{s}"`',
        'len(s) > 1 and s[0]': lambda S, B, r: (f'`"{S.s}"` 长度 {len(S.s)} 且以 `0` 开头 → ==前导零==，不合法' if len(S.s) > 1 and S.s[0] == '0' else f'`"{S.s}"` 没有前导零，继续看下一段'),
        'len(s) > 4 or s ==': lambda S, B, r: ('长度超过 4 或者是空段 → 不合法' if (len(S.s) > 4 or S.s == '') else f'`"{S.s}"` 长度 {len(S.s)}（1~4）且非空，合法'),
        'for s in queryIP.split(":")': '取出一段 `s = "{s}"`',
        'return "IPv4"': '每段都没有前导零 → ==IPv4==',
        'return "IPv6"': '每段长度都在 1~4 → ==IPv6==',
        'return "Neither"': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='交给标准库判断合法性，只补上它漏掉的情况',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断 `queryIP` 是合法 IPv4、合法 IPv6，还是都不是',
                 'IPv4：四段 `0~255`，不能有前导零；IPv6：八段十六进制，每段 1~4 位',
                 '本视频：`"192.168.01.1"` → `"Neither"`（第三段 `01` 有前导零）'],
        quote='虽说有 net.ParseIP 这样的利器，但该函数是允许前导零的，所以仍然要特判一下。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先 `ParseIP`：解析失败一定是 `Neither`',
              '`To4()` 不为空说明是 IPv4，补查每段有没有前导零',
              '否则是 IPv6，补查每段是否为空（`::` 缩写）或超过 4 位'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Python 没有 `net.ParseIP`，在 setup 里补了等价实现（IPv4 允许前导零，IPv6 用 `ipaddress`），作者代码未改',
                 '时间 `O(n)`，空间 `O(n)`（切分后的子串）',
                 '易错点：`ParseIP` 允许 IPv4 前导零、也允许 `::` 缩写，题目都不允许，所以要特判',
                 '`len(s) > 1 and s[0] == "0"`：单独的 `0` 是合法的'],
    ),
)
