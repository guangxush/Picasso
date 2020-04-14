from pyquery import PyQuery as pq
import urllib.request


#  人民网新闻标题爬取
def handler():
    # 设置需要爬取的网站地址
    response = urllib.request.urlopen('http://politics.people.com.cn/')
    code = response.code
    # 打开当前路径下的news.txt文件，以追加的方式对信息进行存储
    fw = open('../learn/data/news.txt', 'a')
    if code == 200:
        # http请求返回200表示请求成功
        print("*****请求成功，开始爬虫*****")
        # 设置文本的编码方式为GBK编码
        content = response.read().decode('gbk')
        # print(content) # 打印网页的全部信息
        doc = pq(content)
        # 爬取10条新闻
        for i in range(1, 11):
            # 通过F12，查找要爬取信息的selector，通过观察我们将要爬取的10条信息的id传入selector中进行遍历爬取
            element = doc(
                'body > div.w1000.mt20.column_2.p9_con > div.left.w655 > div:nth-child(3) > div:nth-child({}) > div > h5 > a'.format(
                    i))
            # 获取新闻标题
            title = element.text()
            print(title)
            # 获取新闻链接
            link = element.attr('href')
            # 转入新闻详细信息页面
            detail_response = urllib.request.urlopen('http://politics.people.com.cn' + link)
            # 新闻信息编码为GBK
            detail_content = detail_response.read().decode('gbk')
            detail_doc = pq(detail_content)
            # 获取id为'#rwb_zw'的div，即正文，也可以通过selector进行选择,同时去掉新闻中的换行符，方便存储查看
            detail = detail_doc('#rwb_zw').text().replace("\n", "")
            print(detail)
            # fw.write(title + '@@@' + detail + "\n")
            fw.write(title + "\n")
    # 记得关闭文件
    fw.close()


if __name__ == '__main__':
    handler()
