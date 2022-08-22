
### ffff <span id=2_1>[例子](tmp_j.md#2_1)</span>
---
<span id=([^>]+)>([^<]+)</span>
$2 #$1

\[([^\]]+)\]\(([^#]+)#([^\)]+)\)
[[ $2 | $1 #$3 ]]


---
<details><summary>[\n]*(\d+)\.([^<]+)</summary>\n
$1. **$2**

---
\n</details>\n\n([\d#\*\.]+)

$1
---



      // 标注
      // [name]^(detail)  =>  <ruby>name<rp>(</rp><rt>detail</rt><rp>)</rp></ruby>
      markdown = markdown.replace(/\[([^\[\]]+)\]\^\(([^\(\)]+)\)/gm, "<ruby>$1<rp>(</rp><rt>$2</rt><rp>)</rp></ruby>");

      //[[ ../Menu.md | Home #aaa ]]  =>  [Home](../Menu.md#aaa)
      markdown = markdown.replace(/\[\[ ([^ ]+) \| ([^ ]+) #([^ ]+) \]\]/gm, "[$2]($1#$3)");
      //# 课文 #aaaa  =>  # <span id=aaaa>课文</span>
      markdown = markdown.replace(/^(#+) ([^#\r\n]+) #([^\r\n]+)/gm, "$1 <span id=$3>$2</span>");
      //[[ ../Menu.md | Home ]]  =>  [Home](../Menu.md)
      markdown = markdown.replace(/\[\[ ([^ ]+) \| ([^ ]+) \]\]/gm, "[$2]($1)");