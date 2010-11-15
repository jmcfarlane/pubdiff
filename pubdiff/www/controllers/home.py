#Python imports
import json
import os
import shutil

# Third party imports
from chula import webservice

# Ocr imports
from pubdiff import review
from pubdiff.www.controllers import base

class Home(base.Controller):
    def index(self):
        return self.render('/home.tmpl')

    def review(self):
        r = review.Review('test')

        self.model = r
        return self.render('/diff.tmpl')

    @webservice.expose()
    def upload(self):
        was_uploaded = False

        if self.env.form_raw:
            TEMP_DIR = '/tmp/pubdiff_upload'
            paths_to_upload = []
            try:
                diffs = json.loads(self.env.form_raw)
                os.makedirs(TEMP_DIR)
                for diff in diffs:
                    # Reconstitute the source files on disk
                    paths = []
                    for state in ['before', 'after']:
                        source = diff[state]
                        name = os.path.basename(source['name'])
                        fq_path = os.path.join(TEMP_DIR, name)
                        paths.append(fq_path)
                        with open(fq_path, 'w') as fh:
                            fh.write(source['contents'])

                    # Append the (now on disk) paths to be uploaded
                    paths_to_upload.append(paths)

                # Perform actual upload to the db of all diffs
                review.upload(paths_to_upload)
                was_uploaded = True
            except Exception, ex:
                return repr(ex)
            finally:
                shutil.rmtree(TEMP_DIR)    
                

        if was_uploaded:
            return 'Diff(s) uploaded successfully'
        else:
            return 'Nothing uploaded'
