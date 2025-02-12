from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechRecognizer, SpeechSynthesisResult, ResultReason
import os, io
from azure.storage.blob import BlobServiceClient, BlobClient, generate_blob_sas,BlobSasPermissions
from datetime import datetime, timedelta

class AzureService:

    connect_str = f"DefaultEndpointsProtocol=https;AccountName={os.getenv('STORAGE_ACCOUNT_NAME')};AccountKey={os.getenv('STORAGE_ACCOUNT_KEY')};EndpointSuffix=core.windows.net"

    @staticmethod
    def transcribe_speech(self, audio_data):
        dll_path = r"C:\Users\xinglu\PycharmProjects\chat\venv\Lib\site-packages\azure\cognitiveservices\speech\Microsoft.CognitiveServices.Speech.core.dll"
        os.environ["PATH"] += os.pathsep + os.path.dirname(dll_path)
        speech_config = SpeechConfig(subscription=os.getenv('SPEECH_SUBSCRIPTION'), region=os.getenv('SPEECH_REGION'))
        audio_config = AudioConfig(stream=audio_data)

        speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once_async().result  # The first result contains the text from the audio

        if result.reason == ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == ResultReason.NoMatch:
            return "No speech could be recognized"
        elif result.reason == ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return f"Recognition was canceled: {cancellation_details.reason}"
        return ""

    @staticmethod
    def get_sas_url(container_name, blob_name, expiry=3600):
        blob_service_client = BlobServiceClient.from_connection_string(AzureService.connect_str)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            blob_name=blob_name,
            expiry=datetime.now() + timedelta(seconds=expiry),
            permission=BlobSasPermissions(read=True),
        ).decode('utf-8')

        blob_url = blob_client.url
        return f"{blob_url}?{sas_token}"

    @staticmethod
    def get_blob_client(container_name, blob_name):
        container_client = BlobServiceClient.from_connection_string(AzureService.connect_str).get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client

    @staticmethod
    def upload_to_blob_storage(container_name, blob_name, data):
        blob_client = AzureService.get_blob_client(container_name, blob_name)
        blob_client.upload_blob(data, blob_type="BlockBlob")

    @staticmethod
    def download_from_blob_storage(container_name, blob_name):
        blob_client = AzureService.get_blob_client(container_name, blob_name)
        download_stream = io.BytesIO()
        blob_client.download_blob().readinto(download_stream)
        download_stream.seek(0)  # 重置流位置到开始
        return download_stream


    # 上传语音文件
    @staticmethod
    def upload_file(self, file, user_id):
        # Read the file content into a byte array
        file_content = file.read()

        # Convert the byte array to an in-memory stream for the Speech SDK
        audio_stream = io.BytesIO(file_content)
        AzureService.upload_to_blob_storage(os.getenv('VOICE_CONTAINER_NAME'), audio_stream)
        # Transcribe the speech
        transcribed_text = AzureService.transcribe_speech(audio_stream)

        # Upload the transcribed text to Blob Storage
        AzureService.upload_to_blob_storage(os.getenv('USER_PROMPT_CONTAINER_NAME'), os.getenv('USER_PROMPT_BLOB_NAME'), transcribed_text)

        # uploaded_file = UploadedFile(filename=filename, content=transcribed_text, user_id=user_id)
        # db.session.add(uploaded_file)
        # db.session.commit()
        # return uploaded_file
        return transcribed_text
