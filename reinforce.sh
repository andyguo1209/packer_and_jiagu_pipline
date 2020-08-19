#!/bin/bash
source /etc/profile
export PATH=/bin:/usr/bin:$PATH
#source packer.config
#@加固后apk文件路径
#INPUT_APK_PATH=/data/apks/v1.0.1/360_101_jiagu_sign.apk
#加固后的地址
OUTS=/data/360jiagu/build/outs/${JOB_NAME}
ls  ${OUTS}
for file_a in ${OUTS}/*.apk; do
    FILE_NAME=`basename $file_a`
    echo $FILE_NAME
done

INPUT_APK_PATH=${OUTS}/${FILE_NAME}
#keystore文件路径
KEYSTORE_PATH=${WORKSPACE}/haigui.jks

#keystore密码，建议加上引号，否则无法读取到特殊符号
KEYSTORE_PASSWORD='12345'

#keystore alias名
KEYSTORE_ALIAS=123456

#keystore alias密码，建议加上引号，否则无法读取到特殊符号
KEYSTORE_ALIAS_PASSWORD='123456'

#渠道列表文件
CHANNELS_FILE_PATH=${WORKSPACE}/markets.txt

echo "==========输出配置信息=========="
echo $INPUT_APK_PATH
echo $KEYSTORE_PATH
echo $KEYSTORE_PASSWORD
echo $KEYSTORE_ALIAS
echo $KEYSTORE_ALIAS_PASSWORD
echo $CHANNELS_FILE_PATH

output_dir="/data/360jiagu/jiagu/packer-ng-reinforce/build/output/${JOB_NAME}"
building_dir="/data/360jiagu/jiagu/packer-ng-reinforce/build/packing/${JOB_NAME}"

rm -rf ${output_dir}
rm -fr ${building_dir}

mkdir -p $output_dir
mkdir -p $building_dir

#NFILE_NAM= $( echo $FILE_NAME |sed "s/${channels}//g")

CHANN=${channels}"_*.*_"
NFILE_NAME=`echo $FILE_NAME |sed "s/${CHANN}//g" `
echo "新包名:"${NFILE_NAME}

ZIPALIGN_FILE_PATH="${output_dir}/zipalign.apk"
APKSIGNER_FILE_PATH="${building_dir}/${NFILE_NAME}"

echo $ZIPALIGN_FILE_PATH
echo $APKSIGNER_FILE_PATH


echo "==========开始zip对齐=========="
#zip对齐
echo $INPUT_APK_PATH
/data/360jiagu/jiagu/packer-ng-reinforce/src/zipalign -v -p 4 $INPUT_APK_PATH $ZIPALIGN_FILE_PATH
echo "==========开始v2签名=========="
#v2签名
/data/360jiagu/jiagu/packer-ng-reinforce/src/apksigner sign  --ks $KEYSTORE_PATH --ks-key-alias $KEYSTORE_ALIAS --ks-pass pass:"$KEYSTORE_PASSWORD" --key-pass pass:"$KEYSTORE_ALIAS_PASSWORD"  --out $APKSIGNER_FILE_PATH  $ZIPALIGN_FILE_PATH
echo "==========开始验证签名=========="
#验证签名是否已添加
/data/360jiagu/jiagu/packer-ng-reinforce/src/apksigner verify -v $APKSIGNER_FILE_PATH
echo "==========开始添加渠道信息=========="
#添加渠道包
/usr/java/jdk1.8.0_25/bin/java -jar /data/360jiagu/jiagu/packer-ng-reinforce/src/packer-ng-2.0.0.jar generate --channels=@$CHANNELS_FILE_PATH --output=$output_dir $APKSIGNER_FILE_PATH
echo "==========开始验证渠道是否已添加=========="
#循环遍历验证所有渠道包是否添加正确
for file in ${output_dir}/*; do
    echo "文件路径：$file"
    #验证渠道是否已添加
    /usr/java/jdk1.8.0_25/bin/java -jar  /data/360jiagu/jiagu/packer-ng-reinforce/src/packer-ng-2.0.0.jar verify $file
done



