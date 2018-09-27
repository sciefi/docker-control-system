#!/usr/bin/env python3
# encoding: utf-8

import os
import docker
from docker.errors import DockerException
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from wsrpc import WebSocketRoute, WebSocket, wsrpc_static

define("listen", default='localhost')
define("port", default=8888, help='port to listen on')

client = docker.from_env()

class Routes(WebSocketRoute):

    def run(self, id):
        try:
            container = client.containers.run(id, detach=True, stdin_open=True, tty=True)
        except DockerException:
            return 'Docker exception'
        return "Container {0} is runned, {1}".format(container.short_id, str(container.image).replace('<', '').replace('>', ''))

    def stop(self, id):
        try:
            container = client.containers.get(id)
            container.stop()
        except DockerException:
            return 'Docker exception'
        return "Container {0} is stopped".format(id)

    def remove(self, id):
        try:
            container = client.containers.get(id)
            container.remove()
        except DockerException:
            return 'Docker exception'
        return "Container {0} is removed".format(id)

    def restart(self, id):
        try:
            container = client.containers.get(id)
            container.restart()
        except DockerException:
            return 'Docker exception'
        return "Container {0} is restarted".format(id)

    def get_images(self):
        images_list = client.images.list()
        return {elem.short_id: str(elem).replace('<', '').replace("Image: ", '').replace('>', '') for elem in images_list}

    def get_containers(self, show_all):
        containers_list = client.containers.list(all=show_all)
        return {elem.short_id: str(elem).replace('<', '').replace("Container: ", '').replace('>', '') for elem in containers_list}

WebSocket.ROUTES['route'] = Routes

class App(tornado.web.Application):
    def __init__(self):
        project_root = os.path.dirname(__file__)
        handlers = (
            wsrpc_static(r'/js/(.*)'),
            (r"/ws/", WebSocket),
            (r'/(.*)', tornado.web.StaticFileHandler, {
                'path': os.path.join(project_root, 'static'),
                'default_filename': 'index.html',
            }),
        )
        tornado.web.Application.__init__(self, handlers=handlers)

if __name__ == "__main__":
        http_server = tornado.httpserver.HTTPServer(App())
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
