#!/bin/bash
 source /etc/profile
#cd `dirname $0`
#echo  `dirname $0`

#keystore文件路径
if [ $1 == "assembleDebug" ];then
        jks=/opt/debug.keystore
	storePassword="123456"
    	keyAlias="yangzc"
    	keyPassword="123456"
else
        jks=/opt/release_t.keystore
	storePassword="wb123456"
        keyAlias="workbox"
    	keyPassword="wb123456"
fi

#打包输出的地址
apks=${WORKSPACE}/build/outputs/apk/

#加固后的地址
#outs=${WORKSPACE}/build/outs
outs=/opt/360jiagu/build/outs/${JOB_NAME}


rm -fr ${outs}/*

#加固包地址
jar_path='/opt/android/360jiagu/jiagu/jiagu.jar'


echo "==========输出配置信息=========="
echo ${jks}
echo "打包输出地址："${apks}
echo "加固后包地址："${outs}
echo ${jar_path}
echo ${storePassword}
echo ${keyAlias}
echo ${keyPassword}

if [ ! -d ${outs}  ]; then
      mkdir ${outs}
fi


#echo "签名"
#ls ${apks}
#渠道列表文件
if [ $1 == "assembleDebug" ];then
         CHANNELS_FILE_PATH="/opt/android/360jiagu/jiagu/packer-ng-reinforce/channel_jiagu.txt"
else
        CHANNELS_FILE_PATH=${WORKSPACE}/release/channel_jiagu.txt
fi

#CHANNELS_FILE_PATH=${WORKSPACE}/release/channel_jiagu.txt
echo ${CHANNELS_FILE_PATH}
#cat ${CHANNELS_FILE_PATH}

/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -login 13811191507 haizj0216

/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -importsign ${jks} ${storePassword} ${keyAlias} ${keyPassword}

/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -deletemulpkg

/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -importmulpkg ${CHANNELS_FILE_PATH}


/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -showmulpkg

#/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -importsign ${jks} wb123456 workbox wb123456

/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -config  -crashlog

for file_a in ${apks}/*release.apk
    do
        echo "test"
        temp_file=`basename $file_a`
        echo ${temp_file}
        #/opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -jiagu $apks/$temp_file $outs -autosign -automulpkg
        /opt/jdk/jdk1.8.0_261/bin/java -jar ${jar_path} -jiagu $apks/$temp_file $outs -autosign -automulpkg
    done
echo "打包"
ls ${outs}



