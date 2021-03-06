import os
from Duplicate_removal import Duplicate_removal
from concurrent.futures import ThreadPoolExecutor
import hashlib

class Sqlmap_batch_scan():

    def __init__(self):
        self.sqlmap_ok_url = []
        self.sqlmap_flase_url = []

    def run_sqlmap(self,sqlmap_url,url_name):
        print(f"[+]>>>正在测试URL:{sqlmap_url}")
        new_url_name = hashlib.md5(url_name.encode("utf-8")).hexdigest()
        #存放报告的路径
        report_path = 'E:/python/HACK/Sqlmap批量扫描/ok_url/'
        os_command = r'sqlmap.py -u "{}" --batch > "{}{}.txt"'.format(sqlmap_url,report_path,new_url_name)
        os.system(os_command)
        # print(f'[+]>>>已生成报告:{new_url_name}.txt')
        judge_file = open('./ok_url/'+new_url_name+'.txt')
        judge_file_text = judge_file.readlines()
        if "Payload" in str(judge_file_text):
            judge_file.close()
            fp = open('./ok_url/'+new_url_name+'.txt','a+')
            fp.write('\n'+'测试url:'+sqlmap_url+' \n')
            fp.close()
            print(f'[*]>>>已验证成功URL:{sqlmap_url}')
            self.sqlmap_ok_url.append(sqlmap_url)

        else:
            judge_file.close()
            os.remove('./ok_url/'+new_url_name+'.txt')
            print(f'[!]>>>未验证成功URL:{sqlmap_url}')
            self.sqlmap_flase_url.append(sqlmap_url)

    def storage_url(self):
        sqlmap_ok_url_file = open('./sqlmap_ok_url.txt','a+')
        sqlmap_flase_url_file = open('./sqlmap_flase_url.txt','a+')
        for ok_urls in self.sqlmap_ok_url:
            ok_url = ok_urls.strip()
            sqlmap_ok_url_file.write(ok_url+'\n')
        for flase_urls in self.sqlmap_flase_url:
            flase_url = flase_urls.strip()
            sqlmap_flase_url_file.write(flase_url+'\n')
        print('[*]>>>链接存储完成！！')

    def run(self,sqlmap_url,url_name):
        self.run_sqlmap(sqlmap_url,url_name)
        self.storage_url()

if __name__ == '__main__':
    sqlmap_batch_scan = Sqlmap_batch_scan()
    #线程池数量
    sqlmap_pool = ThreadPoolExecutor(5)
    sqlmap_file = open('./sqlmap_url.txt','r')
    sqlmap_urls = sqlmap_file.readlines()
    for url in sqlmap_urls:
        sqlmap_url = url.strip()
        if sqlmap_url == '':
            continue
        else:
            url_name = sqlmap_url
            sqlmap_pool.submit(sqlmap_batch_scan.run, sqlmap_url, url_name)
    sqlmap_file.close()
    sqlmap_pool.shutdown()
    print('[*]>>>所有URL验证完毕!!')
    duplicate_removal = Duplicate_removal()
    duplicate_removal.run()

