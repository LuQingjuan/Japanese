#!/bin/bash
#20220817
#./allinone.sh ../Remember/Dialogue/19.md ../Remember/Dialogue/20.md ../Remember/Dialogue/syumi_o_tazuneru.md ../Test/Reading/ka_o_mo_ji_1.md ../Test/Reading/ka_o_mo_ji_2.md ../Test/Reading/tomomi_no_ni_kki.md ../Test/Reading/t_ka_mi_no_te_tyou.md ../Test/Reading/t_ya_ki_ya.md

result=`date '+%Y%m%d'`
rm -rf $result tmp_tanngo.txt
mkdir $result
for arg in "$@"
do
   #与/之间与分割的字符 ，另外/后有一个空格不可省略
   arr=(${arg//\// });
   name=${arr[${#arr[@]}-1]}
   echo $name

   rm AnnotateSentence.md Markdown.md
   echo arg >> tmp_tanngo.txt
   python3 ./tool.py -a $arg
   python3 ./tool.py -m AnnotateSentence.md
   echo "[$arg]($arg)" >> $result"/all_in_one.md"
   mv AnnotateSentence.md $result"/vs_"$name
   mv Markdown.md $result"/mk_"$name
done

mv tmp_tanngo.txt $result

