
# -*- coding:utf-8 -*-
#!/usr/bin/env python

import argparse
import commands

#参数说明：
#-workspace JinRongProject.xcworkspace  #.xcworkspace文件名字
#-scheme WangCaiTarget   				#可以在项目目录下执行xcodebuild -list获取
#-configuration Debug    				#Debug 或者 Release
#-archivePath                           #生成.archive文件之后放在哪个路径
#CODE_SIGN_IDENTITY						#证书的的名字
#PROVISIONING_PROFILE_SPECIFIER			#描述文件的名字
#-exportPath							#导出.ipa文件要放在哪个路径
#-exportOptionsPlist                    #plist文件的路径

#==============================设置常量====================================
#下面关于list中的元素，在配置的时候顺序要对应
WORKSPACE_NAME="xxxxx.xcworkspace"
TARGETS=['target_name_1','target_name_2']
BUILD_CONFIGURATION= 'Debug'  #'Debug' 或者 Release
ARCHIVE_PATH='~/Desktop'
# =============================配置====================================
# plist文件可以通过手动打包一次获得，文件夹中会有生成的。
EXPORT_PLIST_PATH=['第一个 target 的 plist文件路径','第二个 target 的 plist文件路径']
BUILD_CODE_SIGN_IDENTITY=['第一个 target 的证书名字','第二个 target 的证书名字']
BUILD_PROVISIONING_PROFILE_SPECIFIER=['第一个 target 证书对应的描述文件','第二个 target 证书对应的描述文件']

#fir.im API Token
FIR_TOKEN="d79f68f0bxxxxxxxxxxx09ddf0c6985f65"
#app在fir.im的下载页面地址
TARGET_URL_ADDRESS=['第一个 target 在fir.im的下载页面地址','第二个 target 在fir.im的下载页面地址']  
#target在list中的索引
INDEX=0

#=========================================================================

#输出
def statusLog(logString):
	print "+---------------------------------------------------------------------------------+"
	print "|                                                                                 |"
	print "                               %s                                                  " %(logString)
	print "|                                                                                 |"
	print "+---------------------------------------------------------------------------------+"

#打开网页
def openUrl():
	openUrlCmd = 'open %s' %(TARGET_URL_ADDRESS[INDEX])
	print "---> 打开网页命令：%s" %(openUrlCmd)
	(status, output) = commands.getstatusoutput(openUrlCmd)
	if status == 0:
		statusLog('网页已经打开，可以去获取二维码了!')
	else:
		statusLog('打开网页失败，自己手动去打开吧!')
		
#上传
def uploadToFirm(scheme):
	ipaPath = "%s/%sIPA/%s.ipa" %(ARCHIVE_PATH,scheme,scheme)
	uploadCmd = 'fir p %s -T %s' %(ipaPath,FIR_TOKEN)
	print "---> fir上传命令：%s" %(uploadCmd)
	statusLog('正在上传中,先让代码飞一会~~~')
	(status, output) = commands.getstatusoutput(uploadCmd)
	if status == 0:
		statusLog('上传成功！')
		openUrl()
		clearArchive(scheme)
	else:
		print status, output
		statusLog('上传失败！')

#删除archive包和ipa包（上传完成之后才可调用）
def clearArchive(scheme):
	xcarchivePath='%s/%s.xcarchive' %(ARCHIVE_PATH,scheme)
	ipaPath='%s/%sIPA' %(ARCHIVE_PATH,scheme)
	clearCmd = 'rm -r %s %s' %(xcarchivePath,ipaPath) 
	print "---> 删除.xcarchive、ipa命令：%s" %(clearCmd)
	(status, output) = commands.getstatusoutput(clearCmd)
	if status == 0:
		statusLog('删除.xcarchive、ipa文件成功')
	else:
		print status, output
		statusLog('删除.xcarchive、ipa文件失败')


#导出
def exportArchive(scheme):
	exportCmd = "xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%sIPA -exportOptionsPlist %s CODE_SIGN_IDENTITY='%s' PROVISIONING_PROFILE_SPECIFIER='%s'" %(ARCHIVE_PATH,scheme,ARCHIVE_PATH,scheme,EXPORT_PLIST_PATH[INDEX],BUILD_CODE_SIGN_IDENTITY[INDEX],BUILD_PROVISIONING_PROFILE_SPECIFIER[INDEX])
	print "---> 导出命令：%s" %(exportCmd)
	statusLog('正在导出中,先让代码飞一会~~~')
	(status, output) = commands.getstatusoutput(exportCmd)
	if status == 0:
		uploadToFirm(scheme)
	else:
		print status, output
		statusLog('导出失败!')

#打包
def archiveWorkspace(workspace, scheme):
	archiveCmd = "xcodebuild archive -workspace %s -configuration %s -scheme %s -archivePath %s/%s.xcarchive CODE_SIGN_IDENTITY='%s' PROVISIONING_PROFILE_SPECIFIER='%s'" %(workspace,BUILD_CONFIGURATION,scheme,ARCHIVE_PATH,scheme,BUILD_CODE_SIGN_IDENTITY[INDEX],BUILD_PROVISIONING_PROFILE_SPECIFIER[INDEX])
	print "---> 打包命令：%s" %(archiveCmd)
	statusLog('正在打包中,先让代码飞一会~~~')
	(status, output) = commands.getstatusoutput(archiveCmd)
	#print status, output
	if status == 0:
		exportArchive(scheme)
	else:
		print status, output
		statusLog('打包失败')	

def xcbuild(options):
	workspace=WORKSPACE_NAME
	global INDEX
	INDEX=TARGETS.index(options.scheme)
	scheme=options.scheme
	if workspace is not None and scheme is not None:
		archiveWorkspace(workspace, scheme)
	else:
		statusLog('请先配置workspace、scheme信息')	
		
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--scheme", help="scheme name")
	options = parser.parse_args()
	print "options: %s" %(options)
	xcbuild(options)
	
if __name__ == '__main__':
	main()

