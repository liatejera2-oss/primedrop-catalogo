from pathlib import Path
import re

source_path = Path('.github/scripts/patch_point9.py')
source = source_path.read_text(encoding='utf-8')

replacement = r'''msg_pattern = re.compile(r"(`Producto: \$\{row\.product_name\}\\n` \+\s*\n\s*)(`Talla: \$\{row\.size\}\\n` \+)")
if not msg_pattern.search(index):
    raise SystemExit('message anchor missing')
index = msg_pattern.sub(r"\1(row.color ? `Color: ${row.color}\\n` : '') +\n        \2", index, count=1)
'''

source, count = re.subn(
    r'old_msg = """.*?if old_msg not in index: raise SystemExit\(\'message anchor missing\'\)\nindex = index\.replace\(old_msg, new_msg, 1\)\n',
    lambda m: replacement,
    source,
    count=1,
    flags=re.S
)
if count != 1:
    raise SystemExit('Could not repair Point 9 message patch block')

exec(compile(source, str(source_path), 'exec'))
