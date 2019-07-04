import os.path
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

#定义端口为8080
define("port", default=8333, help="run on the given port", type=int)

# GET请求
class IndexHandler(tornado.web.RequestHandler):
    # get函数
    def get(self):
        self.render('index.html')

# POST请求
# POST请求参数： username
class InfoPageHandler(tornado.web.RequestHandler):
    # post函数
    def post(self):
        name = self.get_argument('username')
        command_line="docker exec -ti openvpn add-otp-user"+name
        raw_result = os.popen(command_line).read()
        split_list =raw_result.split('\n')
        data={}
        index=split_list[2].index(':')
        data['username']=name
        data['url']=split_list[0]
        data['secrest_key']=split_list[1][index:-1]
        data['raw_result']=raw_result
        result=json.dumps(data,  indent=4, separators=(',', ': '))
        self.write(result)

# 主函数
def main():
    tornado.options.parse_command_line()
    # 定义app
    app = tornado.web.Application(
            handlers=[ (r'/openvpn/otp-user/add', InfoPageHandler),(r'/', IndexHandler)], #网页路径控制
            template_path=os.path.join(os.path.dirname(__file__), "templates") # 模板路径//
          )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

main()