#!/usr/bin/env python
# encoding=utf8 

"""
by darkray | www.blackh4t.org
just a simple todo list webapp
feature:
    1.use text file to store infomation
    2.light
learn to use tornado & hv fun!
"""

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import os
import time

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define,options
define("port",default=8000,help="webapp listen on this port",type=int)

abs_path = os.path.abspath(__file__) 
app_path = os.path.dirname(__file__)
db_path = os.path.dirname(abs_path)+"/db/"
file_ext = [".txt"]

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',MainHandler),
            (r'/add',AddHandler),
            (r'/del',DelHandler),
            (r'/update',UpdateHandler),
            (r'/done',DoneHandler),
            (r'/undone',UndoneHandler)
        ]
        setting = dict(
            template_path = os.path.join(app_path,"tpl"),
            static_path = os.path.join(app_path,"static"),
            ui_modules={'Item':ItemModule},
            debug=True
        )
        tornado.web.Application.__init__(self,handlers,**setting)
        
        
class MainHandler(tornado.web.RequestHandler):
    def gettodolist(self):
        lists = []
        index_file = db_path + 'indexs'
        if (os.path.exists(index_file)):
            filelists = open(index_file,'r')
            for line in filelists:
                lists.append(line)
            return lists
        else:
            return None
            
    def delblank(self,path):
        lines = []
        infp = open(path, "r")
        for li in infp:
            if li.split():
                lines.append(li)
        infp.close()
        outfp = open(path, "w")
        for i in lines:
            outfp.writelines(i) 
        outfp.close()        
        pass
    
    def get(self):
        #index_file = db_path + 'indexs'
        #if(os.path.exists(index_file)):
        #    self.delblank(index_file)
        self.render(
        "index.html",
        page_title = "foolproof todo list",
        header_title = "Todo List",
        coder = "darkr4y(at)gmail.com",
        #get todo list
        items = self.gettodolist() if (self.gettodolist() != None) else ''
        )
        
class ItemModule(tornado.web.UIModule):
    def render(self,item):
        #list
        i = item.split('|')
        f = open(db_path + i[1][:-2],'r')
        line = f.readline().split('|')
        return self.render_string('item.html', todo_id=i[0],todo_item=line)
        pass
    
    def embedded_javascript(self):
        return ''



class AddHandler(tornado.web.RequestHandler):
    def post(self):
        todo_content = self.get_argument('addinput')
        todo_content = todo_content.replace('|','') 
        timestamp = time.time()
        nowtime = time.strftime('%Y-%m-%d %H:%M',time.localtime(timestamp))
        if (todo_content != ''):
            #write index
            todo_filename = str(int(time.time())) + ".txt"
            self.write(todo_filename)
            index_file = open(db_path + "indexs",'a')
            #get lines
            index_file.write(str(timestamp) + '|' + todo_filename)
            index_file.write("\r\n")
            index_file.close
            self.write(db_path + "indexs")
            #write content
            content_file = open(db_path + todo_filename,'w')
            content_file.write(nowtime + '|' + todo_content + '|0') 
            # 0 for undone & 1 for done
            content_file.close
            #self.write(db_path + todo_filename)
            self.write('added!')
        else:
            self.write('error!')
            

class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    
    def post(self):
        update_id = self.get_argument('tid')
        update_content = self.get_argument('updateinput')
        update_content = update_content.replace('|','')
        #get index id
        lines = []
        index_file = open(db_path + 'indexs','r')
        for i in index_file:
            item = i.split('|')
            update_line = item[0]
            if( update_line == update_id ):
                update_file = item[1][:-2]
        #update content
        f = open(db_path + update_file,'r')
        x = f.readline().split('|')
        f.close()
        new_f = open(db_path + update_file,'w+')
        new_x = x[0] + '|' + update_content + '|' + x[2]
        new_f.write(new_x)
        new_f.close()
        pass
    pass


class DelHandler(tornado.web.RequestHandler):               
    def post(self):
        #del index id
        lines = []
        todo_id = self.get_argument('tid')
        index_file = open(db_path + 'indexs','r')
        for i in index_file:
            todo_file = i.split('|')
            if (todo_file[0] == todo_id):
                del_file = db_path + todo_file[1][:-2]
            lines.append(i)
        index_file.close()
        f = open(db_path + 'indexs','w+')
        for x in lines:
            todo_del = x.split('|')
            if (todo_del[0] != todo_id):
                f.write(x)
        f.close()
        #del content
        if(os.path.exists(del_file)):
            os.remove(del_file)
            
            
            
            
        
        
class DoneHandler(tornado.web.RequestHandler):
    def post(self):
        todo_id = self.get_argument('tid')
        #get index id
        index_file = open(db_path + 'indexs','r')
        for i in index_file:
            todo_file = i.split('|')
            #self.write(todo_file[0])
            #self.write(todo_file[1])
            if (todo_file[0] == todo_id):
                #read status
                r = open(db_path + todo_file[1][:-2],'r')
                line = r.readline()
                r.close
                #write status
                f = open(db_path + todo_file[1][:-2],'w')
                newline = line[:-1] + '1'
                f.write(newline)
                f.close()
                self.write(line)
        pass
    pass
        
        
        
class UndoneHandler(tornado.web.RequestHandler):
    def post(self):
        todo_id = self.get_argument('tid')
        #get index id
        index_file = open(db_path + 'indexs','r')
        for i in index_file:
            todo_file = i.split('|')
            #self.write(todo_file[0])
            #self.write(todo_file[1])
            if (todo_file[0] == todo_id):
                #read status
                r = open(db_path + todo_file[1][:-2],'r')
                line = r.readline()
                r.close
                #write status
                f = open(db_path + todo_file[1][:-2],'w')
                newline = line[:-1] + '0'
                f.write(newline)
                f.close()
                self.write(line)        
        pass
    pass
        


# main
if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

