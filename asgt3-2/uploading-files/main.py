import webapp2
import template

from google.appengine.ext import db

FILE_LIST = db.Key.from_path('FILE', 'LIST')


class File(db.Model):
    name = db.StringProperty()
    mime_type = db.StringProperty()
    content = db.BlobProperty()
    uploaded_at = db.DateTimeProperty(auto_now_add=True)
    tag = db.StringListProperty()


class ListFilesHandler(webapp2.RequestHandler):

    def get(self):
        files = template.variable()
        tagQuery = self.request.get('tag')

        if (tagQuery):
            for f in File.all().ancestor(FILE_LIST).filter("tag =", tagQuery).order('-uploaded_at'):
                fileString =  '<li><a href="/download/%s">%s</a> Tags:' \
                                % (f.name, f.name)
                for t in f.tag:
                    fileString += '<a href="/list?tag=%s">%s</a>, ' \
                            % (t, t)
                print >>files, fileString
        else:               
            for f in File.all().ancestor(FILE_LIST).order('-uploaded_at'):
                fileString =  '<li><a href="/download/%s">%s</a> Tags:' \
                                % (f.name, f.name)
                for t in f.tag:
                    fileString += '<a href="/list?tag=%s">%s</a>, ' \
                                % (t, t)
                print >>files, fileString
                
        html = template.render(
            'list.html',
            {'file_list': files},
            escaped=False
        )
        self.response.write(html)


class UploadFileHandler(webapp2.RequestHandler):

    def post(self):
        uploaded_file = self.request.POST['uploaded_file']

        try:
            saved_file = File(parent=FILE_LIST)

            saved_file.name = uploaded_file.filename
            saved_file.mime_type = uploaded_file.type
            saved_file.content = uploaded_file.file.read()
            saved_file.tag = self.request.POST['tags'].strip('%20').split(',');

            saved_file.put()
        except AttributeError:
            self.abort(400)

        self.redirect('/list')


class DownloadFileHandler(webapp2.RequestHandler):
    def get(self, filename):
        result = File.all().ancestor(FILE_LIST).\
                            filter('name =', filename).get()
        if not result:
            self.abort(404)

        self.response.headers['Content-Type'] = str(result.mime_type)
        self.response.write(result.content)

app = webapp2.WSGIApplication([
    ('/', ListFilesHandler),
    ('/list', ListFilesHandler),
    ('/upload', UploadFileHandler),
    ('/download/(.*)', DownloadFileHandler)
], debug=True)
