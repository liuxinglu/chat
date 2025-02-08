# file_ops_service.py

import os
from pdfminer.high_level import extract_text
from app.model.models import UploadedFile, db
from app.config import upload_folder
from werkzeug.utils import secure_filename
from app.services.azure_service import AzureService

class FileOpsService:
    # 上传文件
    def upload_file(self, file, user_id):
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # 提取PDF中的文本
        doc = extract_text(filepath)

        # 将文件信息保存到数据库
        uploaded_file = UploadedFile(filename=filename, content=doc, user_id=user_id)
        db.session.add(uploaded_file)
        db.session.commit()
        return uploaded_file

    # 获取文件内容
    def get_file_content(self, filename):
        filepath = os.path.join(upload_folder, filename)
        return extract_text(filepath)

    # 获取文件上传历史记录
    def get_upload_history(self, user_id):
        files = UploadedFile.query.filter_by(user_id=user_id).all()
        return [{'fileid': f.id, 'filename': f.filename, 'upload_date': f.upload_date, 'content': f.content} for f in files]

    # 删除指定文件记录
    def delete_file(self, user_id, file_id):
        file_to_delete = UploadedFile.query.filter_by(user_id=user_id, id=file_id).first()
        if not file_to_delete:
            return None
        db.session.delete(file_to_delete)
        db.session.commit()
        return True


