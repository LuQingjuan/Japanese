#!/bin/bash

File='justtest.md'

Help(){
    echo "Add:        tool.sh -a "
    echo "Search:     tool.sh -s "
    echo "Change:     tool.sh -c "
    echo "Command:    tool.sh -m "
}

Add()
{
    echo $1 >>$File
}

Search()
{
    arr=($1)
    echo $arr[@]
    for code in $arr[@]
    do
        echo $code
    done
}

Update()
{

}

mode=''
param=''

mode=$arg[1]

for arg in $*
do
    echo "arg: $index = $arg"
    param="$param $arg"
    fi
done

if [ '-a' == $mode ];then
    Add "$param"
elif [ '-s' == $mode ];then
    echo $param
    Search "$param"
fi