"""
简单的HTTP服务器，用于测试AI续写功能（解决CORS问题）
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

class TestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """处理POST请求"""
        if self.path.startswith('/api/ai/simple-write'):
            # 获取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                # 解析请求数据
                data = json.loads(post_data.decode('utf-8'))
                print(f"收到请求: {data}")

                # 转发到后端API
                backend_url = 'http://localhost:8000/api/ai/simple-write'
                req = urllib.request.Request(
                    backend_url,
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )

                # 发送请求到后端
                with urllib.request.urlopen(req) as response:
                    response_data = response.read().decode('utf-8')
                    print(f"后端响应: {response_data}")

                # 发送响应
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data.encode('utf-8'))

            except Exception as e:
                print(f"错误: {e}")
                # 发送错误响应
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = json.dumps({
                    "status": "error",
                    "message": str(e)
                })
                self.wfile.write(error_response.encode('utf-8'))
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.address_string()}] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), TestHandler)
    print("测试服务器启动在 http://localhost:8080")
    print("请访问 http://localhost:8080/test_ai_write_frontend.html")
    print("\n注意：确保后端服务器在 http://localhost:8000 运行")
    print("按 Ctrl+C 停止服务器")
    server.serve_forever()