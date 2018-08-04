import requests
from pyquery import PyQuery as pq 
from lxml import etree
import codecs
import csv
url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/399812.phtml?qq-pf-to=pcqq.c2c"
head ='http://vip.stock.finance.sina.com.cn/corp/view/vFD_FinancialGuideLineHistory.php?stockid='
tail ='&typecode=financialratios21'
headers ={
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	'cookie':'pgv_pvid=370520813; pgv_pvi=8700964864; pt2gguin=o1303377145; RK=30LxDzcxdX; ptcz=dea6abc11642f7a071623d74c6935b8d1f76df296898e63578b7a6a629732611; __Q_w_s_hat_seed=1; __Q_w_s__QZN_TodoMsgCnt=1; uin=o1303377145; skey=@c94DdQ4TE; ptisp=cnc; p_uin=o1303377145; pt4_token=p2JLBSVmSLo8GOBy8KpRZ-JCObRKCrjV4D1ZNawdfJI_; p_skey=nC-V4Irz*Jh3e0dsnp8FdMG*3*7OeY40QNo-fqFhr3Y_; rv2=80630A11B4327FBE2013EA3A5B1F69E8CB8995A9969AA84B9B; property20=B4B0212077C9887F92612EF238BCDF817A667CE2CEB7321ED89982A556D92B8E3F3D79B8934FD68B; pgv_si=s6466100224; pgv_info=ssid=s4567547088'
}
def get_urlist(baseurl):

	doc = pq(baseurl,encoding = 'GBK')
	doc = doc('#con02-0 #NewStockTable')
	doc = doc.find('td')
	num = []
	for item in doc:
		if (len(pq(item).text()) == 6):
			num.append(pq(item).text())
	return num

def get_page(number):
	now_url = head+number+tail
	doc = pq(now_url,encoding = 'GBK')
	doc =doc('body .wrap .R .tagmain tbody')
	doc2 =doc.find('tr')
	test = doc2.children().text()
	data = test.split(' ')
	data1 = []
	for i in range(len(data)):
		if((i+1)%3!=0):
			data1.append(data[i])
	return data1

def get_and_save(run_url):
	url_list = get_urlist(run_url)
	for item in url_list:
		file_name = item+'.csv'
		doc = get_page(item)
		time = []
		data = []
		for i in range(len(doc)):
			if(i%2==0):
				time.append(doc[i])
			else:
				data.append(doc[i])
		file_csv = codecs.open(file_name,'w+','utf-8')#追加
		writer = csv.writer(file_csv, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
		headers = ['time','data']
		with open(file_name,'a',newline = '') as f:
			f_csv = csv.DictWriter(f, headers)
			f_csv.writeheader()
			for x,y in zip(time,data):
				temp = {}
				temp['time'] =x
				temp['data'] =y
				temp = [temp]
				f_csv.writerows(temp)
		print('Done!')


if __name__ =='__main__':
	get_and_save(run_url = url)