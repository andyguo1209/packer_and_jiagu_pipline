#!/usr/bin/python

import os
import os.path
import md5
import zipfile
import shutil
import commands

src_apk = commands.getoutput('find ./build/outputs/apk -name ' + "*knowbox_release.apk")
#name of rootApk
src_apk_name = "AndroidRCStudent_" + src_apk.split("_")[1]
#channel list
channelFile = "release/channel.txt"
#path of rootApk
#src_apk = "build/outputs/apk/AndroidRCStudent" + apk_version + "-release.apk"
#output Folder
#output_dir = "/Users/weilongzhang/Desktop/releaseChannel/"
output_dir = "./build/outputs/apk/fullchannel/"

#do MD5
def doMd5(src):
	m1 = md5.new()
	m1.update(src)
	return m1.hexdigest()

#read zip File
def readZipFile(filePath, fileName):
	z = zipfile.ZipFile(filePath, "r");
	return z.read(fileName)

#append file to zip
def appendZipFile(filePath, path, zipPath):
	z = zipfile.ZipFile(filePath, 'a', zipfile.ZIP_DEFLATED)
	z.write(path, zipPath)

#doSafe
def doSafe(filePath, channelName):
	manifest = readZipFile(filePath, "META-INF/MANIFEST.MF")
	cert = readZipFile(filePath, "META-INF/CERT.SF")
	#fotmat[channel:sign]
	data = channelName + "=" + doMd5(manifest) + doMd5(cert)
	#tempFile path
	tmpFile = output_dir + "/data"
	if os.path.exists(tmpFile) and os.path.isfile(tmpFile):
		os.remove(tmpFile)

	fobj = open(tmpFile, "w");
	fobj.write(data);
	fobj.close();

	appendZipFile(filePath, tmpFile, "META-INF/chs.dis")

#Clear Folder
def clearFolder(dirPath):
	filelist=os.listdir(dirPath)
	for f in filelist:
		filepath = os.path.join(dirPath, f)
		if os.path.isfile(filepath):
			os.remove(filepath)
		elif os.path.isdir(filepath):
			shutil.rmtree(filepath,True)

#release
def doRelease():
	print("==========================================")
	print("start release jobs")
	if not os.path.exists(src_apk) or not os.path.isfile(src_apk):
		print("rootApk is not exists !!!")
		return

	#check output Folder
	if os.path.exists(output_dir) and os.path.isdir(output_dir):
		clearFolder(output_dir)

	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	f = open(channelFile)
	lines = f.readlines()
	f.close()
	for line in lines:
		target_channel = line.strip()
		target_apk = output_dir + src_apk_name + "-" + target_channel + "-release.apk"
		shutil.copy(src_apk,  target_apk)
		#doSafe
		doSafe(target_apk, target_channel)
		print "doSafe: " + target_apk

def zip_dir(dirname, zipfilename):
    filelist = []
    #Check input ...
    fulldirname = os.path.abspath(dirname)
    fullzipfilename = os.path.abspath(zipfilename)
    print "Start to zip %s to %s ..." % (fulldirname, fullzipfilename)
    if not os.path.exists(fulldirname):
        print "Dir/File %s is not exist, Press any key to quit..." % fulldirname
        inputStr = raw_input()
        return
    if os.path.isdir(fullzipfilename):
        tmpbasename = os.path.basename(dirname)
        fullzipfilename = os.path.normpath(os.path.join(fullzipfilename, tmpbasename))
    if os.path.exists(fullzipfilename):
        print "%s has already exist, are you sure to modify it ? [Y/N]" % fullzipfilename
        while 1:
            inputStr = raw_input()
            if inputStr == "N" or inputStr == "n" :
                return
            else:
                if inputStr == "Y" or inputStr == "y" :
                    print "Continue to zip files..."
                    break

    #Get file(s) to zip ...
    if os.path.isfile(dirname):
        filelist.append(dirname)
        dirname = os.path.dirname(dirname)
    else:
        #get all file in directory
        for root, dirlist, files in os.walk(dirname):
            for filename in files:
                filelist.append(os.path.join(root,filename))

    #Start to zip file ...
    destZip = zipfile.ZipFile(fullzipfilename, "w", allowZip64=True)
    for eachfile in filelist:
        destfile = eachfile[len(dirname):]
        print "Zip file %s..." % destfile
        destZip.write(eachfile, destfile)
    destZip.close()

#doRelease
doRelease()
zip_dir(output_dir, "./build/outputs/apk/fullchannel.zip")
#clearFolder(output_dir)

# print doMd5('hello world')
# print readZipFile(os.path.join(rootDir, 'AndroidRCStudent-xiaomi-debug.apk'), "META-INF/MANIFEST.MF")
# print readZipFile(os.path.join(rootDir, 'AndroidRCStudent-xiaomi-debug.apk'), "META-INF/CERT.SF")
# appendZipFile(os.path.join(rootDir, 'AndroidRCStudent-xiaomi-debug.apk'), '/Users/yangzc/Desktop/bbbb.txt', 'META-INF/bbb.txt')

#walk files

