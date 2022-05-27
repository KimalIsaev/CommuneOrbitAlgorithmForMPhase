ceildiv() {
	echo "$1 $2" | awk '{print int( ($1/$2) + 1 )}'
}

parent_dir=$(dirname $0) 
r_dir=$parent_dir/r
a_dir=$parent_dir/a
b_dir=$parent_dir/b
p_dir=$parent_dir/p

mkdir -p $r_dir $a_dir $b_dir $p_dir 

algorithm=$1
draw_script=$2
sigma=$3
param_file=$4

percision=0.0005
subdivisions=$(ceildiv $sigma $percision)

time=$(date +"%d:%m:%Y_%H:%M:%S")
i=0
while read line
do
    if [ -z "${line}" ]; then
        exit 0
    fi;
	name=$(basename $param_file .csv)'_'$i'_'$time
	python3 $algorithm $r_dir/$name.txt $a_dir/$name.txt \
        $b_dir/$name.txt $p_dir/$name.txt $sigma $subdivisions $line
	python3 $draw_script $r_dir/$name.txt $r_dir/$name.png $percision
	python3 $draw_script $a_dir/$name.txt $a_dir/$name.png $percision
	python3 $draw_script $b_dir/$name.txt $b_dir/$name.png $percision
	python3 $draw_script $p_dir/$name.txt $p_dir/$name.png
	export i=$(($i+1))
	echo $name
done < $param_file

