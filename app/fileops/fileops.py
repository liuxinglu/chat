from flask import Blueprint, request, send_from_directory, g, jsonify,session
import os
from app.config import upload_folder,download_folder
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
from rake_nltk import Rake
import nltk

fileops_bp = Blueprint('file_ops', __name__)

nltk.download('stopwords')
nltk.download('punkt_tab')



rake_nltk_extractor = Rake()

@fileops_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        # 提取PDF中的文本
        doc = extract_text(filepath)
        # word_list = preprocess_and_tokenize_text(doc)
        keywords =  "" #extract_keywords(word_list)
        # session['doc'] = doc
        return jsonify({
            'message': 'File uploaded successfully',
            'text': doc,
            'keywords': keywords}), 200
    else:
        return jsonify({'error': 'File must be a PDF'}), 400


#  预处理文本并使用jieba进行分词
def preprocess_and_tokenize_text(text):
    # 清理文本（这里可以根据需要添加更多的清理步骤）
    text = text.strip()  # 去除前后空白
    # 使用jieba进行分词
    jieba.load_userdict(os.path.abspath(os.path.curdir + '/app/static/userdict.txt'))  # 加载自定义词典
    words = jieba.cut(text)
    # 将分词结果转换为列表形式（如果需要，可以进一步处理，如去除停用词）
    word_list = list(words)
    cleaned_list = [item for item in word_list if item not in ["\n", ", ", '（', '）', '【', '】']]
    # print(cleaned_list)
    return cleaned_list


# 将分词后的文本转换为字符串，并使用TF-IDF方法提取关键字
def extract_keywords(word_list, top_n=20):
    text = ' '.join(word_list)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # 获取top_n个关键字
    top_indices = tfidf_scores.argsort()[::-1][:top_n]
    keywords = [feature_names[i] for i in top_indices]
    return keywords


@fileops_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(upload_folder, filename)


@fileops_bp.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(download_folder, filename, as_attachment=True)

